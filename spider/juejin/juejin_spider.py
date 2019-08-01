import time
import requests
import pymysql
import json
import random
from lxml import etree

"""
下面是自定义的模块
"""
from spider import config
from spider.utils import logger
from spider.juejin.const import DATA_DICT, HEADERS


class JueJinSpider(object):
    """
    掘金网数据抓取类

    """

    def __init__(self, data_dict=None, crawl_page=6):
        """
        :param crawl_page:要抓去页数
        """
        self.conn = None
        self.cursor = None
        self.mysql_util = None
        self.crawl_url = "https://web-api.juejin.im/query"
        self.crawl_page = crawl_page
        self.after = ""

        if not data_dict:
            raise Exception('请填写正确的请求数据！')
        self.data_dict = data_dict

    def get_data(self, post_data):
        if self.after:
            data = post_data['data'].replace('{after}', self.after)
        else:
            data = post_data['data'].replace('{after}', "")

        try:
            query_response = requests.post(self.crawl_url, data=data, headers=HEADERS)
        except Exception as e:
            print('数据列表请求失败,原因是:', e)
            logger.warning('数据列表请求失败,原因是:', e)
        else:
            query_response = json.loads(query_response.text)
            if query_response.get('data') and query_response['data'].get('articleFeed') and \
                    query_response['data']['articleFeed'].get('items'):
                items = query_response['data']['articleFeed']['items']
            else:
                return
            has_next_page = items['pageInfo']['hasNextPage']

            for item in items['edges']:
                HEADERS['User-Agent'] = self.random_user_agent()

                if item['node'].get('category'):
                    category = item['node']['category']['name']
                    category = self.choice_category(category)
                    # print('category:---上', category)
                else:
                    category = post_data['category']
                    # print('category:---下下下', category)
                    logger.warning('不存在分类标签，说明是除推荐以外的东西！')

                article_response = requests.get(item['node']['originalUrl'], headers=HEADERS)
                html = etree.HTML(article_response.text)

                title = html.xpath('//title/text()')[0]
                if self.distinct_data(title) == 'filter it':
                    # 如果已经存在，就舍弃
                    print(title, ' -- 已经存在')
                    continue

                article_content = html.xpath('//div[@class="article-content"]')
                if not article_content:
                    continue
                else:
                    article_content = article_content[0]

                article_content = etree.tostring(article_content).decode('utf-8')
                article_content = pymysql.escape_string(
                    article_content.replace('data-src', 'src').replace('<pre>', '<br><br><pre>'))

                data_item = dict()
                data_item['content'] = article_content
                data_item['title'] = title
                data_item['category'] = category
                data_item['origin_url'] = item['node']['originalUrl']

                self.insert_data(data_item)

                print(title, ' -- 存储成功', category)
            if has_next_page:
                self.after = items['pageInfo']['endCursor']
            else:
                self.after = ''

    def distinct_data(self, title):
        """
        文章去重，根据title字段
        :param title:
        :return:
        """
        sql = 'SELECT title FROM article_article WHERE title="%s"' % title
        results = self.mysql_util.select(sql)
        if results:
            return 'filter it'
        else:
            return 'insert it'

    def insert_data(self, item):
        title = item['title']
        content = item['content']
        category = item['category']
        origin_url = item['origin_url']
        author_id = self.random_author_id()

        sql = "INSERT INTO article_article(title,content,create_time,category_id,author_id,origin_url) " \
              "VALUES ('{title}','{content}','{create_time}','{category_id}','{author_id}','{origin_url}');".format(
            title=title, content=content, create_time=self.now(),
            category_id=category, author_id=author_id, origin_url=origin_url)
        self.mysql_util.insert(sql)

    def run(self):
        """
        运行程序
        :return:
        """
        self.mysql_util = MysqlUtil(DB_CONFIG)

        for data in self.data_dict:
            for i in range(self.crawl_page):
                self.get_data(data)

        self.mysql_util.close()

    @staticmethod
    def now():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    @staticmethod
    def random_user_agent():
        return random.choice(config.MY_USER_AGENT)

    @staticmethod
    def random_author_id():
        """
        随机选择用户id，给匹配上文章
        :return:
        """

        user_ids = [1, 2, 3, 4]
        return random.choice(user_ids)

    @staticmethod
    def choice_category(category):
        """
        把掘金上面文章对应到我这边的标签
        :return:
        """
        category_dict = {
            '人工智能': '4',
            '后端': '6',
            '代码人生': '7',
            '前端': '9',
            'Android': '10',
            'IOS': '10',
            '计算机基础': '14',
            '其他': '15',
        }
        if category_dict.get(category):
            return category_dict.get(category)
        else:
            return category_dict['其他']


class MysqlUtil(object):
    """
    数据库管理工具类
    """

    def __init__(self, db_config=None):
        if not db_config:
            raise Exception('Please configure actual database param！')

        self.conn = pymysql.connect(**db_config)
        self.cursor = self.conn.cursor()

    def insert(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def select(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def update(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    """执行程序，每次会跑一边全部标签，抓2页"""

    DB_CONFIG = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'wei19960722',
        'database': 'person_blog_system',
    }

    jj = JueJinSpider(data_dict=DATA_DICT, crawl_page=2)
    jj.run()

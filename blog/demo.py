# -*- coding:utf-8 -*-

num = [1, 4, -5, 10, -7, 2, 3, -1]
filter_square = map(lambda x:x**2,filter(lambda x:x>0, num))
print(list(filter_square))
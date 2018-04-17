# -*- coding: utf-8 -*-
import re
a = '<a href="https://www.baidu.com//articles/gz.html" title="贵州省">贵州省主题介绍</a> '

print re.findall(r'href="(.*?)"', a)

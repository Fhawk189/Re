# -*- coding: utf-8 -*-
import requests
import re
from itertools import izip
from json import dumps
from urllib import quote
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/62.0.3202.89 Safari/537.36',
}


def write_file(all_info):
    fp = open('info.xls', 'a')
    for info in all_info:
        fp.write(dumps(info, encoding='utf-8', ensure_ascii=False, sort_keys=False, indent=4))
        fp.write('\n')
    fp.close()


def get_html(work, where, page_num):
    where = quote(where)  # %E5%8C%97%E4%BA%AC
    work = quote(work)
    url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%s&kw=%s&sm=0&p=%s' % (where, work, page_num)
    response = requests.get(url, headers=headers).text
    return response


def get_info(response):
    one_work_info = dict()
    salary = re.findall(r'<td class="zwyx">(.*?)</td>', response)
    work_locate = re.findall(r'<td class="gzdd">(.*?)</td>', response)
    company = re.findall(r'<td class="gsmc"><a href=.*?>(.*?)<a href=.*?></a></td>', response)
    work_name = re.findall(r'<a style="font-weight: bold".*?>(.*?)</a>', response)
    work_paticuler_info = re.findall(r'<a style="font-weight: bold".*?href="(.*?)".*?>', response)
    company_info = re.findall(r'<td class="gsmc"><a href="(.*?)".*?>', response)
    for salary, locate, company, work, work_info, company_info in \
            izip(salary, work_locate, company, work_name, work_paticuler_info, company_info):
        one_work_info['salary'] = salary
        one_work_info['work_locate'] = locate
        one_work_info['company'] = re.sub(r'<.*?>', '', company)
        one_work_info['work_name'] = re.sub(r'<.*?>', '', work)
        one_work_info['work_paticuler_info'] = work_info
        one_work_info['company_info'] = company_info
        yield one_work_info


def run():
    work = raw_input(u"请输入你想要查询的工作：")
    where = raw_input(u"请输入你要查询的工作地点：")
    find_num = input(u"请输入爬取多少页数据：")
    for i in range(find_num):
        html = get_html(work, where, i)
        work_info = get_info(html)
        write_file(work_info)


if __name__ == '__main__':
    run()

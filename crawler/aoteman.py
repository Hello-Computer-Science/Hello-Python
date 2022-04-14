import csv
import re
import requests
from bs4 import BeautifulSoup

# 声明 UA
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
}


# run方法
def run():
    url = "http://www.ultramanclub.com/allultraman/"
    try:
        res = requests.get(url=url, timeout=10)
        res.encoding = "gb2312"
        html = res.text
        # 获取链接列表
        return getLinks(html)

    except Exception as e:
        print("发生异常", e)


# 获取链接
def getLinks(html):
    startTag = '<ul class="lists">'
    start = html.find(startTag)
    html = html[start:]
    links = re.findall('<li class="item"><a href="(.*)">', html)
    print(links)
    # links = list(set(links)) # set去重
    links = [f"http://www.ultramanclub.com/allultraman/{i.split('/')[1]}/" for i in set(links)]  # 拼接url成 'http://www.ultramanclub.com/allultraman/xxx/' 的格式
    # print(links)
    return links


# 获取详情
def getDetail(url):
    try:
        # 网页访问速度慢，需要设置 timeout
        res = requests.get(url=url, headers=headers, timeout=15)
        res.encoding = "gb2312"
        html = res.text
        # 去除简介中的换行符，否则标签中返回的字符串为None，e：must be str, not NoneType
        html = (html.replace('<br>', '')).replace('<br/>', '')
        soup = BeautifulSoup(html, "lxml")
        data = []  # 单个奥特曼详情

        # 名称
        name = re.search('<title>(.*?)\[', html).group(1)
        print("名称：" + name)
        data.append(name)
        # 必杀技
        skillDiv = soup.find(name='div', class_='skill')
        # 有的奥特曼页面没有必杀技，判空
        if not skillDiv:
            skill = "没有"
        else:
            skill = skillDiv.find('dd').string
        print("必杀技：" + skill)
        data.append(skill)
        # 简介
        introP = soup.find(name='p', class_='introduction')
        # 注意这里获取要用text，用string的话如果p标签中含有<br/>会导致soup.find().string为None
        intro = introP.text
        print("简介:" + intro)
        data.append(intro)

        print(data)
        return data
    except Exception as e:
        print("********************************************")
        print(url)
        print("爬取详情发生异常", e)


def saveUltraman4Csv(result):
    headers = ['名称', '必杀技', '简介']

    # 创建
    filename = '奥特曼图鉴.csv'
    with open(filename, 'a', newline="", encoding='utf-8-sig')as csvfile:
        write = csv.writer(csvfile)
        write.writerow(headers)
        write.writerows(result)


if __name__ == '__main__':
    print("开始爬取奥特曼详情...")
    details = run()
    dataList = []  # 初始化奥特曼详情列表
    for detail in details:
        # for i in range(2):
        #     data = getDetail(details[i])
        data = getDetail(detail)
        dataList.append(data)
    print(dataList)
    print("数据爬取完毕!")
    saveUltraman4Csv(dataList)
    print("数据保存完毕!")
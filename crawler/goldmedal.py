import os
import time
import codecs
import requests
import prettytable as pt
url = 'https://api.cntv.cn/olympic/getOlyMedals'
params = {
    'serviceId': 'pcocean',
    'itemcode': 'GEN-------------------------------',
}
json = requests.get(url, params=params).json()
result = json['data']['medalsList']
tb = pt.PrettyTable()
tb.field_names = ["排名", "国家或地区", "金牌数", "银牌数", "铜牌数", "总获奖数"]
for r in result:
    tb.add_row([r['rank'], r['countryname'].ljust(10),
               r['gold'], r['silver'], r['bronze'], r['count']])
print(tb)
filePath = 'medal.txt'
# 写入文件
# f = codecs.open(filePath, 'a', encoding='utf-8')
# f.write(str(os.linesep + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())) + os.linesep + os.linesep + str(tb) + os.linesep)

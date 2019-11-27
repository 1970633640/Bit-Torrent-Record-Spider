import requests
from pyquery import PyQuery as pq
from netaddr import *

def getDownload(ip, file1, file2):
    response = requests.get("https://iknowwhatyoudownload.com/en/peer/?ip=%s" % ip).content.decode('utf-8')
    doc = pq(response)
    locs = []
    for i in doc(".label-primary").items():
        locs.append(i.text())
    loc = ' '.join(locs[-2:])
    info = doc(".label-info").text()
    file1.write(','.join([ip, loc, info]))
    file1.write('\n')
    for tr in doc("tbody").children().items():
        data = []
        for i in tr(".date-column").items():
            data.append(i.text().replace(',','.'))
        if len(data) != 2:
            data = ['err', 'err']
        data.append(tr(".category-column").text())
        data.append(tr('.name-column').text().strip().replace(',', '，'))
        data.append(tr(".size-column").text())
        if len(data) == 5:
            file2.write("%s,%s\n" % (ip, ','.join(data)))

def getIP(ip):
    response = requests.get("https://iknowwhatyoudownload.com/en/peer/?ip=%s" % ip).content.decode('utf-8')
    doc = pq(response)
    ips=[]
    for i in doc('.bold-links').items():
        ips.append(i.text())
    return ips[1:]

file1 = open("ip.csv", "a", encoding="utf-8")
file2 = open("download.csv", "a", encoding="utf-8")

CIDRs=['1.2.3.4/24']
for CIDR in CIDRs:
    ip_cidr=IPNetwork(CIDR)
    for ip in ip_cidr.subnet(24):
        print(ip[0])
        ips=getIP(ip[0])
        for ip1 in ips:
            getDownload(ip1,file1,file2)
file1.close()
file2.close()
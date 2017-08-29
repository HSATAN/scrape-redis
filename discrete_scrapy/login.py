# coding=utf8
from scrapy.selector import Selector
import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Upgrade-Insecure-Requests':'1',
    'Referer':'http://www.missevan.com/member/login',
    'Origin':'http://www.missevan.com',
    'Host':'www.missevan.com'
}

#  账户名和密码
data = {
    'LoginForm[username]': '18813045328',
    'LoginForm[password]': 'raybo2017'
}

url = 'http://www.missevan.com/member/login?backurl=%2F'  #登陆地址
main_url = 'http://www.missevan.com'
#   用session保持登陆状态

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='mzhan_cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print 'cookie 不存在'


def login():
    response = session.post(url=url, data=data)
    session.cookies.save()
    return session

def is_login():

    response = session.get(main_url)
    sel = Selector(response)
    flag = sel.xpath('//li[@class="user-menu"]/a/text()').extract()
    if flag:
        flag = ''.join(flag).strip('\n ')
        print '当前登陆账户--' ,flag
        return True
    return False
if __name__=='__main__':
    if not is_login():
        login()

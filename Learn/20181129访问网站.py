# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-10-25 12:10:57
# @Last Modified by:   何睿
# @Last Modified time: 2018-10-25 12:11:20


from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
from multiprocessing import Pool
from ips import proxies
from secret import qq_email_pwd
import urllib.request
import urllib.error
import random
import time


class simulation():
    # 这个类是用来模拟访问网站，即增加网站访问量
    def __init__(self, Refer="https://www.ruicore.cn/"):
        self.DNT = 1
        self.Refer = Refer
        self.scheme = "https"
        self.accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        self.AcceptLanguage = "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        self.UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"

    def get(self, url, random_proxy):
        proxy_support = urllib.request.ProxyHandler({"http": random_proxy})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        opener.addheaders = [
            ("DNT", self.DNT),
            ("Referer", self.Refer),
            ("scheme", self.scheme),
            ("accept", self.accept),
            ('Accept-Language', self.AcceptLanguage),
            ('User-Agent', self.UserAgent),
        ]
        response = urllib.request.urlopen(url)
        return response.code

    def mail(self, ip, code=-1):
        host_server = "smtp.qq.com"
        qq = "764808240"
        pwd = qq_email_pwd
        sender_qq_mail = '764808240@qq.com'
        receiver = 'rui@ruicore.cn'
        mail_content = "访问失败,ip地址"+str(ip)+"错误代码"+str(code)
        mail_title = "访问失败"
        smtp = SMTP_SSL(host_server)
        smtp.set_debuglevel(1)
        smtp.ehlo(host_server)
        smtp.login(qq, pwd)
        msg = MIMEText(mail_content, 'plain', 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = sender_qq_mail
        msg["To"] = receiver
        smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
        smtp.quit()

    def surf(self, url):
        count = 0
        while True:
            sleep_time = random.randint(3, 5)
            time.sleep(sleep_time)
            random_proxy = random.choice(proxies)
            count += 1
            try:
                code = self.get(url, random_proxy)
                print("第"+str(count)+"次", "sleep" +
                      str(sleep_time)+"秒", random_proxy, code)
            except urllib.request.HTTPError as e:
                self.mail(random_proxy, e.code)
            except urllib.request.URLError as err:
                self.mail(random_proxy, err.reason)


if __name__ == "__main__":
    url = "https://www.ruicore.cn/"
    p = Pool(5)
    baidu = "https://www.baidu.com/link?url=NQ0j6ayGSL6B14P7WqHhK9rFUGWx5Pe-eZ5dZMhrm3m&wd=&eqid=9ff285fa0000919a000000025bd154ab"
    sougou = "http://www.so.com/link?m=ajwvr2eZKcIhsw9M%2BGxYBRfN0AUCx9j4BSD1CDwt8IfTLDW8kkQ6Ct0l9Z0QHLYDvQ9zgzqhvzhSI%2B%2B2LsiRpVpL6aTI%3D"
    yandex = "http://yandex.com/clck/jsredir?bu=kxnz&from=yandex.com%3Bsearch%2F%3Bweb%3B%3B&text=&etext=1950.3wehAOiFm-OzjdE2Qyqb3dr4gDcKAeUNN8O44ROeows.82fb8450605a2ad5f902c4f137c0cfca4b3dddd3&uuid=&state=PEtFfuTeVD5kpHnK9lio9bb4iM1VPfe4W5x0C0-qwflIRTTifi6VAA,,&&cst=AiuY0DBWFJ5fN_r-AEszk75kcxsfaUPnvsaFv86mQMHmgM2XpeVZygE_AQKBa_K45HTjPPdZtOQ91lPR6K2UU6ooPrX8L6V86HOwEWwbmposEgdVYL01u5-dNozBuMu0x8X6bSxhAkUAd2aELwCzGJ2bUOWok5YiXvtL3FrZpWx97aQv-nHOfqy-HRgYSuIOzdrB7S1sCblleknOEii_R4YfONS16HvoOH08inN8R92KkmrM8k0xJrvs-Y_UWLVdAQYp1R7SJzvenm2FCkiAUg,,&data=UlNrNmk5WktYejY4cHFySjRXSWhXTjV4ejlwR1pPdm1fcFVOd1VaTzdBT0l5UExBMm83VzZfWDVmcjdlWWRTbXM4Z19IWlRjTUtMNGNqREc0NEdxNk1JYnd4RXVSRlduOEhobjhCZHdWOU0s&sign=a3870a3ea637fadcb42595ab9b1b1b5f&keyno=0&b64e=2&ref=orjY4mGPRjkh5N2Mxdt9IijjiAnZEKSkYaBtQufTH9sLzItZt2SREdvy9ql8shXwlAoyQ8KKmyf54xeJsm8zZ2mySCJgZNOYm1YKHcAaFi4u8BVlxJrJ0Q,,&l10n=en&rp=1&cts=1540445944096&hdtime=3821.8"
    rambler = "https://nova.rambler.ru/cl?rex=521C082D55DEB83B&block=serp&st=1540446073&id=title_1&rnd=0.7804583381256931&key=ScsFVUujNH2hXxqgR6nv4CeTBcAADAWQ1xyuLnvs5J-uRmI4RifxKICr1qF0PEGh4klRy4q0ZnZbLDtFAzLnzLWVMO7uC4AOzmuTZXt2bAy6v6rgmW_LNSV-sF7faV999kQUA1kwVQdoOF1CiIvh5A==&_URL=https%3A%2F%2Fwww.ruicore.cn%2F"
    baidu_js = "https://hm.baidu.com/hm.js?80ede74ee7cab31fe3b63ae77e36b6e7"
    sim_baidu = simulation(Refer=baidu)
    sim_sougou = simulation(Refer=sougou)
    sim_yandex = simulation(Refer=yandex)
    sim_rambler = simulation(Refer=rambler)
    sim_baidujs = simulation()
    p.apply_async(sim_baidu.surf, args=(url,))
    p.apply_async(sim_sougou.surf, args=(url,))
    p.apply_async(sim_yandex.surf, args=(url,))
    p.apply_async(sim_rambler.surf, args=(url,))
    p.apply_async(sim_baidujs.surf, args=(baidu_js,))
    p.close()
    p.join()

#encoding=utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import sys
import xlsxwriter
import xlwt
import xlrd

reload(sys)
sys.setdefaultencoding('utf-8')

def Get_Create(url,F):#url是网页地址，F是所有人名字的list
    driver=webdriver.Chrome()
    driver.get(url)
    driver.find_element_by_id('username').send_keys('KS_GLXY')
    driver.find_element_by_id('password').send_keys('1736802373')
    driver.find_element_by_id('button').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="bar_con"]/div[3]/img').click()
    time.sleep(2)
    js=" var frames = document.getElementsByTagName('iframe');return frames[0].id;"
    num=driver.execute_script(js)
    driver.switch_to_frame(num)#得到id，转到iframe框架中
    Num=len(F)#总人数
    book=xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet=book.add_sheet("Sheet1",cell_overwrite_ok=True)
    Num_tr=3#初始位置
    Col=0#初始行位置
    for i in range(0,Num):
        driver.find_element_by_id('manual_name').send_keys(F[i])
        driver.find_element_by_xpath('//*[@id="form1"]/table/tbody/tr['+str(Num_tr)+']/td/div/input[2]').click()
        bs=BeautifulSoup(driver.page_source,"lxml")
        table=bs.find_all('table')
        tab=table[0]
        Num_tr=len(tab.findAll('tr'))#获取表格行的个数，用于下一次Xpath定位
        tr=tab.findAll('tr')
        for n in range(0,Num_tr-4):#需要写入的行数
            y=0
            for td in tr[n+1].findAll('td'):
                sheet.write(Col,y,td.getText())
                y=y+1
            Col=Col+1
        #tr=tab.findAll('tr')[1]
        #for td in tr.findAll('td'):
        #    sheet.write(i,y,td.getText())
        #    y=y+1
    add='C:/HeRui/result.xls'
    book.save(add)
   

def GetName(address,num):
    workbook=xlrd.open_workbook(address)
    sheet=workbook.sheet_by_name('Sheet1')
    Re=[]#所有的名字放在一个一个list中
    x=3
    y=1
    for i in range(0,num):
        Re.append(sheet.cell_value(x,y))
        x=x+1
    return Re

url ='http://lgdy.whut.edu.cn/Panel/'

F=GetName(u'C:/HeRui/何睿.xls',143)
Get_Create(url,F)
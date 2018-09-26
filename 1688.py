import os
import time

import jprops
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from papago import Translator
from tkinter import *
from io import BytesIO

client_id = ""
client_secret = ""
translator = Translator(str(client_id), str(client_secret))

def openDriver(driverPath) :
    global driver
    driver = webdriver.Chrome(driverPath)


def scroll(cnt):
    for i in range(cnt):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(0.3)

def jqueryScroll(cnt):
    height = 500
    for i in range(cnt):
        driver.execute_script("$('#J_M_Detail_PageLayoutContent').scrollTop("+str(height)+")")
        height = height + 1000
        time.sleep(1)

def getUrl(dir):
    driver.get(dir)

def getElement(css_selector):
    return driver.find_element(By.CSS_SELECTOR, css_selector)

def getDriverElement(cusDriver ,css_selector):
    return cusDriver.find_element(By.CSS_SELECTOR, css_selector)


def getElements(css_selector):
    return driver.find_elements(By.CSS_SELECTOR, css_selector)

def getDriverElements(cusDriver, css_selector):
    return cusDriver.find_elements(By.CSS_SELECTOR, css_selector)


def sendKey(css_selector, val):
    driver.find_element(By.CSS_SELECTOR, css_selector).send_keys(val)


def elementsClick(css_selector, idx) :
    driver.find_elements(By.CSS_SELECTOR, css_selector)[idx].click()

def click(css_selector) :
    driver.find_element(By.CSS_SELECTOR, css_selector).click()

def driverClick(cusDriver ,css_selector):
    cusDriver.find_element(By.CSS_SELECTOR, css_selector).click()


def newTab(url):
    driver.execute_script("window.open('" + url + "')")
    handles = driver.window_handles
    tab = handles[len(handles) - 1]
    driver.switch_to.window(tab)

def closeTab(tabIdx):
    driver.close()
    handles = driver.window_handles
    try :
        driver.switch_to.window(handles[tabIdx])
    except Exception :
        driver.switch_to.window(handles[0])



def mkdir(path):
    if os.path.isdir(rootPath) :
        print()
    else :
        os.mkdir(rootPath)
    makeDir = os.path.join(rootPath, path)
    if os.path.isdir(makeDir):
        print()
    else :
        os.mkdir(makeDir)

def saveFile(path, name, str) :
    mkdir(path)
    f = open(rootPath + "/" + path + '/' +name, mode="w", encoding="utf-8")
    f.write(str)
    f.close()

def refreshPrevention() :
    handlers = driver.window_handles
    main = handlers[0]
    driver.switch_to.window(main)
    time.sleep(0.5)
    driver.switch_to.window(handlers[len(handlers) -1])

def saveImage(path, url, imgCnt):
    mkdir(path)
    etc = url[url.rindex("."):len(url)]
    f = open(rootPath + "/" + path + '/' + 'img' + str(imgCnt) + etc,'wb')
    f.write(requests.get(url).content)
    f.close()


def modalRemove() :
    imgs = getElements('div>div>img')
    for img in  imgs :
        src = img.get_attribute("src")
        if src == 'https://gw.alicdn.com/tfs/TB1q0IgvTmWBKNjSZFBXXXxUFXa-55-55.png' :
            img.click()

def priceAndAmount(path) :
    priceSection = getElement('#mod-detail-price')
    ladder1 = getDriverElements(priceSection, 'td.ladder-3-1')
    ladder2 = getDriverElements(priceSection, 'td.ladder-3-2')
    ladder3 = getDriverElements(priceSection, 'td.ladder-3-3')
    price = ''
    price = price + ladder1[0].text + '\t' +ladder1[1].text + '\r\n'
    price = price + ladder2[0].text + '\t' + ladder2[1].text + '\r\n'
    price = price + ladder3[0].text + '\t' + ladder3[1].text + '\r\n'
    saveFile(path, 'price.txt', price)

def mPriceAndAmount(path) :
    tot = ''
    priceSection = getElement('div.m-detail-price')
    prices = getDriverElement(priceSection, 'dl.d-price-rangecount')
    amounts = getDriverElement(priceSection, 'dl.d-price-discount')
    price = getDriverElements(prices, 'dd')
    amount = getDriverElements(amounts, 'dd')
    tot = tot + price[0].text + '\t' + amount[0].text + '\r\n'
    tot = tot + price[1].text + '\t' + amount[1].text + '\r\n'
    tot = tot + price[2].text + '\t' + amount[2].text + '\r\n'

    saveFile(path, 'price.txt', tot)



def mobileSubMain(url) :
    getUrl(url)

    description = getElement('h1.d-title')
    print(description.text)
    ko = translator.translate(description.text, 'zh-CN', 'ko')
    mkdir(ko.text)
    time.sleep(2)
    jqueryScroll(10)

    container = getElement('div.m-detail-description')
    imgs = getDriverElements(container, 'img')
    imgCnt = 1
    for img in imgs :
        src = img.get_attribute('src')
        etc = src[src.rindex("."):len(src)]
        if os.path.isfile(rootPath + '/'+ko.text + '/img' + str(imgCnt) + etc) :
            print('is file')
        else :
            src = img.get_attribute('src')
            saveImage(ko.text, src, str(imgCnt))
            imgCnt = imgCnt + 1
            time.sleep(1)
    time.sleep(2)

    driver.execute_script("$('#J_M_Detail_PageLayoutContent').scrollTop(400)")

    detail_tabs = getElement('div.m-detail-tabs')
    tabs = getDriverElements(detail_tabs, 'div.tab-item')
    tabs[1].click()
    container = getElement('div.m-detail-attributes')
    lis = getDriverElements(container, 'li')
    detail_ko = ''
    detail_cn = ''
    for li in lis :
        name = getDriverElement(li, 'span.name').text
        prop = getDriverElement(li, 'span.property').text

        detail_cn = detail_cn + name + '\t' + prop + '\r\n'

    details = detail_cn.split('\r\n')
    for detail in details :
        des = detail.split('\t')
        loopCnt = 1
        for de in des :
            try :
                print(de)
                trans = translator.translate(de, 'zh-CN', 'ko')
                if loopCnt % 2 == 1 :
                    detail_ko = detail_ko + trans.text + ' : '
                else :
                    detail_ko = detail_ko + trans.text
                loopCnt = loopCnt + 1
            except Exception :
                print('translate error')
        detail_ko = detail_ko + '\r\n'

    detail_cn = detail_cn.replace(' ', '\t')
    saveFile(ko.text, 'detail.txt', detail_ko + '\r\n\r\n\r\n\r\n\r\n' + detail_cn)
    saveFile(ko.text, 'url.txt', url)
    mPriceAndAmount(ko.text)


def subMain(url) :
    getUrl(url)

    description = getElement('h1.d-title')
    print(description.text)
    ko = translator.translate(description.text, 'zh-CN', 'ko')
    mkdir(ko.text)
    time.sleep(2)
    scroll(5)

    try :
        click('#sufei-dialog-close')
    except Exception as e :
        print(e)
    # 상세정보추출
    time.sleep(1)

    container = getElement('div.de-description-detail')
    imgs = getDriverElements(container, 'img')
    imgCnt = 1
    # 이미지추출
    for img in imgs :
        src = img.get_attribute('src')
        etc = src[src.rindex("."):len(src)]
        if os.path.isfile(rootPath + '/'+ko.text + '/img' + str(imgCnt) + etc) :
            print('is file')
        else :
            src = img.get_attribute('src')
            saveImage(ko.text, src, str(imgCnt))
            imgCnt = imgCnt + 1
            time.sleep(1)
    time.sleep(2)

    driver.execute_script("window.scrollBy(0, -100000)")
    driver.execute_script("window.scrollBy(0, 400)")


    d_content = getElement('div.mod-detail-attributes')
    driverClick(d_content, '.obj-expand')

    trs = getDriverElements(d_content, 'tr')
    detail_ko = ''
    detail_cn = ''
    for tr in trs :
        print(tr.text)
        detail_cn = detail_cn + tr.text + '\r\n'

    details = detail_cn.split('\r\n')
    for detail in details :
        des = detail.split(' ')
        loopCnt = 1
        for de in des :
            try :
                print(de)
                trans = translator.translate(de, 'zh-CN', 'ko')
                if loopCnt % 2 == 1 :
                    detail_ko = detail_ko + trans.text + ' : '
                else :
                    detail_ko = detail_ko + trans.text
                loopCnt = loopCnt + 1
            except Exception :
                print('translate error')
        detail_ko = detail_ko + '\r\n'

    detail_cn = detail_cn.replace(' ', '\t')
    saveFile(ko.text, 'detail.txt', detail_ko + '\r\n\r\n\r\n\r\n\r\n' + detail_cn)
    saveFile(ko.text, 'url.txt', url)
    priceAndAmount(ko.text)


class gui() :
    def __init__(self):
        self.root = Tk()
        self.root.title('1688 이미지 추출')
        self.lbl = Label(self.root, text="chromeDriver")
        self.lbl.grid(row=0, column=0)
        self.entryText = StringVar()
        self.txt = Entry(self.root, width=50, textvariable=self.entryText)
        self.txt.grid(row=0, column=1)
        self.lbl2 = Label(self.root, text="imageSavePath")
        self.lbl2.grid(row=1, column=0)
        self.entryText2 = StringVar()
        self.txt2 = Entry(self.root, width=50, textvariable=self.entryText2)
        self.txt2.grid(row=1, column=1)
        self.lbl3 = Label(self.root, text="Desktop URL")
        self.lbl3.grid(row=2, column=0)
        self.entryText3 = StringVar()
        self.txt3 = Entry(self.root, width=50,textvariable=self.entryText3)
        self.txt3.grid(row=2, column=1)
        self.txt3.bind("<FocusIn>", self.txt3Callback) #keyup
        self.lbl4 = Label(self.root, text="Mobile URL")
        self.lbl4.grid(row=3, column=0)
        self.entryText4 = StringVar()
        self.txt4 = Entry(self.root, width=50, textvariable=self.entryText4)
        self.txt4.grid(row=3, column=1)
        self.txt4.bind("<FocusIn>", self.txt4Callback) #keyup
        self.btn = Button(self.root, text="추출", width=15, command=self.okClick)
        self.btn.grid(row=4, column=1)
        with open('config.properties') as fp:
            properties = jprops.load_properties(fp)
            self.entryText.set(properties.get('chromeDriverPath'))
            self.entryText2.set(properties.get('saveImagePath'))
        self.root.mainloop()

    def txt3Callback(self, event):
        self.entryText4.set('')

    def txt4Callback(self, event):
        self.entryText3.set('')

    def okClick(self) :

        self.btn.configure(state=DISABLED)
        global rootPath
        rootPath = self.txt2.get()
        openDriver(self.txt.get())
        url = self.txt3.get()
        if url == '' :
            url = self.txt4.get()
            mobileSubMain(url)
        else :
            subMain(url)

        self.btn.configure(state=NORMAL)
        driver.close()
gui()
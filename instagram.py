import os
import time
from io import BytesIO
import jprops
from tkinter import *
from tkinter.ttk import Separator
from selenium import webdriver
from PIL import Image

class Instagram :
    def __init__(self):
        self.gui()

    def gui(self):
        self.root = Tk()
        self.root.title("Instagram Crawling")
        self.root.resizable(False, False)
        # 크롬 드라이버 설정
        self.chromelbl = Label(self.root, text="크롬드라이버 경로")
        self.chromelbl.grid(row=0, column=0, columnspan=3)

        self.chromedriver = StringVar()
        self.chrome = Entry(self.root, width=60, textvariable=self.chromedriver)
        self.chrome.grid(row=1, column=0, columnspan=3)
        # 이미지 저장경로
        self.imglbl = Label(self.root, text="저장할 이미지 경로")
        self.imglbl.grid(row=2, column=0, columnspan=3)

        self.img = StringVar()
        self.imgPath = Entry(self.root, width=60, textvariable=self.img)
        self.imgPath.grid(row=3, column=0, columnspan=3)

        # url 입력
        self.urllbl = Label(self.root, text="인스타그램 URL")
        self.urllbl.grid(row=4, column=0, columnspan=3)

        self.url = StringVar()
        self.webUrl = Entry(self.root, width=60, textvariable=self.url)
        self.webUrl.grid(row=5, column=0,columnspan=3)

        # feed 시작점
        self.feedlbl = Label(self.root, text="시작할 피드번호")
        self.feedlbl.grid(row=6, column=0, columnspan=3)

        self.feed = StringVar()
        self.feeds = Entry(self.root, width=60, textvariable=self.feed)
        self.feeds.grid(row=7, column=0,columnspan=3)

        # radio BUtton
        self.sep = Separator(self.root, orient="horizontal")
        self.sep.grid(row=8, column=0,columnspan=3)

        self.option = IntVar()
        self.R1 = Radiobutton(self.root, text="모든피드 다운로드", variable=self.option, value=1, command=self.radioSelection)
        self.R1.grid(row=9,  column =0)
        # R1.pack( anchor = W )

        self.R2 = Radiobutton(self.root, text="피드 다운로드", variable=self.option, value=2, command=self.radioSelection)
        # R2.pack( anchor = W )
        self.R2.grid(row=9, column =2)

        self.btn = Button(self.root, text="추출", width=15,command=self.clickEvent)
        self.btn.grid(row=10, column=0, columnspan=3)

        with open('config.properties') as fp:
            properties = jprops.load_properties(fp)
            self.chromedriver.set(properties.get('chromeDriverPath'))
            self.img.set(properties.get('saveImagePath'))
            self.option.set(1)
            self.feed.set(1)

        self.root.mainloop()

    def valid(self):
        chrome = self.chromedriver.get()
        img = self.img.get()
        url = self.url.get()
        option = self.option.get()
        flag = True
        if chrome == '' :
            flag= False
        if img == '' :
            flag= False
        if url == '' :
            flag= False
        if option == '' :
            flag= False
        return flag

    def clickEvent(self):
        if(self.valid()) :
            self.connect()
            self.movePage()
            if(self.option.get() == 1) :
                self.main()
            else :
                self.sub()

    def radioSelection(self) :
        self.option.set(self.option.get())

    def connect(self) :
        global rootPath
        rootPath = self.img.get()
        global driver
        driver = webdriver.Chrome(self.chromedriver.get())

    def movePage(self) :
        driver.get(self.url.get())

    def main(self) :
        global feedCnt
        feedCnt = 1
        scroll(1)
        feeds = getElements("div.v1Nh3")
        for feed in feeds :
            startFeedCnt = self.feed.get()
            if feedCnt >= int(startFeedCnt) :
                getElementCus(feed, 'a').click()
                sleep(1)
                # 모달선택
                modal = getElement('div._2dDPU')
                # 상세정보 출력
                detail_wrap = getElementCus(modal, 'div.C7I1f')
                detail = getElementCus(detail_wrap, 'span').text
                strs = detail.split('\n')
                current_path = strs[0]
                mkDir(current_path)
                fileSaveStr(current_path, detail)
                # 이미지 태그
                lis = getElementsCus(modal, 'li._-1_m6')
                imgCnt = 1
                for li in lis :
                    if os.path.isfile(rootPath + '/' + str(feedCnt)+ '.'+current_path + '/'+'img' + str(imgCnt) +".png") :
                        print('파일존재함')
                    else :
                        img = getElementCus(li, 'img')
                        src = img.get_attribute("src")
                        # 이미지 새탭으로 호출
                        newTab(src)
                        fileSaveImg(current_path, imgCnt)
                        closeTab(0)
                    imgCnt = imgCnt + 1
                    try :
                        getElementCus(modal, 'div.coreSpriteRightChevron').click()
                    except Exception:
                        print('lastImage')
                getElementCus(modal, 'button.ckWGn').click()
            feedCnt = feedCnt + 1
        driver.close()

    def sub(self):
        global feedCnt
        feedCnt = 9999
        # 상세정보 출력
        detail_wrap = getElement('div.C7I1f')
        detail = getElementCus(detail_wrap, 'span').text
        strs = detail.split('\n')
        current_path = strs[0]
        mkDir(current_path)
        fileSaveStr(current_path, detail)
        # 이미지 태그
        lis = getElements('li._-1_m6')
        imgCnt = 1
        for li in lis :
            if os.path.isfile(rootPath + '/' + str(feedCnt)+ '.'+current_path + '/'+'img' + str(imgCnt) +".png") :
                print('파일존재함')
            else :
                img = getElementCus(li, 'img')
                src = img.get_attribute("src")
                # 이미지 새탭으로 호출
                newTab(src)
                fileSaveImg(current_path, imgCnt)
                closeTab(0)
            imgCnt = imgCnt + 1
            try :
                getElement('div.coreSpriteRightChevron').click()
            except Exception:
                print('lastImage')
        driver.close()

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

def fileSaveImg(path, imgCnt) :
    imgElement = getElement('img')
    location = imgElement.location
    size = imgElement.size
    # imgDrive.save_screenshot("c:/img/" + path + '/'+'img' + str(imgCnt) + etc)
    png = driver.get_screenshot_as_png()
    im = Image.open(BytesIO(png))

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom))
    im.save(rootPath + '/' + str(feedCnt)+ '.'+path + '/'+'img' + str(imgCnt) +".png", "PNG")

def fileSaveStr(path, var) :
    f = open(rootPath + '/'+ str(feedCnt) + '.' + path + '/dOri.txt', mode='w', encoding='utf-8')
    f.write(var)
    f.close()

def sleep(sec) :
    time.sleep(sec)

def getElementCus(cus , css_selector):
    return cus.find_element_by_css_selector(css_selector)

def getElement(css_selector) :
    return driver.find_element_by_css_selector(css_selector)

def getElementsCus(cus, css_selector) :
    return cus.find_elements_by_css_selector(css_selector)

def getElements(css_selector) :
    return driver.find_elements_by_css_selector(css_selector)

def scroll(cnt):
    for i in range(cnt):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        sleep(0.3)

def mkDir(directory):
    if os.path.isdir(rootPath) :
        print()
    else :
        os.mkdir(rootPath)
    dic = os.path.join(rootPath, str(feedCnt) + '.'+directory)
    if os.path.isdir(dic) :
        print()
    else :
        os.mkdir(dic)

instagram = Instagram()

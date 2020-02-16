from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import PyQt5.sip
import os
from random import randint

tplt = "%-7s %-7s" # 输出格式
brower=webdriver.Edge()
url='https://www.xuexi.cn/'

# 判定是否有视频
def browerVideo():
    time.sleep(0.5)
    brower.implicitly_wait(15)
    otherPageList= brower.find_elements_by_xpath('//*[@id="6a61"]/div/div/div/div/div/section/div/div/div/div[1]/div[1]/div')
    if len(otherPageList) > 0:
        brower.implicitly_wait(10)
        otherPageList[0].click()
        time.sleep(0.5)
        window = brower.window_handles
        brower.switch_to.window(window[-1])  # 调到新网页
    else :
        print("error!")
        return

    brower.implicitly_wait(10)
    time.sleep(3.5) # 加载网页
    btnList=brower.find_elements_by_class_name('btn')
    totalNumbers=int(btnList[-1].get_attribute('innerText'))-1 # -1是为了防止超出，最多点击tot-1次
    clickNumbers=randint(0,totalNumbers)
    # print(totalNumbers,clickNumbers)
    for i in range(clickNumbers):
        btnList[-2].click()
        time.sleep(0.12)

    totalVideoSum=0
    videoPageList = brower.find_elements_by_class_name('text-wrap')
    for i,videoPage in enumerate(videoPageList):
        print("正在运行第%d个视频" % (i+1))
        videoPage.click()
        time.sleep(0.5)
        brower.implicitly_wait(5)
        window = brower.window_handles
        brower.switch_to.window(window[-1])  # 调到新网页
        time.sleep(3) # 加载新网页
        brower.implicitly_wait(5)

        video = brower.find_elements_by_class_name('outter')
        if len(video) > 0:
            for j in range(len(video)):
                # 获取有效时间
                video_duration_str = brower.find_element_by_xpath("//span[@class='duration']").get_attribute(
                    'innerText')
                video_duration = int(video_duration_str.split(':')[0]) * 60 + int(video_duration_str.split(':')[1])

                time.sleep(0.5)
                print("这个视频共有%d秒" %(video_duration),end=',')
                brower.execute_script('window.scrollTo(0,' + str(400) + ')')

                #根据探索，低于180s的视频观看不算有效阅读
                if video_duration <180:
                    print("时间过短，跳过")
                else :
                    print("时间合适，运行有效时间180s")
                    js = 'document.getElementsByTagName("video")[0].muted = true;'  # 静音操作
                    brower.execute_script(js)
                    time.sleep(min(video_duration + 3, 183))
                    totalVideoSum+=1
                    print("有效观看%d个视频\n" % (totalVideoSum))

        brower.close()
        window = brower.window_handles
        brower.switch_to.window(window[-1])  # 退回到视频列表页

        if totalVideoSum >6:
            print("已有效观看6个以上视频，无需多观看...")
            break

    print("有效视频观看结束...")
    brower.close()
    window = brower.window_handles
    brower.switch_to.window(window[-1])  # 退回到主页

# 动态下滑上滑
def UpAndDown():
    brower.implicitly_wait(5)
    time.sleep(2) # 等待页面加载完毕
    mainWindow = brower.find_element_by_class_name('main-view') # 获取高度
    height = mainWindow.size['height']

    #将视频静音
    video = brower.find_elements_by_class_name('outter')
    if len(video)>0 :
        js = 'document.getElementsByTagName("video")[0].muted = true;'
        brower.execute_script(js)

    cnt = 0
    flag = True
    for j in range(7):
        for i in range(50):
            if flag:
                cnt += i * 5
                if cnt>height:
                    cnt=height
                    flag=False
            else:
                cnt -= i * 5
                if cnt<0:
                    cnt=0
                    flag=True

            brower.execute_script('window.scrollTo(0,' + str(cnt) + ')')
            time.sleep(0.275)

#浏览网页
def browerPages():
    print("请输入查看网页标题的关键字:", end='')
    mystr = str(input())
    print("等待5s网页加载...", end=' ')
    brower.implicitly_wait(10)
    time.sleep(5)
    print("...")
    text = brower.find_elements_by_xpath("//span[contains(text(),'%s')]" % str(mystr))
    print("这次程序将运行总共有" + str(min(len(text),10)) + "个含有“%s“标题关键字的网页" % str(mystr))
    # 浏览网页
    for i in range(min(len(text),10)):
        print("正在运行第" + str(i + 1) + "个网页----->网页标题:" + str(text[i].text))
        time.sleep(1)
        brower.implicitly_wait(5)
        text[i].click() # 点开新网页
        brower.implicitly_wait(5)
        window = brower.window_handles
        brower.switch_to.window(window[1]) # 调到新网页
        brower.implicitly_wait(5)
        UpAndDown() # 上下滑动
        brower.close() #关闭这一新开的网页
        window = brower.window_handles
        brower.switch_to.window(window[0]) # 回到主页

# 判断网页登录情况
def judgeLogin():
    time.sleep(3) # 睡眠3s 加载网页
    brower.implicitly_wait(5)
    mySpan=brower.find_elements_by_class_name('logged-text')
    if len(mySpan) != 0:
        return True
    else :
        return False

def login():
    time.sleep(3)
    brower.implicitly_wait(5)
    btn_login=brower.find_elements_by_class_name('login-icon')
    btn_login[0].click()
    time.sleep(3)
    window = brower.window_handles
    brower.switch_to.window(window[1])  # 调到新网页
    mainWindow = brower.find_element_by_id('app')  # 获取高度
    height = mainWindow.size['height']

    brower.execute_script('window.scrollTo(0,' + str(height) + ')')
    print("网页保持15s，请不用关闭网页，扫描完成后会自动进行")
    time.sleep(15)  # 睡眠15s 加载网页

    brower.close()  # 关闭这一新开的网页
    window = brower.window_handles
    brower.switch_to.window(window[0])  # 回到主页

# 查看得分情况
def getScore():
    time.sleep(0.5)
    items=brower.find_elements_by_class_name('linkItem') # 查找link列表
    for item in items:
        if item.get_attribute('innerText') == '我的积分':  # 具体选项
            item.click()
            break

    window = brower.window_handles
    brower.switch_to.window(window[-1])  # 进入新网页
    time.sleep(3) # 睡眠加载网页信息
    brower.implicitly_wait(10)

    scoreList = {}
    sumScore = 0

    sumScore = int(brower.find_elements_by_class_name('my-points-points')[1].get_attribute('innerText'))
    titles = brower.find_elements_by_class_name('my-points-card-title')
    titleScores = brower.find_elements_by_class_name('my-points-card-text')

    for i,title in enumerate(titles):
        title_str=title.get_attribute('innerText')
        titleScore_str=titleScores[i].get_attribute('innerText')
        scoreList.setdefault(title_str,titleScore_str)

    brower.close()
    window = brower.window_handles
    brower.switch_to.window(window[0])  # 回到主页

    return sumScore,scoreList

if __name__ == '__main__':
    try:
        brower.implicitly_wait(10)
        print("**正在检查网页登录情况**")
        brower.get(url=url)  # 打开网页
        while not judgeLogin(): # 循环检查
            print("----->未登录<-----")
            login()
            time.sleep(0.5)
            brower.refresh() # 刷新页面
            time.sleep(0.5)
        print("----->Login Successful<-----\n")

        print("第一阶段-->浏览网页 共12分")
        browerPages()
        print("\n")

        print("第二阶段-->浏览视频 共12分")
        browerVideo()
        print("\n")

        sumScore,scoreList=getScore()
        print("查看今日得分:%d" % (sumScore))
        print("%-7s  %-7s" % ('加分项名称','已加分/可加分'))
        for scoreItem in scoreList.keys():
            print("%-7s  %-7s" % (scoreItem,scoreList[scoreItem]))

        print('')
        print("Finish!")
        time.sleep(5.5)
    finally:
        brower.close()
        os.system('pause') # 按键退出

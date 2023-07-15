from tkinter import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

root = Tk()
root.title("출첵")
#root.geometry("640x480")   # 가로 x 세로
# root.geometry("435x240-2770-330")    # 가로 x 세로 + x좌표 + y좌표, 사이트2개
root.geometry("435x350-2770-330")    # 가로 x 세로 + x좌표 + y좌표, 사이트3개

# root.resizable(False, False)    # x(너비), y(높이) 창크기 변경 불가

def inven():
    # print("inven att")
    options = Options()
    options.add_argument("headless") #크롬창이 뜨지 않고 백그라운드로 동작됨
    
    # config.json 파일처리 ----------------
    with open('config.json','r') as f:
        config = json.load(f)
    url1 = config['SITE1']['URL1']
    url2 = config['SITE1']['URL2']
    user_id = config['SITE1']['ID']
    password = config['SITE1']['PASSWORD']
    # ------------------------------------
    # print(user_id)
    # print(password)
    # print(url1)
    # print(url2)
    driver = webdriver.Chrome(options=options)
    
    # 인벤 초화면 진입
    driver.get(url1)
    #driver.maximize_window()
    action = ActionChains(driver)

    time.sleep(1)
    # 로그인 버튼 클릭
    driver.find_element(By.CLASS_NAME, "login-btn").click()
    time.sleep(1)
    # ID/Passwd 입력하고 로그인 버튼 클릭
    driver.find_element(By.ID, "user_id").send_keys(user_id)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "loginBtn").click()
    time.sleep(1)

    # time.sleep(300)
    # 로그인 보상 받고 뜨는 팝업 내용 확인하기
    try:
        # print("try....")
        # //*[@id="myModal"]/div/div/div[2]/span        # XPATH
        # //*[@id="myModal"]/div/div/div[2]/strong      # XPATH
        # /html/body/div[4]/div/div/div/div[2]/span     # Full XPATH    이번사례는 XPATH로 실패하고 Full XPATH로 성공했음
        # /html/body/div[4]/div/div/div/div[2]/strong   # Full XPATH

        # login_text1 = driver.find_element(By.XPATH, '//*[@id="myModal"]/div/div/div[2]/span').text
        # login_text2 = driver.find_element(By.XPATH, '//*[@id="myModal"]/div/div/div[2]/strong').text

        login_text1 = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[2]/span')
        login_text2 = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[2]/strong')
        # 불로소득으로 login_text1 적립, 인증보너스로 login_text2 적립
        # print(login_text1)
        # print(login_text1.text)
        # print(login_text2)
        # print(login_text2.text)
        # print("try... 2") # 이게 안찍히면 여기까지 못오고 에러났다는 의미임.

        entry_inven3.delete(0, END)
        entry_inven3.insert(0, "불로소득: (" + login_text1.text + "), 인증보너스: (" + login_text2.text + ")")
        result_txt = "불로소득: (" + login_text1.text + "), 인증보너스: (" + login_text2.text + ")"
        # print("try... end") # 이게 안찍히면 여기까지 못오고 에러났다는 의미임.
    except:
        # print("no login_text")
        login_text1 = "로그인 보상 없음 (이미 받았음)"

        entry_inven3.delete(0, END)
        entry_inven3.insert(0, login_text1)
        result_txt = login_text1

    # 출첵 화면으로 이동
    driver.get(url2)
    
    time.sleep(1)

    # Before Count 표시
    att_count1 = driver.find_element(By.CLASS_NAME, "countNum").text
    # print(att_count1)
    entry_inven1.delete(0, END)
    entry_inven1.insert(0, att_count1)
    
    # 출첵 도장찍기 버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="invenAttendCheck"]/div/div[2]/div/div[3]/div[1]/div[4]/a').click()
    try:
        time.sleep(1)
        result = driver.switch_to.alert     # alert 창 정보 가져오기
        # print(result.text.replace("(0001)",""))
        entry_inven3.delete(0, END)
        entry_inven3.insert(0, result.text.replace("(0001)",""))
        
        # alert 창 확인
        result.accept()

        # alert 창 끄기
        # result.dismiss()
    except:
        pass
        # print("no alert")

    # After Count 표시
    att_count2 = driver.find_element(By.CLASS_NAME, "countNum").text
    # print(att_count2)
    entry_inven2.delete(0, END)
    entry_inven2.insert(0,att_count2)

    time.sleep(2)
    driver.quit()

    # result_inven = {
    #     'count1': att_count1,
    #     'count2': att_count2,
    #     'txt': result_txt
    # }
    # return(result_inven)

def avsubs():
    # print("inven att")
    options = Options()
    options.add_argument("headless") #크롬창이 뜨지 않고 백그라운드로 동작됨
    
    # headless로 동작할때 element를 못찾으면 아래 두줄 추가
    options.add_argument("start-maximized")
    options.add_argument("window-size=1920,1080")

    # options.add_argument("start-maximized");
    # options.add_argument("disable-infobars")
    # options.add_argument("--disable-extensions")

    # config.json 파일처리 ----------------
    with open('config.json','r') as f:
        config = json.load(f)
    url1 = config['SITE2']['URL1']
    url2 = config['SITE2']['URL2']
    user_id = config['SITE2']['ID']
    password = config['SITE2']['PASSWORD']
    # ------------------------------------
    # print(user_id)
    # print(password)
    # print(url1)
    # print(url2)
    driver = webdriver.Chrome(options=options)

    # AVSUBS 초화면 진입
    driver.get(url1)
    #driver.maximize_window()
    action = ActionChains(driver)

    time.sleep(1)
    # 로그인 버튼 클릭
    # driver.find_element(By.XPATH, '//*[@id="thema_wrapper"]/aside/div/div[1]/ul/li[1]/a').click()
    driver.find_element(By.XPATH, '//*[@id="thema_wrapper"]/aside/div/div[1]/ul/li[1]/a').send_keys(Keys.ENTER)
    time.sleep(1)
    # ID/Passwd 입력하고 로그인 버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="mb_id"]').send_keys(user_id)
    driver.find_element(By.XPATH, '//*[@id="mb_password"]').send_keys(password)
    driver.find_element(By.CLASS_NAME, "btn.btn-navy.btn-block").click()
    # time.sleep(10)  # 로그인 누르고 10초 대기
    time.sleep(1)  # 로그인 누르고 10초 대기

    # 출첵 화면으로 이동
    driver.get(url2)
    # time.sleep(15)
    time.sleep(1)

    # 오늘 출석일, 연속일자 Count 표시
    att_count1 = driver.find_element(By.CLASS_NAME, 'pull-left.hidden-xs').text
    # print(att_count1)
    entry_avsubs1.delete(0, END)
    entry_avsubs1.insert(0, att_count1)    

    # 연속일자 Count 표시
    # att_count2 = driver.find_element(By.CLASS_NAME, 'font-13.en.orangered').text
    # print(att_count2)
    # entry_avsubs2.delete(0, END)
    # entry_avsubs2.insert(0, att_count2)

    # 출첵 버튼 누르기
    driver.find_element(By.CLASS_NAME, 'btn.btn-color.btn-lg').click()
    try:
        time.sleep(1)
        result = driver.switch_to.alert
        # print(result.text)
        entry_avsubs3.delete(0, END)
        entry_avsubs3.insert(0, result.text)

        # alert 창 확인
        result.accept()

        # alert 창 끄기
        # result.dismiss()
    except:
        pass
        # print("no alert")


    time.sleep(2)
    driver.quit()

def emart():
    # print("emart function called")
    options = Options()
    # options.add_argument("headless") #크롬창이 뜨지 않고 백그라운드로 동작됨
    
    # config.json 파일처리 ----------------
    with open('config.json','r') as f:
        config = json.load(f)
    url1 = config['SITE3']['URL1']
    url2 = config['SITE3']['URL2']
    user_id = config['SITE3']['ID']
    password = config['SITE3']['PASSWORD']
    # ------------------------------------
    # print(user_id)
    # print(password)
    # print(url1)
    # print(url2)
    driver = webdriver.Chrome(options=options)

    # 이마트 로그인 화면 진입
    driver.get(url1)
    #driver.maximize_window()
    action = ActionChains(driver)

    time.sleep(1)
    # 로그인 버튼 클릭
    # id = userId,userId, loginBtn

    # ID/Passwd 입력하고 로그인 버튼 클릭
    driver.find_element(By.ID, 'userId').send_keys(user_id)
    driver.find_element(By.ID, 'userPw').send_keys(password)
    driver.find_element(By.ID, "loginBtn").click()

    time.sleep(1)
    # 이벤트 페이지 이동
    driver.get(url2)
    # "출석체크" 키워드가 포함된 곳을 클릭하기
    keyword = "출석체크"
    driver.find_element(By.XPATH, "//*[contains(text(),'" + keyword + "')]").click()
    time.sleep(1)
    
    # 출석하기 버튼 클릭
    driver.find_element(By.CLASS_NAME, "type-important.btns-check").click()
    # 여기까지 했는데
    # 이마트앱에서만 참여가 가능합니다.
    # 이마트앱으로 이동하시겠습니까? 라고 나옴.. ㅡ.ㅡ;;;
    time.sleep(5)



    time.sleep(2)
    driver.quit()

# btn_inven1 = Button(root, text="인벤", padx=3, pady=20, command=inven)
# btn_inven1.pack(pady=5)

# label1 = Label(root, text="Before")
# label1.pack(side="left")
# label2 = Label(root, text="After")
# label2.pack(side="right")

# entry_inven1 = Entry(root, width=5)
# entry_inven1.pack(side="left")
# entry_inven2 = Entry(root, width=5)
# entry_inven2.pack(side="right")
# entry_inven3 = Entry(root, width=30)
# entry_inven3.pack(side="bottom", fill="x")

# 인벤 프레임
frame_inven = LabelFrame(root, text="인벤")
frame_inven.pack(side="top", fill="both", expand=True)
btn_inven1 = Button(frame_inven, text="출첵", padx=3, pady=20, command=inven)
btn_inven1.pack(side="left", pady=5)

entry_inven1 = Entry(frame_inven, width=2)
entry_inven1.pack(side="left")
entry_inven2 = Entry(frame_inven, width=2)
entry_inven2.pack(side="left")
entry_inven3 = Entry(frame_inven, width=33)
entry_inven3.pack(side="left")


# Avsubs 프레임
frame_avsubs = LabelFrame(root, text="AVSUBS")
frame_avsubs.pack(side="top", fill="both", expand=True)
btn_avsubs1 = Button(frame_avsubs, text="출첵", padx=3, pady=20, command=avsubs)
btn_avsubs1.pack(side="left", pady=5)

entry_avsubs1 = Entry(frame_avsubs, width=12)
entry_avsubs1.pack(side="left")
# entry_avsubs2 = Entry(frame_avsubs, width=5)
# entry_avsubs2.pack(side="left")
entry_avsubs3 = Entry(frame_avsubs, width=30)
entry_avsubs3.pack(side="left")

# emart 프레임
frame_emart = LabelFrame(root, text="EMART")
frame_emart.pack(side="top", fill="both", expand=True)
btn_emart1 = Button(frame_emart, text="출첵", padx=3, pady=20, command=emart)
btn_emart1.pack(side="left", pady=5)

entry_emart1 = Entry(frame_emart, width=12)
entry_emart1.pack(side="left")
entry_emart3 = Entry(frame_emart, width=30)
entry_emart3.pack(side="left")

root.mainloop()

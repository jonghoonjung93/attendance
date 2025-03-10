# from tkinter import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from datetime import timedelta
import time,datetime
import json
import telegram
import asyncio
import socket
import random
import os

"""
* CSS_SELECTOR, LINK_TEXT 사용방법
driver.find_element(By.CSS_SELECTOR, ".class_name")
driver.find_element(By.CSS_SELECTOR, "#id_name")
driver.find_element(By.CSS_SELECTOR, "[title='title_name']")
driver.find_element(By.CSS_SELECTOR, "[placeholder='placeholder_name']")
driver.find_element(By.LINK_TEXT, "text_name")          # 링크 텍스트 일치
driver.find_element(By.PARTIAL_LINK_TEXT, "text_name")  # 링크 텍스트의 일부분이라도 일치
navs = driver.find_element(By.CSS_SELECTOR, ".nav)
for nav in navs:
    print(nav.get_attribute("outerHTML"))   # 해당 element 의 바깥쪽 HTML을 가져옴

* selenium, soup 콜라보
driver.get(url)
html = driver.page_source   # 이후 Beautifulsoup을 이용해서 속도를 빠르게
"""

def mode_check():
	hostname = socket.gethostname()
	if hostname == 'jungui-MacBookAir.local':
		MODE = "TEST"
	else:
		MODE = "ONLINE"
	return(MODE)

def printL(message):	# 로그파일 기록 함수 (맥북에서는 화면에도 출력)
	log_directory = "logs"
	current_date = datetime.datetime.now().strftime("%Y%m%d")
	log_path = os.path.join(log_directory, f"log.{current_date}")
	current_time = datetime.datetime.now()
	formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

	if mode_check() == 'TEST':
		print(message)
	with open(log_path, "a") as log_file:
		log_file.write(f"{formatted_time} {message}\n")

def inven():
    printL("-- inven att start")
    options = Options()

    # 운영모드 체크
    if mode_check() == 'TEST':
        # options.add_argument("headless") #크롬창이 뜨지 않고 백그라운드로 동작됨
        pass
    else:
        options.add_argument("headless") #크롬창이 뜨지 않고 백그라운드로 동작됨
                
    # 아래 옵션 두줄 추가(NAS docker 에서 실행시 필요, memory 부족해서)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
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
    try:
        driver.find_element(By.ID, 'btn-extend').click()    # 다음에 변경하기 3개월 (비밀번호 변경주기 도달시에 눌러줘야 넘어감)
    except:
        pass
    else:   # 다음에 변경하기 눌렀을 경우
        time.sleep(1)
    # time.sleep(1000)

    # 로그인 보상 받고 뜨는 팝업 내용 확인하기
    try:    # 이미 보상받은 경우에는 element 가 없기때문에 try 사용
        login_full = driver.find_element(By.XPATH, '//*[@id="myModal"]/div/div/div[2]')
        # print("login_full = " + login_full.text)
        result_txt = login_full.text
    except Exception as e:
        # print("1.An error occurred:", str(e))
        # print("no login_text")
        login_text1 = " 로그인 보상 없음 (이미 받았음)"
        result_txt = login_text1

    # 출첵 화면으로 이동
    driver.get(url2)
    
    time.sleep(1)

    # Before Count 표시
    att_count1 = driver.find_element(By.CLASS_NAME, "countNum").text
    # print(att_count1)
    # entry_inven1.delete(0, END)
    # entry_inven1.insert(0, att_count1)
    
    # 출첵 도장찍기 버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="invenAttendCheck"]/div/div[2]/div/div[3]/div[1]/div[4]/a').click()
    try:
        time.sleep(1)
        result = driver.switch_to.alert     # alert 창 정보 가져오기
        # print(result.text.replace("(0001)",""))
        # entry_inven3.delete(0, END)
        # entry_inven3.insert(0, result.text.replace("(0001)",""))
        
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
    # entry_inven2.delete(0, END)
    # entry_inven2.insert(0,att_count2)

    benny = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[3]/div[2]/p[4]').text
    result_txt = result_txt + "\n " + benny
    # print(benny)

    time.sleep(2)
    driver.quit()

    result_inven = {
        'count1': att_count1,
        'count2': att_count2,
        'txt': result_txt
    }
    return(result_inven)

def subs():
    printL("-- subs att start")
    options = Options()

    # 운영모드 체크
    if mode_check() == 'TEST':
        # options.add_argument("headless") #크롬창이 뜨지 않고 백그라운드로 동작됨
        pass
    else:
        options.add_argument("headless") #크롬창이 뜨지 않고 백그라운드로 동작됨

    # headless로 동작할때 element를 못찾으면 아래 두줄 추가 (창크기가 작아서 못찾을수 있음)
    options.add_argument("start-maximized")
    options.add_argument("window-size=1300,1300")

    # 아래 옵션 두줄 추가(NAS docker 에서 실행시 필요, memory 부족해서)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("disable-gpu")
    # options.add_argument("lang=ko_KR")

    # 아래는 headless 크롤링을 막아놓은곳에 필요 (user agent에 HeadlessChrome 이 표시되는걸 방지)
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')

    # config.json 파일처리 ----------------
    with open('config.json','r') as f:
        config = json.load(f)
    url1 = config['SITE2']['URL1']
    url2 = config['SITE2']['URL2']
    url3 = config['SITE2']['URL3']
    url4 = config['SITE2']['URL4']
    url5 = config['SITE2']['URL5']
    url6 = config['SITE2']['URL6']
    url7 = config['SITE2']['URL7']
    url8 = config['SITE2']['URL8']
    user_id = config['SITE2']['ID']
    password = config['SITE2']['PASSWORD']
    reply = config['SITE2']['REPLY']
    # ------------------------------------
    # print(user_id)
    # print(password)
    # print(url1)
    # print(url2)
    driver = webdriver.Chrome(options=options)
    
    # SUBS 초화면 진입 (timeout 에 대비한 재시도 처리, 아직 검증안됐음)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            driver.get(url1)
            printL(f"connect 명령종료 : {url1}")
            time.sleep(2)
            # printL(f"{driver.find_element(By.ID, 'cf-error-details').text}")
            healthcheck = driver.find_element(By.CLASS_NAME, 'header-icon')
            # printL(healthcheck)
            printL(f"접속 성공~! : {url1}")
            break
        except:
            printL(f"failed. retry...{attempt+1}")
            if attempt == 2:    #3회 재시도후 실패시
                result_subs = {
                    'count1': 0,
                    'txt': "ERROR"   # 에러종료처리
                }
                return(result_subs)


    #driver.maximize_window()
    action = ActionChains(driver)

    # 로그인 버튼 클릭
    # driver.find_element(By.XPATH, '//*[@id="thema_wrapper"]/aside/div/div[1]/ul/li[1]/a').click()
    driver.find_element(By.XPATH, '//*[@id="thema_wrapper"]/aside/div/div[1]/ul/li[1]/a').send_keys(Keys.ENTER)
    time.sleep(1)
    # ID/Passwd 입력하고 로그인 버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="mb_id"]').send_keys(user_id)
    driver.find_element(By.XPATH, '//*[@id="mb_password"]').send_keys(password)
    driver.find_element(By.CLASS_NAME, 'attend-me').click() # 자동출석 체크 제거 (수동출석 하기 위해)
    driver.find_element(By.CLASS_NAME, "btn.btn-navy.btn-block").click()
    # time.sleep(10)  # 로그인 누르고 10초 대기
    time.sleep(1)  # 로그인 누르고 10초 대기

    # --------- 출첵 기능 --------
    printL(f"출첵 시작... {url2}")
    driver.get(url2)
    time.sleep(10)
    # time.sleep(1)

    # 출첵 버튼 누르기
    driver.find_element(By.CLASS_NAME, 'btn.btn-color.btn-lg').click()
    try:
        time.sleep(5)
        result = driver.switch_to.alert
        time.sleep(2)
        printL(f"result.txt = {result.text}")
        result_txt = result.text

        # alert 창 확인
        result.accept()

        # alert 창 끄기
        # result.dismiss()
    except Exception as err:    # 이미 출석했을때는 alert이 뜨는데, 출첵성공때는 안뜬다. 그래서 출첵성공시 여기로...
        result_txt = "출첵 성공"
        printL(f"{result_txt}")
    
    # 오늘 출석일, 연속일자 Count 표시
    att_count1 = driver.find_element(By.CLASS_NAME, 'pull-left.hidden-xs').text

    # 사이드바에서 레벨,Exp,MP 가져오기
    driver.find_element(By.XPATH, '/html/body/div[1]/aside/div/div[1]/ul/li[1]/a/b').click()
    time.sleep(1)
    level = driver.find_element(By.XPATH, '//*[@id="sidebar-user"]/div[1]/div[3]').text
    mp = driver.find_element(By.XPATH, '//*[@id="sidebar-user"]/div[1]/div[6]/ul/li[1]/a/span').text
    level = level.replace("\r", "").replace("\n", " ")  # 변수중간에 엔터값 지우기
    levelmp = f"{level}\n MP: {mp}"
    # print(levelmp)
    result_txt = f"{result_txt}\n {levelmp}"

    # ---- 게시판 (조회 bot) ----
    def board_read(board, content):
        printL(f"{content} 게시판 조회 시작... {board}")
        driver.get(board)
        time.sleep(3)

        # 어제 날짜 mm.dd 로 만들기
        today = datetime.datetime.now().date()
        yesterday = today - timedelta(days=1)
        yesterday_str = yesterday.strftime("%m.%d")

        # 목록에서 어제자만 추출
        list_yesterday_href = []
        lists = driver.find_element(By.CLASS_NAME, 'list-body').find_elements(By.CLASS_NAME, 'list-item')
        for list in lists:
            list_date = list.find_element(By.CLASS_NAME, 'wr-date.hidden-xs').text
            list_href = list.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if list_date == yesterday_str:  # 어제자 컨텐츠만 표시
                list_yesterday_href.append(list_href)
        
        printL(f"읽기 목록 : {len(list_yesterday_href)}개")
        
        # 어제자 링크를 추출한 list 를 하나씩 조회 (어제자 없으면 그냥 넘어감)
        for list2 in list_yesterday_href:
            printL(f"{list2}")
            driver.get(list2)
            time.sleep(3)
    
        return_txt = f"{content}({yesterday_str}) : {str(len(list_yesterday_href))}개"
        return(return_txt)
    
    result_url3 = board_read(url3, "AI")    # AI 게시판 조회
    result_txt = f"{result_txt}\n {result_url3}"    # AI 게시판 결과내용 추가
    result_url8 = board_read(url8, "스포츠")    # 스포츠 게시판 조회
    result_txt = f"{result_txt}\n {result_url8}"    # 스포츠 게시판 결과내용 추가

    #----- subs 게시판 (리플달기) -----#
    def subs_comment(subs_url):
        printL(f"subs 게시판 시작... {subs_url}")
        today = datetime.datetime.now().date()
        yesterday = today - timedelta(days=1)
        yesterday_str_yyyymmdd = yesterday.strftime("%Y.%m.%d")
        # 유저 게시판 이동
        driver.get(subs_url)
        list_yesterday_href = []
        lists = driver.find_elements(By.CLASS_NAME, 'list-row')
        for list in lists:
            list_date = list.find_element(By.CLASS_NAME, 'wr-date.en').text
            list_href = list.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if list_date == yesterday_str_yyyymmdd:
                list_yesterday_href.append(list_href)
            # print(f"{list_date}, {list_href}")

        printL(f"yesterday : {len(list_yesterday_href)}개")
        for list_href in list_yesterday_href:
            printL(f"{list_href}") 
            driver.get(list_href)
            time.sleep(5)
            random_content = random.choice(reply)
            driver.find_element(By.ID, 'wr_content').send_keys(random_content)  #리플 달기
            time.sleep(1)
            driver.find_element(By.ID, 'btn_submit').click()
            time.sleep(32)
        printL(f"리플 {len(list_yesterday_href)}개 완료 ({subs_url})")

        return(len(list_yesterday_href))
    
    #----- 투표 게시판 (투표하기) -----#
    def poll_click(poll_url):
        printL(f"poll 게시판 시작... {poll_url}")
        today = datetime.datetime.now().date()
        yesterday = today - timedelta(days=1)
        yesterday_str_mmdd = yesterday.strftime("%m.%d")
        # 투표 게시판 이동
        try:
            driver.get(poll_url)
            printL("poll 게시판 접속성공")
        except TimeoutException:
            printL(f'poll 게시판 진입시 TimeoutException 발생, continue...')
            return("poll failed (timeout)")
        except Exception as e:
            printL(f'poll 게시판 진입시 알수없는 에러 발생 : ({e})')
            return("poll failed (error)")
        time.sleep(2)
        list_yesterday_href = []
        try:    # 여기서 에러난것 같음. 에러내용확인 처리 필요
            lists_poll = driver.find_element(By.CLASS_NAME, 'list-body').find_elements(By.CLASS_NAME, 'list-item')
        except Exception as e:
            printL(f'poll 게시판 진입후 find_element 에서 에러 발생 : ({e})')
            return("poll find_element fail (error)")
        for list_item in lists_poll:
            list_date = list_item.find_element(By.CLASS_NAME, 'wr-date.hidden-xs').text
            list_href = list_item.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if list_date == yesterday_str_mmdd:  # 어제자 컨텐츠만 표시
                list_yesterday_href.append(list_href)
            # print(f"{list_date}, {list_href}")

        printL(f"투표 목록 : {len(list_yesterday_href)}개")
        poll_success = 0
        for list_href in list_yesterday_href:
            printL(f"{list_href}") 
            try:
                driver.get(list_href)
            except TimeoutException:
                printL(f'TimeoutException 발생, continue...')
                continue
            except Exception as e:
                printL(f'알수없는 에러 발생 : ({e})')
                continue
            time.sleep(7)
            poll_txt = ""
            # radio 버튼 클릭
            try:
                driver.find_element(By.CLASS_NAME, 'list-group').find_element(By.TAG_NAME, 'input').click()
                printL("radio click 성공")
                # poll_success = poll_success + 1
                time.sleep(3)
            except:
                printL("radio click 실패")
            try:
                driver.find_element(By.CLASS_NAME, 'btn.btn-crimson').click()
                printL("설문참여 클릭 성공")
            except:
                printL("설문참여 클릭 실패. 설문조사 종료 확인 필요")
            time.sleep(4)
            try:
                poll_button_result = driver.switch_to.alert
                poll_txt = poll_button_result.text
            except:
                printL("alert 읽기 실패")
            printL(f"alert message : {poll_txt}")
            if poll_txt == "참여에 감사드립니다." or poll_txt == "이미 참여하셨습니다.":
                poll_success = poll_success + 1
            time.sleep(3)
            try:
                poll_button_result.accept()
            except:
                pass
            time.sleep(5)
        printL(f"투표 {poll_success}/{len(list_yesterday_href)}개 완료 ({poll_url})")

        # return(poll_success)
        return(f"{poll_success}/{len(list_yesterday_href)}개")

    # 하루 한번만 수행되도록, 중복되지 않도록 처리
    try:
        with open('last_execution.json', 'r') as file:
            data = json.load(file)
            last_execution_date = datetime.datetime.strptime(data['last_execution'], '%Y-%m-%d').date()
    except (FileNotFoundError, json.JSONDecodeError):
        # File not found or invalid data, set last_execution_date to None
        last_execution_date = None

    # Get the current date
    current_date = datetime.date.today()

    # Check if the current date is different from the last execution date
    if last_execution_date != current_date:
        # Update the last execution date to the current date
        last_execution_date = current_date
        # Save the last execution date to a file
        with open('last_execution.json', 'w') as file:
            data = {'last_execution': str(last_execution_date)}
            json.dump(data, file)

        # Perform the action that should be executed once a day
        printL("subs 게시판 리플 하루 한번만 수행되는 부분 실행")
        subs_count4 = subs_comment(url4)  # 마스터 subs 게시판 리플 달기
        subs_count5 = subs_comment(url5)  # 대작가 subs 게시판 리플 달기
        subs_count6 = subs_comment(url6)  # 유저 subs 게시판 리플 달기
        result_txt = f"{result_txt}\n Subs comment: ({subs_count4},{subs_count5},{subs_count6})개"
        printL(f"Subs comment: ({subs_count4},{subs_count5},{subs_count6})개")
    else:
        # The action has already been executed today
        printL("subs 게시판 리플달기는 오늘 이미 한번 실행되었음. pass~")

    poll_count = poll_click(url7)  # 투표 게시판 투표하기
    result_txt = f"{result_txt}\n Poll : {poll_count}"
    printL(f"Poll : {poll_count}")

    # time.sleep(20000)
    #-----------------------------#

    # ---- 다시 프리미엄 게시판으로 이동 (레벨,Exp,MP 재조회를 위해서) ----
    driver.get(url3)
    time.sleep(3)

    # 사이드바에서 레벨,Exp,MP 가져오기
    driver.find_element(By.XPATH, '/html/body/div[1]/aside/div/div[1]/ul/li[1]/a/b').click()
    time.sleep(1)
    level = driver.find_element(By.XPATH, '//*[@id="sidebar-user"]/div[1]/div[3]').text
    mp = driver.find_element(By.XPATH, '//*[@id="sidebar-user"]/div[1]/div[6]/ul/li[1]/a/span').text
    level = level.replace("\r", "").replace("\n", " ")  # 변수중간에 엔터값 지우기
    levelmp = f"{level}\n MP: {mp}"
    # print(levelmp)
    result_txt = f"{result_txt}\n {levelmp}"

    # time.sleep(1000)

    result_subs = {
        'count1': att_count1,   # 연속 출석 count
        'txt': result_txt   # 결과메세지 + level, exp, mp 상태
    }

    time.sleep(2)
    driver.quit()

    return(result_subs)

def solar():
    printL("-- solar value start")
    options = Options()

    # 운영모드 체크
    if mode_check() == 'TEST':
        # options.add_argument("headless") #크롬창이 뜨지 않고 백그라운드로 동작됨
        pass
    else:
        options.add_argument("headless") #크롬창이 뜨지 않고 백그라운드로 동작됨
                
    # 아래 옵션 두줄 추가(NAS docker 에서 실행시 필요, memory 부족해서)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # config.json 파일처리 ----------------
    with open('config.json','r') as f:
        config = json.load(f)
    url1 = config['SOLAR']['URL1']
    url2 = config['SOLAR']['URL2']
    rec3 = config['SOLAR']['REC3']
    rec4 = config['SOLAR']['REC4']
    # user_id = config['SOLAR']['ID']
    # password = config['SOLAR']['PASSWORD']
    # ------------------------------------
    # print(user_id)
    # print(password)
    # print(url1)
    # print(url2)
    driver = webdriver.Chrome(options=options)
    
    # 전력거래소 사이트 SMP 조회화면 진입
    driver.get(url1)
    #driver.maximize_window()
    action = ActionChains(driver)

    time.sleep(1)
    
    smp_head = driver.find_element(By.XPATH, '//*[@id="contents_body"]/div[2]/div[2]/table/thead/tr').text
    smp_data = driver.find_element(By.XPATH, '//*[@id="contents_body"]/div[2]/div[2]/table/tbody/tr[27]').text
    
    #----- (월) (화) 이런식으로 요일표시된거 지우기. 너무 길어서
    import re
    pattern = r'\(.*?\)'
    cleaned_text = re.sub(pattern, '', smp_head)
    cleaned_text = cleaned_text.strip()
    #---------------------------------------------

    smp_head = cleaned_text.replace('\n', '')
    
    # print(repr(smp_head)) #문자열안에 특수문자까지 다 볼때
    # print(smp_head)
    # print(smp_data)

    time.sleep(2)
    driver.get(url2)
    action = ActionChains(driver)

    time.sleep(1)
    rec_data = driver.find_element(By.ID, 'tab-1').text
    rec = rec_data.replace('\n',' ')

    # print(f'rec_data = {rec_data}')
    # print(f'rec = {rec}')

    def get_last_word(s):   # 마지막 문자열만 return 해주는 함수
        # Split the string into words
        words = s.split()
        # Return the last word if the list is not empty
        return words[-1] if words else ""
    
    rec_avg = get_last_word(rec)
    # print(f'rec_avg = {rec_avg}')

    # print(type(rec3))
    # print(type(rec_avg))

    rec_avg_cleaned = rec_avg.replace(",", "")  # rec_avg 값에 ,제거 (int 변환시 에러방지)

    rec3_value = int(rec3) * int(rec_avg_cleaned)
    rec4_value = int(rec4) * int(rec_avg_cleaned)
    rec_total = rec3_value + rec4_value

    rec3_value_comma = format(rec3_value, ",")  # 금액처럼 3자리수마다 ,찍기
    rec4_value_comma = format(rec4_value, ",")
    rec_total_comma = format(rec_total, ",")

    # print(f'rec3 = {rec3}개, {rec3_value_comma}원')
    # print(f'rec4 = {rec4}개, {rec4_value_comma}원')

    # time.sleep(10000)

    driver.quit()

    result_solar = {
        'smp_head': smp_head,
        'smp_data': smp_data,
        'rec': rec,
        'rec3': rec3,
        'rec4': rec4,
        'rec3_value': rec3_value_comma,
        'rec4_value': rec4_value_comma,
        'rec_total': rec_total_comma
    }
    return(result_solar)

def aliexpress():
    printL("-- aliexpress coin start")
    options = Options()

    # 운영모드 체크
    if mode_check() == 'TEST':
        # options.add_argument("headless") #크롬창이 뜨지 않고 백그라운드로 동작됨
        pass
    else:
        options.add_argument("headless") #크롬창이 뜨지 않고 백그라운드로 동작됨
                
    # 아래 옵션 두줄 추가(NAS docker 에서 실행시 필요, memory 부족해서)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # config.json 파일처리 ----------------
    with open('config.json','r') as f:
        config = json.load(f)
    url1 = config['ALI']['URL1']
    user_id = config['ALI']['ID']
    password = config['ALI']['PASSWORD']
    # ------------------------------------
    print(user_id)
    print(password)
    print(url1)
    driver = webdriver.Chrome(options=options)

    # aliexpress coin 화면 진입
    driver.get(url1)
    #driver.maximize_window()
    action = ActionChains(driver)

    time.sleep(1)

    # ID 입력하고 로그인 버튼 클릭
    driver.find_element(By.CLASS_NAME, "cosmos-input").send_keys(user_id)
    driver.find_element(By.CLASS_NAME, "cosmos-input").send_keys(Keys.ENTER)
    time.sleep(2)
    # time.sleep(1000)
    driver.find_element(By.NAME, "fm-login-password").send_keys(password)
    driver.find_element(By.NAME, "fm-login-password").send_keys(Keys.ENTER)
    
    # 여기까지 했는데 로그인 할때 슬라이드 해야되는게 나오서 STOP
    pass

def stock_check():
    printL("-- stock check start")
    options = Options()

    # 운영모드 체크
    if mode_check() == 'TEST':
        # options.add_argument("headless") #크롬창이 뜨지 않고 백그라운드로 동작됨
        pass
    else:
        options.add_argument("headless") #크롬창이 뜨지 않고 백그라운드로 동작됨
                
    # 아래 옵션 두줄 추가(NAS docker 에서 실행시 필요, memory 부족해서)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # config.json 파일처리 ----------------
    with open('config.json','r') as f:
        config = json.load(f)
    url1 = config['STOCK_TSLA']['URL1']
    url2 = config['STOCK_TSLA']['URL2']
    url3 = config['STOCK_TSLA']['URL3']
    jh_cnt = config['STOCK_TSLA']['JH']
    yn_cnt = config['STOCK_TSLA']['YN']
    yh_cnt = config['STOCK_TSLA']['YH']
    yj_cnt = config['STOCK_TSLA']['YJ']
    sh_cnt = config['STOCK_TSLA']['SH']
    # ------------------------------------
    # print(url1)
    # print(jh_cnt)
    # print(yn_cnt)
    # print(yh_cnt)
    # print(yj_cnt)
    # print(sh_cnt)
    driver = webdriver.Chrome(options=options)

    # 네이버 주식 TSLA 주가 조회
    driver.get(url1)
    #driver.maximize_window()
    action = ActionChains(driver)

    time.sleep(2)

    tsla_value = driver.find_element(By.CLASS_NAME, "GraphMain_price__H72B2").text.replace("\nUSD", "")
    tsla_pct = driver.find_elements(By.CLASS_NAME, "VGap_gap__LQYpL")[1].text
    # print(tsla_value)
    # print(tsla_pct)

    # time.sleep(2)

    # 총 주식수 계산
    total_cnt = int(jh_cnt) + int(yn_cnt) + int(yh_cnt) + int(yj_cnt) + int(sh_cnt)

    # KRW 환율 조회
    driver.get(url2)
    action = ActionChains(driver)

    time.sleep(2)

    # time.sleep(10000)
    # usd_krw = driver.find_element(By.CLASS_NAME, "DetailInfo_price__InDYQ").text.replace("\nKRW", "").replace(",","")
    # 위의 구문은 CLASS_NAME 이 자꾸 바뀌는 문제로 아래문장으로 변경처리
    try:
        usd_krw = driver.find_element(By.CSS_SELECTOR, "[class^='DetailInfo_price__I']").text.replace("\nKRW", "").replace(",","")
        # print(usd_krw)
    except:
        usd_krw = "1440.44"
        # print("usd_krw fail")
    print(usd_krw)

    # JH
    result_jh = int(int(jh_cnt) * float(tsla_value) * float(usd_krw))
    jh_krw = format(result_jh, ',')
    # print(jh_krw)

    # YN
    result_yn = int(int(yn_cnt) * float(tsla_value) * float(usd_krw))
    yn_krw = format(result_yn, ',')
    # print(yn_krw)

    # YH
    result_yh = int(int(yh_cnt) * float(tsla_value) * float(usd_krw))
    yh_krw = format(result_yh, ',')
    # print(yh_krw)

    # YJ
    result_yj = int(int(yj_cnt) * float(tsla_value) * float(usd_krw))
    yj_krw = format(result_yj, ',')
    # print(yj_krw)

    # SH
    result_sh = int(int(sh_cnt) * float(tsla_value) * float(usd_krw))
    sh_krw = format(result_sh, ',')
    # print(sh_krw)

    # TOTAL
    result_total = result_jh + result_yn + result_yh + result_yj + result_sh
    total_krw = format(result_total, ',')

    driver.quit()

    # STOCK History DB 저장기능
    flag = True
    if flag:
        import sqlite3

        current_time = datetime.datetime.now()
        # formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        formatted_date = current_time.strftime("%Y%m%d")
        # formatted_month = current_time.strftime("%Y%m")

        daily_chg = 0
        # DB insert 처리
        try:
            conn = sqlite3.connect('stock.sqlite3')
            cursor = conn.cursor()

            def query_database(query):
                cursor.execute(query)
                result = cursor.fetchall()
                return result
            # 어제자(또는 가장 최근일) TOTAL 금액조회
            query1 = f'SELECT max(date), total_krw from stock_history where user = "TOTAL" and date != "{formatted_date}"'
            # 어제자(또는 가장 최근일) 환율 조회
            query2 = f'SELECT max(date), usd_krw from stock_history where user = "TOTAL" and date != "{formatted_date}"'
            try:
                YESTER_TOTAL_KRW = query_database(query1)[0][1]
                # print(result_total, YESTER_TOTAL_KRW)
                YESTER_USD_KRW = query_database(query2)[0][1]
            except:
                YESTER_TOTAL_KRW = 0
                YESTER_USD_KRW = 0

            daily_chg = format(result_total - int(YESTER_TOTAL_KRW), ',')
            # print(daily_chg)
            daily_chg_hwan = "{:.2f}".format(((float(usd_krw) - float(YESTER_USD_KRW)) / float(YESTER_USD_KRW)) * 100)

            # DEBUG Start
            printL(float(usd_krw))
            printL(float(YESTER_USD_KRW))
            printL(float(usd_krw) - float(YESTER_USD_KRW))
            printL(((float(usd_krw) - float(YESTER_USD_KRW)) / float(YESTER_USD_KRW)) * 100)
            printL(daily_chg_hwan)
            # DEBUG End

            if float(daily_chg_hwan) > 0:   # 일일 환율변동 %값이 양수면 + 붙여주기
                daily_chg_hwan = f"+{daily_chg_hwan}%"
            else:
                daily_chg_hwan = f"{daily_chg_hwan}%"
            printL(daily_chg_hwan)

            if float(daily_chg.replace(",", "")) > 0:   # 일일변동금액 %값이 양수면 + 붙여주기
                daily_chg = f"+{daily_chg}"
            else:
                daily_chg = f"{daily_chg}"
            printL(daily_chg)

            data_list1 = [
                (formatted_date, 'TSLA', 'JH', int(jh_cnt), float(usd_krw), result_jh),
                (formatted_date, 'TSLA', 'YN', int(yn_cnt), float(usd_krw), result_yn),
                (formatted_date, 'TSLA', 'YH', int(yh_cnt), float(usd_krw), result_yh),
                (formatted_date, 'TSLA', 'YJ', int(yj_cnt), float(usd_krw), result_yj),
                (formatted_date, 'TSLA', 'SH', int(sh_cnt), float(usd_krw), result_sh),
                (formatted_date, 'TSLA', 'TOTAL', total_cnt, float(usd_krw), result_total)
            ]
            cursor.executemany("INSERT OR REPLACE INTO stock_history (date, ticker, user, stock_cnt, usd_krw, total_krw) VALUES (?,?,?,?,?,?);", data_list1)
    
            conn.commit()
        finally:
            conn.close()

    result_stock = {
        'url1' : url1,
        'url2' : url2,
        'url3' : url3,
        'tsla_value': tsla_value,
        'tsla_pct': tsla_pct,
        'usd_krw': "{:.6s}".format(usd_krw),
        'jh_cnt': jh_cnt,
        'yn_cnt': yn_cnt,
        'yh_cnt': yh_cnt,
        'yj_cnt': yj_cnt,
        'sh_cnt': sh_cnt,
        'jh_krw': jh_krw,
        'yn_krw': yn_krw,
        'yh_krw': yh_krw,
        'yj_krw': yj_krw,
        'sh_krw': sh_krw,
        'total_krw' : total_krw,
        'total_cnt' : total_cnt,
        'daily_chg' : daily_chg,
        'daily_chg_hwan' : daily_chg_hwan
    }
    return(result_stock)

global_var = 0

# telegram 메세지 발송함수
async def tele_push(content): #텔레그램 발송용 함수
    if mode_check() == 'TEST':
        telegram_target = 'TELEGRAM-TEST'	# TEST 모드
    else:
        telegram_target = 'TELEGRAM'	# ONLINE 모드
	# telegram_target = 'TELEGRAM'	# 강제 ONLINE 모드
    # config.json 파일처리 ----------------
    with open('config.json','r') as f:
        config = json.load(f)
    token = config[telegram_target]['TOKEN']
    chat_ids = config[telegram_target]['CHAT-ID']
    # ------------------------------------

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    bot = telegram.Bot(token = token)

    # await bot.send_message(chat_id, formatted_time + "\n" + content)

    # 실패시 재시도를 여기서 하도록 변경
    for chat_id in chat_ids:
        # printL(f"chat_id : {chat_id}")
        send_retry = 0
        while True:	# 텔레그램 발송이 혹시 실패하면 최대 3회까지 성공할때까지 재시도
            try:
                if "STOCK" in content:  # STOCK 의 경우에만 Markdown 을 사용함
                    await bot.send_message(chat_id, formatted_time + "\n" + content, parse_mode = 'Markdown', disable_web_page_preview=True)
                else:
                    await bot.send_message(chat_id, formatted_time + "\n" + content)
                printL(f"-- SEND success!!! : {chat_id}")
                break
            except:
                send_retry = send_retry + 1
                printL(f"-- tele_push failed!!! ({send_retry}) : chat_id = {chat_id}")
                time.sleep(3)
                if send_retry == 3:
                    printL(f"-- tele_push aborted!!! : chat_id = {chat_id}")
                    break
            else:	# 정상작동시
                pass
            finally:	# 마지막에 (정상,에러 상관없이)
                pass

    global global_var
    global_var = global_var + 1	# 보낸 메세지가 있으면 +1씩 올라감

# ----------- MAIN ------------- 
flag = True
if flag:    # 시작시간 처리
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    start_time = current_time.strptime(formatted_time, "%Y-%m-%d %H:%M:%S")
    printL(f"-- START : {start_time}")
    printL(f"-- {mode_check()} MODE")

# inven 출석 실행
flag = True
if flag:
    attendance = inven()
    msg_content = f"[인벤] 횟수 : {attendance['count1']}->{attendance['count2']}, \n{attendance['txt']}"
    printL(msg_content)
    asyncio.run(tele_push(msg_content)) #텔레그램 발송 (asyncio를 이용해야 함)

# subs 출석 실행
flag = True
if flag:
    attendance = subs()
    if attendance['txt'] != "ERROR":
        msg_content2 = f"[SUBS] : {attendance['count1']},\n {attendance['txt']}"
        printL(msg_content2)
        asyncio.run(tele_push(msg_content2)) #텔레그램 발송 (asyncio를 이용해야 함)

# SMP,REC 시세조회 실행
flag = True
if flag:
    attendance = solar()
    # msg_content = f"[인벤] 횟수 : {attendance['count1']}->{attendance['count2']}, \n{attendance['txt']}"
    msg_content = f"[SOLAR] SMP 시세: \n - {attendance['smp_head']}\n - {attendance['smp_data']}\nREC 시세: \n - {attendance['rec']}\n - REC3 :{attendance['rec3']}개, {attendance['rec3_value']}원 \n - REC4 :{attendance['rec4']}개, {attendance['rec4_value']}원\n - Total : {attendance['rec_total']}원"
    printL(msg_content)
    asyncio.run(tele_push(msg_content)) #텔레그램 발송 (asyncio를 이용해야 함)

# ALIEXPRESS COIN 출석체크 실행 (로그인 DRAG에 막힘)
flag = False    # False 유지
if flag:
    attendance = aliexpress()
    # msg_content = f"[인벤] 횟수 : {attendance['count1']}->{attendance['count2']}, \n{attendance['txt']}"
    msg_content = f"[ALI] SMP 시세: \n - {attendance['smp_head']}\n - {attendance['smp_data']}\nREC 시세: \n - {attendance['rec']}\n - REC3 :{attendance['rec3']}개, {attendance['rec3_value']}원 \n - REC4 :{attendance['rec4']}개, {attendance['rec4_value']}원\n - Total : {attendance['rec_total']}원"
    printL(msg_content)
    asyncio.run(tele_push(msg_content)) #텔레그램 발송 (asyncio를 이용해야 함)

# 주가,수량,수익 일일체크
flag = True
if flag:
    # from datetime import datetime

    # 오늘의 요일을 숫자로 가져옴 (월요일=0, 일요일=6)
    today = datetime.datetime.today().weekday()

    # 일요일(6)이나 월요일(0)이 아닐 때 로직 수행
    if today not in (0, 6):
        attendance = stock_check()
        link1 = attendance['url1']
        link2 = attendance['url2']
        link3 = attendance['url3']
        # msg_content = f"[인벤] 횟수 : {attendance['count1']}->{attendance['count2']}, \n{attendance['txt']}"
        msg_content = f"\[[STOCK]({link3})] TSLA: [{attendance['tsla_value']} ({attendance['tsla_pct']})]({link1}) \nUSDKRW : [{attendance['usd_krw']} ({attendance['daily_chg_hwan']})]({link2}) \nJH : {attendance['jh_krw']} ({attendance['jh_cnt']}) \nYN : {attendance['yn_krw']} ({attendance['yn_cnt']}) \nYH : {attendance['yh_krw']} ({attendance['yh_cnt']}) \nYJ : {attendance['yj_krw']} ({attendance['yj_cnt']}) \nSH : {attendance['sh_krw']} ({attendance['sh_cnt']}) \nTOTAL : {attendance['total_krw']} ({attendance['total_cnt']}) \nDaily : {attendance['daily_chg']}"
        printL(msg_content)
        asyncio.run(tele_push(msg_content)) #텔레그램 발송 (asyncio를 이용해야 함)

if global_var == 0:	# 전체적으로 보낼 메세지가 1건도 없을때
	msg_content = " - att_auto : 메세지가 없음"
	printL(msg_content)
	asyncio.run(tele_push(msg_content)) #텔레그램 발송 (asyncio를 이용해야 함)

flag = True
if flag:    # 종료시간 처리
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time = current_time.strptime(formatted_time, "%Y-%m-%d %H:%M:%S")
    printL(f"-- END : {end_time}")
    printL(f"-- Elapsed time : {end_time - start_time}")
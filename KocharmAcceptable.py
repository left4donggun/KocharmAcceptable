from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import time

# 셀레니움 헤드리스 비활성화 및 GPU 비활성화
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-gpu")

# 드랍다운 메뉴 설정
def setDropDown(driver,findElement,css):
    element= Select(driver.find_element_by_css_selector(css))
    for i in range(len(element.options)):
        element= Select(driver.find_element_by_css_selector(css))
        if findElement==element.options[i].text :
            element.select_by_value(element.options[i].get_attribute('value'))

# 응시가능인원 조회
def getAcceptable(event,grade,city,place):
    # 브라우저 실행 및 사이트 접속
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.implicitly_wait(3) # 로딩될때까지 기다리는 대기시간
    driver.get('https://license.korcham.net/')
    
    # 프레임 변경(변경안하면 기본프레임만 읽혀서 개체에 접근을못함)
    driver.switch_to.frame(driver.find_element_by_css_selector('#idFrameMain'))

    # 시험장 확인 및 상시검정 탭으로
    driver.find_element_by_css_selector('#content_area > div > div.main_top_area > div.main_top_area_left > h2 > a').click()
    time.sleep(3)
    driver.find_element_by_css_selector('#content_area > div > div > div.content_right > div.tab_btn_area_license1 > ul > li:nth-child(2) > a').click()
    time.sleep(3)

    # 종목선택, 등급선택, 지역선택, 시험장선택
    setDropDown(driver, event, '#selectJmcd')
    setDropDown(driver, grade, '#selectDkcd')
    setDropDown(driver, city, '#selectAreaCd')
    setDropDown(driver, place, '#selectPcode')
    
    # 조회 버튼 클릭
    driver.find_element_by_css_selector('#myForm > div.tit_box01.mb200 > span > a').click()
    time.sleep(3)

    # 응시 가능시간 조회
    hm = [0 for i in range(10)]          
    # 14:40 15:30 ...
    for i in range(3,8):
        try:
            hm[i]=driver.find_element_by_css_selector('#placeInfoTable > tbody > tr:nth-child(1) > th:nth-child('+str(i)+')').text
        except:
            break
    
    # 일자 및 시간별 응시가능인원 조회
    acceptable={}
    # 일자별
    for r in range(2,20):
        try:
            date=driver.find_element_by_css_selector('#placeInfoTable > tbody > tr:nth-child('+str(r)+') > td:nth-child(1)').text
            acceptable[date]={}
        except:
            break
        # 시간별
        for c in range(3,8):
            try:
                ableCount = driver.find_element_by_css_selector('#placeInfoTable > tbody > tr:nth-child('+str(r)+') > td:nth-child('+str(c)+')').text
                acceptable[date][hm[c]]=ableCount
            except:
                break
    # 브라우저 종료 후 리턴
    driver.close()
    return acceptable

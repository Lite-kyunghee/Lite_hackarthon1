# riro_login_fixed.py
# 수정: Selenium 4 방식(Service 사용)으로 chromedriver 경로 지정
# Python 3.8+
# 실행: python riro_login_fixed.py

import time
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service  # <- 여기 중요
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# -------- 사용자 입력: 터미널에서 안전하게 입력 받기 --------
USER_ID = input("학교 아이디 또는 이메일 입력: ").strip()
USER_PW = getpass("비밀번호 입력 (입력중 표시되지 않음): ")

# -------- URL들 --------
LOGIN_URL = "https://kyungheeboy.riroschool.kr/user.php?action=signin"
TARGET_URL = "https://kyungheeboy.riroschool.kr/portfolio.php?db=1551"

# -------- chromedriver 경로 지정 (네가 설치한 곳으로 바꿔줘) --------
CHROMEDRIVER_PATH = r"C:\tools\chromedriver.exe"  # 예시 경로: 실제 경로로 변경

# -------- Chrome 옵션 설정 --------
options = Options()
options.add_argument("--headless=new")   # 창 안 띄우려면 이 줄 유지, 디버그할 땐 주석 처리
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1366,1080")

# -------- Service 객체 생성 후 드라이버 생성 --------
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

try:
    # 1) 로그인 페이지 열기
    driver.get(LOGIN_URL)
    time.sleep(1)

    # 2) id, pw 입력 필드에 값 넣기 (질문에서 알려준 id, pw 필드 id 사용)
    el_id = driver.find_element(By.ID, "id")
    el_pw = driver.find_element(By.ID, "pw")

    el_id.clear()
    el_id.send_keys(USER_ID)
    el_pw.clear()
    el_pw.send_keys(USER_PW)

    # 3) 제출 (엔터)
    el_pw.send_keys(Keys.ENTER)

    # 4) 로그인 처리 대기
    time.sleep(2.0)

    # 5) 포트폴리오 페이지 열기 (로그인 유지된 상태로)
    driver.get(TARGET_URL)
    time.sleep(1.5)

    # 6) 페이지 소스 저장
    html = driver.page_source
    with open("portfolio.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ 완료: 'portfolio.html' 파일이 저장되었습니다.")
except Exception as e:
    print("오류 발생:", e)
finally:
    driver.quit()

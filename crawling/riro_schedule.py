from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.alert import Alert
from getpass import getpass
import time

# -------------------------------
# 1️⃣ 계정 입력
# -------------------------------
USER_ID = input("학교 아이디 또는 이메일 입력: ").strip()
USER_PW = getpass("비밀번호 입력 (입력 중 표시되지 않음): ")

# -------------------------------
# 2️⃣ URL 정보
# -------------------------------
LOGIN_URL = "https://kyungheeboy.riroschool.kr/user.php?action=signin"
SCHEDULE_URL = "https://kyungheeboy.riroschool.kr/school_schedule.php?db=2301"

# -------------------------------
# 3️⃣ chromedriver 경로 (네 PC 경로로 수정)
# -------------------------------
CHROMEDRIVER_PATH = r"C:\tools\chromedriver.exe"

# -------------------------------
# 4️⃣ Chrome 설정
# -------------------------------
options = Options()
options.add_argument("--headless=new")  # 창 숨김 (디버깅 시 주석 처리)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1366,1080")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

try:
    # -------------------------------
    # 5️⃣ 로그인
    # -------------------------------
    driver.get(LOGIN_URL)
    time.sleep(1)

    driver.find_element(By.ID, "id").send_keys(USER_ID)
    driver.find_element(By.ID, "pw").send_keys(USER_PW)
    driver.find_element(By.ID, "pw").send_keys(Keys.ENTER)
    time.sleep(2)

    # 로그인 실패 시 alert 닫기
    try:
        alert = Alert(driver)
        print("⚠️ 로그인 실패:", alert.text)
        alert.accept()
        raise Exception("로그인 실패 (아이디 또는 비밀번호 확인 필요)")
    except NoAlertPresentException:
        pass

    # -------------------------------
    # 6️⃣ 학사일정 페이지 이동
    # -------------------------------
    driver.get(SCHEDULE_URL)
    time.sleep(2)

    # -------------------------------
    # 7️⃣ 페이지 저장
    # -------------------------------
    html = driver.page_source
    with open("school_schedule.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ 완료! 'school_schedule.html' 파일이 저장되었습니다.")

except Exception as e:
    print("오류 발생:", e)

finally:
    driver.quit()

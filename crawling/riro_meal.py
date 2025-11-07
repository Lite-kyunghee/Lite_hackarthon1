from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from getpass import getpass
import time

# -------------------------------
# 1️⃣ 계정 입력 (터미널에서 직접 입력)
# -------------------------------
USER_ID = input("학교 아이디 또는 이메일 입력: ").strip()
USER_PW = getpass("비밀번호 입력 (입력 중 표시되지 않음): ")

# -------------------------------
# 2️⃣ URL 정보
# -------------------------------
LOGIN_URL = "https://kyungheeboy.riroschool.kr/user.php?action=signin"
MEAL_URL = (
    "https://kyungheeboy.riroschool.kr/"
    "meal_schedule.php?db=2303&action=month&year=2025&month=11&meal_code=%EC%A4%91%EC%8B%9D"
)

# -------------------------------
# 3️⃣ chromedriver 경로 수정
# -------------------------------
CHROMEDRIVER_PATH = r"C:\tools\chromedriver.exe"  # 실제 설치된 경로로 바꿔줘

# -------------------------------
# 4️⃣ Chrome 실행 설정
# -------------------------------
options = Options()
options.add_argument("--headless=new")  # 창 없이 실행 (디버그 원하면 주석처리)
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

    # 로그인 입력
    driver.find_element(By.ID, "id").send_keys(USER_ID)
    driver.find_element(By.ID, "pw").send_keys(USER_PW)
    driver.find_element(By.ID, "pw").send_keys(Keys.ENTER)

    time.sleep(2)

    # -------------------------------
    # 6️⃣ 급식표 페이지로 이동
    # -------------------------------
    driver.get(MEAL_URL)
    time.sleep(2)

    # -------------------------------
    # 7️⃣ 페이지 HTML 저장
    # -------------------------------
    html = driver.page_source
    with open("meal_schedule.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ 완료! 'meal_schedule.html' 파일이 저장되었습니다.")

except Exception as e:
    print("오류 발생:", e)

finally:
    driver.quit()
python riro_meal.py

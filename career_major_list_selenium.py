from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# 1️⃣ Chrome 실행 옵션 설정
options = Options()
options.add_argument("--headless=new")  # 브라우저 창 숨김 (디버깅 시 주석 처리)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1366,1080")

# 2️⃣ 크롬드라이버 경로 설정 (본인 경로로 수정)
CHROMEDRIVER_PATH = r"C:\tools\chromedriver.exe"
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# 3️⃣ 대상 URL
url = "https://www.career.go.kr/cloud/w/major/uList"
driver.get(url)

# JavaScript 렌더링 대기
time.sleep(3)

# 🔽 스크롤 내려서 전체 항목 로딩
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# 4️⃣ HTML 가져오기 및 파싱
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# 5️⃣ 학과명 추출 (<p class="title">)
titles = [t.get_text(strip=True) for t in soup.select("p.title") if t.get_text(strip=True)]

# 6️⃣ DataFrame 생성
df = pd.DataFrame({"학과명": titles})

# 7️⃣ 엑셀로 저장 (encoding 인자 제거)
df.to_excel("career_major_list.xlsx", index=False)

print(f"✅ 완료! {len(df)}개의 학과가 career_major_list.xlsx 파일로 저장되었습니다.")
driver.quit()

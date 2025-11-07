import requests
from bs4 import BeautifulSoup

# 1️⃣ 크롤링할 URL
url = "https://www.career.go.kr/cloud/w/major/uList"

# 2️⃣ 요청 보내기
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers)
resp.raise_for_status()

# 3️⃣ HTML 파싱
soup = BeautifulSoup(resp.text, "html.parser")

# 4️⃣ p.title 태그 모두 선택
titles = soup.select("p.title")

# 5️⃣ 텍스트 추출
for i, t in enumerate(titles, 1):
    text = t.get_text(strip=True)
    if text:
        print(f"{i}. {text}")

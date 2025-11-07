from bs4 import BeautifulSoup

# 1. portfolio.html 파일 열기
with open("portfolio.html", "r", encoding="utf-8") as f:
    html = f.read()

# 2. BeautifulSoup으로 HTML 분석
soup = BeautifulSoup(html, "html.parser")

# 3. 제목(title) 찾기 (예: h1, h2, div.title 중 하나)
title = soup.select_one("h1, h2, .title, .board-view-title")
if title:
    print("📘 제목:", title.get_text(strip=True))
else:
    print("❌ 제목을 찾지 못했어요. HTML 구조 확인 필요.")

# 4. 담당 교사/작성자/학년/반 등의 정보 찾기 (예시)
info_table = soup.find("table")  # 포트폴리오 정보가 테이블일 가능성 높음
if info_table:
    for row in info_table.find_all("tr"):
        cells = row.find_all(["th", "td"])
        if len(cells) >= 2:
            key = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True)
            print(f"🧾 {key}: {value}")

# 5. 본문(내용) 찾기 (예: .content, .board-view, .post-content)
content = soup.select_one(".content, .board-view, .post-content, #content")
if content:
    text = content.get_text("\n", strip=True)
    print("\n📄 본문 미리보기:\n", text[:300], "...")
else:
    print("❌ 본문을 찾지 못했어요. HTML 구조 확인 필요.")

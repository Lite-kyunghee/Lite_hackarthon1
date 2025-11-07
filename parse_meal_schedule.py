from bs4 import BeautifulSoup
import re

# 1️⃣ 급식표 HTML 파일 열기
with open("meal_schedule.html", "r", encoding="utf-8") as f:
    html = f.read()

# 2️⃣ BeautifulSoup으로 HTML 파싱
soup = BeautifulSoup(html, "html.parser")

# 3️⃣ 날짜별 급식 정보가 들어있는 셀(td, div 등) 찾기
# 학교 리로스쿨 급식표는 보통 <td class="day"> 안에 날짜, <div class="menu"> 안에 메뉴가 들어있어요.
meals = []

for day_cell in soup.select("td, div"):
    text = day_cell.get_text("\n", strip=True)
    # 날짜(1~31)와 메뉴가 함께 들어있는 경우만 필터링
    if re.match(r"^\d{1,2}\s", text):
        day_match = re.match(r"^(\d{1,2})", text)
        if day_match:
            day = day_match.group(1)
            menu = text[len(day):].strip()
            if menu:
                meals.append({"day": day, "menu": menu})

# 4️⃣ 결과 출력
if meals:
    print("✅ 2025년 11월 급식표 (중식):\n")
    for item in meals:
        print(f"{item['day']}일 → {item['menu']}")
else:
    print("❌ 급식 데이터를 찾지 못했어요. HTML 구조가 달라졌을 수 있어요.")
import csv
with open("meal_schedule.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["day", "menu"])
    writer.writeheader()
    writer.writerows(meals)
print("📁 CSV 파일 저장 완료: meal_schedule.csv")

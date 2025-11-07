from bs4 import BeautifulSoup
import re
import csv

# 1️⃣ HTML 파일 읽기
with open("school_schedule.html", "r", encoding="utf-8") as f:
    html = f.read()

# 2️⃣ BeautifulSoup으로 파싱
soup = BeautifulSoup(html, "html.parser")

# 3️⃣ 학사 일정 데이터 추출
# 학교 일정은 보통 <td> 또는 <div> 안에 "날짜 + 일정명" 형태로 들어있음
events = []

for cell in soup.select("td, div"):
    text = cell.get_text("\n", strip=True)

    # 날짜로 시작하는 셀 찾기 (예: '11.08', '11월 8일', '8일')
    match = re.match(r"^(\d{1,2})(?:\.|\s*월\s*|\s*일\s*)", text)
    if match:
        day = match.group(1)
        schedule = text[len(match.group(0)):].strip()
        if schedule:
            events.append({"day": day, "event": schedule})

# 4️⃣ 결과 출력
if events:
    print("✅ 학사 일정 목록:")
    for e in events:
        print(f"{e['day']}일 → {e['event']}")
else:
    print("❌ 학사 일정 데이터를 찾지 못했어요. HTML 구조를 확인해봐야 할 수도 있어요.")

# 5️⃣ CSV로 저장 (선택)
with open("school_schedule.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["day", "event"])
    writer.writeheader()
    writer.writerows(events)

print("📁 CSV 저장 완료: school_schedule.csv")

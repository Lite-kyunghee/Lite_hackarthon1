import requests
from bs4 import BeautifulSoup

def get_suhang_data():
    url = "https://kyungheeboy.riroschool.kr/portfolio.php?db=1551"

    # 주신 쿠키 일부만 넣어도 로그인 유지됨
    cookies = {
        "PHPSESSID": "hn9jq44c4h1b6hf33cu0j3klhd",
        "riro_token": "VVc1R00wd3hhSFJYUlZwcFVYazVTVkpYV2xSaWJrSXdVVlpOTlZKR2EzcGhNMEpU...", 
        "cookie_token": "VDBod2EwNVlWblJQVlRrelZUQm9VMDFXV2s5V2JUQXpUbTEwTWxRd09ETldia3BJ...", 
    }

    headers = {"User-Agent": "Mozilla/5.0"}

    session = requests.Session()
    session.cookies.update(cookies)

    res = session.get(url, headers=headers)
    res.encoding = "utf-8"

    if "로그인이 필요합니다" in res.text:
        print("❌ 로그인 만료 또는 쿠키 오류")
        return []

    soup = BeautifulSoup(res.text, "html.parser")

    data = []
    for row in soup.select("table tbody tr"):
        cols = [td.get_text(strip=True) for td in row.select("td")]
        if len(cols) >= 3:
            data.append({
                "subject": cols[0],
                "desc": cols[1],
                "date": cols[2],
            })

    return data

import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# 환경 변수 로드
load_dotenv()

# API 키 설정
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# API 키 확인
if not NEWS_API_KEY:
    raise ValueError("❌ API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")

# 뉴스 API 설정
NEWS_URL = "https://newsapi.org/v2/everything"

def get_news():
    """NewsAPI에서 한국 관련 뉴스 가져오기"""
    params = {
        "q": "Korea",  # 검색어 설정
        "apiKey": NEWS_API_KEY,
        "pageSize": 5  # 최신 뉴스 5개 가져오기
    }

    try:
        response = requests.get(NEWS_URL, params=params)
        response.raise_for_status()
        data = response.json()

        print(f"🔍 API 응답 상태 코드: {response.status_code}")
        print(f"🔍 API 응답 데이터: {data}")

        if data.get("status") != "ok":
            print(f"🚨 API 오류: {data.get('message', '알 수 없는 오류')}")
            return []

        articles = data.get("articles", [])
        if not articles:
            print("⚠️ 뉴스가 없습니다.")
            return []

        return [(a.get("title", "제목 없음"),
                 a.get("description", "설명 없음"),
                 a.get("url", "https://newsapi.org/")) for a in articles]

    except requests.exceptions.RequestException as e:
        print(f"🚨 뉴스 데이터를 가져오는 중 오류 발생: {e}")
        return []

def update_readme():
    """README.md 파일 업데이트"""
    articles = get_news()
    news_summary = "⚠️ 최신 뉴스를 가져오는 데 실패했습니다." if not articles else ""

    for i, (title, desc, url) in enumerate(articles):
        news_summary += f"**{i + 1}. [{title}]({url})**\n> {desc}\n\n"

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    readme_content = f"""# 📢 한국의 최신 뉴스 (자동 업데이트)\n\n## 📰 오늘의 뉴스\n{news_summary}\n⏳ 업데이트 시간: {now}\n"""

    try:
        with open("README.md", "w", encoding="utf-8") as file:
            file.write(readme_content)
        print("✅ README.md 업데이트 완료")
    except IOError as e:
        print(f"🚨 README.md 파일 업데이트 실패: {e}")

if __name__ == "__main__":
    update_readme()
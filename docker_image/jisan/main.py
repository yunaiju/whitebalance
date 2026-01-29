from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import requests

def handler(event=None, context=None):
    service = Service("/opt/chromedriver")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/opt/chrome/chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
    chrome_options.add_argument('window-size=1392x1150')
    chrome_options.add_argument("disable-gpu")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    response_body = {}
    try:
        driver.get("https://www.jisanresort.co.kr/w/ski/slopes/info.asp")

        # WebDriverWait을 사용하여 테이블이 로드될 때까지 기다리기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.slope_table tbody'))
        )

        # 2. 슬로프 이름들 가져오기 (thead 첫 번째 tr)
        thead = driver.find_element(By.CSS_SELECTOR, ".slope_table thead")
        header_rows = thead.find_elements(By.TAG_NAME, "tr")

        # 첫 번째 tr → 슬로프 이름들
        slope_names = [th.text.strip() for th in header_rows[0].find_elements(By.TAG_NAME, "th")][1:]

        # 두 번째 tr → 난이도 정보
        slope_levels = [th.text.strip() for th in header_rows[1].find_elements(By.TAG_NAME, "th")]

        # 3. 상태 정보 가져오기
        tbody = driver.find_element(By.CSS_SELECTOR, ".slope_table tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        status_data = []
        for row in rows:
            tds = row.find_elements(By.TAG_NAME, "td")[1:]  # 첫 번째는 '주간', '야간', '심야'라서 제외
            row_data = []
            for td in tds:
                img = td.find_element(By.TAG_NAME, "img")
                src = img.get_attribute("src")
                status = "open" if "slope_open" in src else "close"
                row_data.append(status)
            status_data.append(row_data)  # 예: ['open', 'open', ..., 'close']

        # 4. 열 기준으로 재구성
        slope_data = []
        for i in range(len(slope_names)):
             slope_data.append([
                slope_names[i],  # 예: "1-1"
                slope_levels[i],  # 예: "초급"
                status_data[0][i],  # 주간
                status_data[1][i],  # 야간
                status_data[2][i],  # 심야
            ])

        slope_data = []

        print("Crawled slope_data : ", slope_data)

        # 백엔드 전송
        api_url = "https://whitebalance.site/slopeInfo/jisan"
        headers = {'Content-Type': 'application/json'}

        response = requests.post(api_url, json={"slope_data": slope_data}, headers=headers)
        response.encoding = 'utf-8'  # 인코딩을 강제로 설정

        print("Response slope_data : ", json.dumps({"slope_data": slope_data}, ensure_ascii=False))
        print(response.status_code)  # 상태 코드 출력
        print(response.text)  # 응답 본문 출력

        response_body = {
            'status': response.status_code,
            'body':json.dumps("데이터 전송 성공" if response.status_code == 200 else "데이터 전송 실패",
                              ensure_ascii=False  # 한글 인코딩 처리
            )
        }
    except Exception as e:
        response_body = {
            'statusCode' : 500,
            'body':json.dumps(f"Error: {str(e)}")
        }
    finally:
        driver.quit()

    return response_body
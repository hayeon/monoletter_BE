from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")  # headless 모드 추가

# ChromeDriverManager를 통해 설치된 ChromeDriver 경로를 Service 객체에 전달
service = Service(ChromeDriverManager().install())

# Service 객체와 options를 사용하여 Chrome WebDriver 생성
driver = webdriver.Chrome(service=service, options=options)

def url_crawl(driver: webdriver.Chrome):
    url_list = []
    with open("C://data/linkcareer_link.txt", 'w') as f:
        for page in range(1, 573):
            url = "https://linkareer.com/cover-letter/search?page=" + str(page) + "&tab=all"
            driver.get(url)
            driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[4]/div[2]/div/div[3]/div[1]")
            driver.implicitly_wait(3)
            url_tag = driver.find_elements(By.TAG_NAME, 'a')
            for tag in url_tag:
                url_name = tag.get_attribute('href')
                if "cover-letter" in url_name and "search" not in url_name:
                    print(url_name)
                    url_list.append(url_name)
        for content in list(set(url_list)):
            f.write(content + "\n")

def self_introduction(driver: webdriver.Chrome, url):
    person = {}
    driver.get(url)
    info = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[4]/div/div[2]/div[1]/div[1]/div/div/div[2]/h1')
    specification = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[4]/div/div[2]/div[1]/div[1]/div/div/div[3]/p')
    content = driver.find_element(By.ID, "coverLetterContent")
    person['info'] = info.text  # 지원자 정보
    person['specification'] = specification.text  # 지원자 스펙
    person['self_intro'] = content.text  # 지원자 자소서
    print(person)
    return person

url_crawl(driver=driver)  # 필요한 경우 주석 해제

with open(url, 'r') as f:
    while True:
        txt_link = f.readline().strip()  # .strip()을 추가하여 줄바꿈 문자를 제거
        if txt_link == "":
            break
        person = self_introduction(driver=driver, url=txt_link)
driver.quit()

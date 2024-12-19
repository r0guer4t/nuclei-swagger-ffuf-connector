import time
import random
import requests
import urllib
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

fuzzfile = "fuzz.txt"
inputFile = "swaggerVuln.txt"
outDir = "swagger-jsons"
userAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
    "Mozilla/5.0 (PLAYSTATION 3; 3.55)",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
]

os.makedirs(outDir, exist_ok=True)

def init_driver(user_agent):
    options = Options()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver

def find_swagger_link(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for link in soup.find_all('a', href=True):
        href = link["href"]
        if href.endswith("swagger.json"):
            return href
    return None

def fetch_json(url, driver, useragent):
    UA = useragent
    print(f"Trying: {url} with user agent \n{UA}\n\n")
    driver.get(url)
    time.sleep(6)
    content = driver.page_source

    soup = BeautifulSoup(content, "html.parser")

    pre_tag = soup.find("pre")
    if pre_tag:
        json_content = pre_tag.text.strip()
        json_content = json_content.replace('\n', '')
        if json_content:
            filename = f"{url.replace("https://", "").replace("/", "").replace("/swagger/24.43.0.56349/swagger.json", "")}.json"
            filepath = os.path.join(outDir, filename)
        with open(filepath, "w") as f:
            f.write(json_content)
            print(f"Saved {filepath}")
            return
    print(f"Skipped: {url}; No json")

def main():
    
    with open(inputFile, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    for url in urls:
        for uagent in userAgents:
            user_agent = uagent
            driver = init_driver(user_agent)
            try:
                driver.get(url)
                time.sleep(4)
                swagger_link = find_swagger_link(driver)
                baseurl = url.split("/")[2]
                if swagger_link:
                    if not swagger_link.startswith("http"):
                        from urllib.parse import urljoin
                        swagger_url = "".join(['https://',f'{baseurl}', f'{swagger_link}'])
                        print(f"Found swagger link: {swagger_url}")
                        fetch_json(swagger_url, driver, uagent)
                else:
                    print(f"No swagger page found for \n{url}\n with user agent \n[{uagent}]\n")
            except Exception as e:
                print(f"Exception {e}")

if __name__ == "__main__":
    main()
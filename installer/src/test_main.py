import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

url = "https://jp.indeed.com/q-%E5%AE%BF%E7%9B%B4-l-%E4%BA%AC%E9%83%BD%E5%BA%9C-%E4%BA%AC%E9%83%BD%E5%B8%82-%E6%B1%82%E4%BA%BA.html?vjk=be88d2ec933121b1"
headers = {"User-Agent": "Mozilla/5.0"}

def test_main():
    print("テストが正常に実行されました。")

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.get("https://secure.indeed.com/auth?hl=ja_JP&co=JP")
    time.sleep(2)  # ページが完全に読み込まれるまで待機


    try:
        print("『職種・キーワード』入力欄が出るまで待機します（最大300秒）...")

        # id="text-input-what" の要素が出現するまで最大300秒待機
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.ID, "text-input-what"))
        )

        print("要素が見つかりました！入力可能です。")

    except Exception as e:
        print("要素が見つかりませんでした：", e)

    # --- 「職種・キーワード」入力欄に "宿直" を入力 ---
    keyword_input = driver.find_element(By.ID, "text-input-what")
    keyword_input.clear()
    keyword_input.send_keys("宿直")

    # --- 「勤務地」入力欄に "京都" を入力 ---
    location_input = driver.find_element(By.ID, "text-input-where")
    location_input.clear()
    location_input.send_keys("京都")

    # --- Enterキーで検索実行 ---
    location_input.send_keys(Keys.RETURN)

    # 必要に応じて次の処理（検索結果の取得など）へ続ける
    time.sleep(5)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    # 求人全体のラップを取得
    wrapper = soup.find("div", id="jobsearch-ViewjobPaneWrapper")
    # その中から「求人本文」だけを取り出す
    description_div = wrapper.find("div", class_="jobsearch-JobComponent-description")

    # 出力
    if description_div:
        print(description_div.get_text(separator="\n", strip=True))
    else:
        print("本文セクションが見つかりませんでした。")


if __name__ == "__main__":
    test_main()
    print("テストが完了しました。")



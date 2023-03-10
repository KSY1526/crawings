import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('window-size= 1920,1080')
chrome_options.add_argument('--kiosk')
# executable_path : /opt/ml/crawling/chromedriver
driver = webdriver.Chrome(executable_path='/opt/ml/crawings/chromedriver', chrome_options=chrome_options)
data = pd.read_csv('./save_csv/river_behind_concat.csv')
url_list = list(data['url'].values)
userlink = pd.DataFrame()
#url_list = ["36528615", "31317229", "1269259731", "1779562085", "33040151", "1675801137", "1384361907", "1372982703", "1681990192", "1971062401"]
current_status = 2000
for _url in tqdm(url_list[2000:2256]):
    try:
        driver = webdriver.Chrome(executable_path='/opt/ml/crawings/chromedriver', chrome_options=chrome_options)
        action = ActionChains(driver)
        print(_url)
        URL = f"https://m.place.naver.com/restaurant/{_url}/review/visitor"
        driver.get(URL)
        time.sleep(2.5)
        count = 0
        flag = False
        while True:
            try: action.move_to_element(driver.find_element(By.CLASS_NAME, "lfH3O")).click().perform()
            except: break
            print("\r",count, end="")
            count+= 1
            if count >= 60: flag = True; break
        print("click 1/2 complete")
        time.sleep(2.5)
        try:
            #action.move_to_element(driver.find_elements(By.CLASS_NAME, "YeINN")[-1]).perform()  #?????? ?????? ??? + ?????? ?????????
            driver.find_element(By.CLASS_NAME, 'I8cuq').click()
        except: print("NO ???????????????")
        time.sleep(2.5)
        action = ActionChains(driver)
        while True:
            try:
                action.move_to_element(driver.find_element(By.CLASS_NAME, "lfH3O")).click().perform()
            except:
                break
            print("\r",count, end="")
            count+= 1
            if count >= 60: flag = True; break
        print("click 2/2 complete")
        if flag:
            with open("./user_csv/notsaved.txt", "a") as file:
                file.write(f"{str(current_status)}\n")
                file.close()
            current_status += 1
            continue
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        user = soup.find_all(class_='YeINN')
        link_list = [i.a['href'] for i in user]
        user_list = [i.text for i in user]
        #time.sleep(5)
        print(_url, len(link_list), len(user_list))
        userlink2 = pd.DataFrame({'link' : link_list, 'user' : user_list}, dtype = str)
        userlink2['rest'] = _url
        userlink = pd.concat([userlink, userlink2], axis = 0, sort=False)
        userlink.to_csv(f'./user_csv/river_behind{current_status}.csv', index=False)#river_behind500
        with open("./user_csv/log.txt", "w") as file:
            file.writelines(str(current_status))
        current_status += 1
    except:
        with open("./user_csv/notsaved.txt", "a") as file:
            file.write(f"{str(current_status)}\n")
            file.close()
        current_status += 1
        continue
print("End~")
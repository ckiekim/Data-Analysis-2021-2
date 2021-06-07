# 충정로역 맛집 검색
# 망고 플레이트 활용
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

driver = webdriver.Chrome()
driver.get('https://www.mangoplate.com/')
time.sleep(1)
search_box = driver.find_element_by_css_selector('#main-search')
search_box.send_keys('충정로역')
search_box.send_keys(Keys.ENTER)    # Keys.RETURN

time.sleep(1)
anchors = driver.find_elements_by_css_selector('p.paging>a')
name_list, score_list, summary_list, addr_list, tel_list = [],[],[],[],[]
for page in range(1, len(anchors)):
    lis = driver.find_elements_by_css_selector('ul.list-restaurants>li')
    for li in lis:
        info = li.find_element_by_css_selector('.info')
        name = info.find_element_by_css_selector('.title').text
        summary = info.find_element_by_css_selector('.etc').text
        li.find_element_by_xpath('/html/body/main/article/div[2]/div/div/section/div[3]/ul/li[1]/div[1]/figure/a').click()
        
        time.sleep(2)
        score = driver.find_element_by_css_selector('.rate-point').text
        table = driver.find_element_by_css_selector('table.info')
        trs = driver.find_elements_by_css_selector('tbody>tr')
        addr = trs[0].find_element_by_css_selector('td').text
        addr = addr.split('\n')[0]
        tel = trs[1].find_element_by_css_selector('td').text

        name_list.append(name)
        score_list.append(score)
        summary_list.append(summary)
        addr_list.append(addr)
        tel_list.append(tel)

        driver.back()
        time.sleep(1)

    anchors[page].click()
    time.sleep(2)

df = pd.DataFrame({
    '상호': name_list,
    '평점': score_list,
    '요약': summary_list,
    '주소': addr_list,
    '전화번호': tel_list
})
df.to_csv('충정로역맛집.csv', index=False, sep=',', encoding='utf8')
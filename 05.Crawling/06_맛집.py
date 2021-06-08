# 충정로역 맛집 검색
# 망고 플레이트 활용
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
driver.get('https://www.mangoplate.com/')
time.sleep(1)

# pop-up 창(iframe) 으로 이동해서 다시보지 않기 클릭
driver.switch_to.frame('google_ads_iframe_/395211568/init/desktop_all_0')
driver.find_element_by_css_selector('.ad_btn.ad_block_btn').click()

# 메인 창으로 이동해서 검색 데이터 입력후 리턴
driver.switch_to.default_content()
search_box = driver.find_element_by_css_selector('#main-search')
search_box.send_keys('충정로역')
search_box.send_keys(Keys.ENTER)    # Keys.RETURN
time.sleep(1)

anchors = driver.find_elements_by_css_selector('p.paging>a')
len_anchors = len(anchors)

name_list, score_list, summary_list, addr_list, tel_list = [],[],[],[],[]
for page in range(len_anchors):
    anchors = driver.find_elements_by_css_selector('p.paging>a')
    anchors[page].click()
    time.sleep(2)

    lis = driver.find_elements_by_css_selector('.list-restaurant')
    len_lis = len(lis)
    for index in range(len_lis):
        lis = driver.find_elements_by_css_selector('.list-restaurant')
        pair = lis[index].find_elements_by_css_selector('.list-restaurant-item')
        for i in range(len(pair)):
            lis = driver.find_elements_by_css_selector('.list-restaurant')
            pair = lis[index].find_elements_by_css_selector('.list-restaurant-item')
            info = pair[i].find_element_by_css_selector('.info')
            name = info.find_element_by_css_selector('.title').text
            summary = info.find_element_by_css_selector('.etc').text
            print(index, i, name)

            pair[i].find_element_by_css_selector('.only-desktop_not').click()
            time.sleep(2)

            try:
                score = driver.find_element_by_css_selector('.rate-point').text
            except:
                score = 'NA'
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

df = pd.DataFrame({
    '상호': name_list,
    '평점': score_list,
    '요약': summary_list,
    '주소': addr_list,
    '전화번호': tel_list
})
df.to_csv('충정로역맛집.csv', index=False, sep=',', encoding='utf8')
import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import traceback
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'cookie': 'CARTCOOKIEUUID=02511c8a-6dd9-4c27-ab77-427fd6360ef8; _gcl_au=1.1.978218272.1751446308; LPVID=U1MjMwN2E0ZjJlZjc3ODZl; _fbp=fb.1.1751446318652.72849915399442378; _gid=GA1.2.1890157068.1751446376; fs_uid=#Z1BBJ#6592c614-fbf0-4690-b49a-e54309c1e7ab:d86ccc92-9354-4527-9c15-ab1be0e67ca7:1751446378059::1#/1782982379; akacd_Default_PR=3928901761~rv=77~id=5dcd3807cc9f7401821ce3658e81fc5e; bm_mi=93FE1AEC36E687E6F8CCD4298252DA2B~YAAQLA1x3y5ySLGXAQAA9kd+yhzCvzqR0uw7vhhzMPWH6niFcaSRb/pBHJ16C9CMI1BKNZXPwuLF1yUGCWHtCjqiftVYA9OhWD4ROVajHLywOVYkq7zv7xWckvf7oF/DJKyk4gXI0pS1uID4295GqcMHLRgvMlGh51r3EuYn0oEZgkKFR5bN+kxDwsNHAJU7Zg1rul/9N7hqnWrCS9iy8ihlhgrrmWxbmtUclCAf2AXstDxfZqO2xGMRANyNtup5FaS8jGTAiswMDrr9UDv+jdoASgSbAE/RfWVwv8bI50BCW/VmChgMxvG09j+Qwr3ucWW9NuBpTpzu6MWpxQHyfkTDNB8KRYqIqb8YmrfJbq7JZsPw6lIlWpgQ5ntmvX1LYw==~1; ASP.NET_SessionId=4kyh2iuxc3km4s1kvxk4tcyt; __RequestVerificationToken=1ccqDi4X_kKgAf-A6Zkq19zOR1Q4VWxdc4EqYXqiErBzUxoa920N44UIqmx9wyzAxX_Dt09_3eSmyrzfxZVelHqcn801; ak_bmsc=49DD8A03F97331858172EF8564A1D087~000000000000000000000000000000~YAAQLA1x36JySLGXAQAApU5+yhwCfpMGplLQ9MVAcMhzGnllZk4jTeciK/5ih+niB5PVW/pVtUejPoAytvnCBloDh96oc5Z+KinhhpULAQXoDnPtSG63dAAJ/+uIr6F4ziAXHpfxgMKxzl259NRm56CgObEqyGK2NoEJb+pUTv7dQ4oZz+gmg8jWSe88tkBZPmyzqtWWPz3Q+x1kPxd6VdsHz+Y5DflIVkJHmQjOsC/BPRupQMBorgDnEF3uf2VlAWuUucr88jkirZi9rqBY6dX4dxB1PFSt1tUMum+DAxaUf9j8mYLmYjH+8ByQxukE8lTkJixqP01Wfs0BkP7HMygTIwDdh8MKUem6+qOYBI04hPummFpZTT6y/FfzY30tmAf4EVMF/AeGs8YWbRF9QhjsEBD/POimJ+AqzrfKJb9E3OsXXzUeNCOOJiFAMZsPBOzkSMzodbgMyR7Q+nC9OQHWo9D3ckIrVfBhKN+ewBzWcm6hKI00oB8LYYzjcXnMiGwuh4Da1dd02m9wpAw+KdC6tQ91ds2Y6cTZww6CYkqdjko=; __neoui=ae4e01a4-50ae-44fb-9e4c-b95ab33b8c05; _rdt_uuid=1751446318023.3adf85fe-9e36-416d-a3c8-e5f7a49d3a6f; LPSID-12757882=9zFu1iT7S8ayWIgTngMiBA; preferences=pl=zh-CN&pc_cn2=RMB; AKA_A2=A; bm_ss=ab8e18ef4e; QSI_HistorySession=https%3A%2F%2Fwww.mouser.cn%2FProductDetail%2FAmphenol-Commercial-Products%2FDPF20102721TR%3Fqs%3DST9lo4GX8V0LiCA7mgvRiQ%253D%253D~1751448996601%7Chttps%3A%2F%2Fwww.mouser.cn%2Fc%2F%3Fm%3DTAIYO%2520YUDEN~1751449834007%7Chttps%3A%2F%2Fwww.mouser.cn%2Fc%2Fpassive-components%2Femi-filters-emi-suppression%2Fferrites%2Fferrite-beads%2F%3Fm%3DTAIYO%2520YUDEN~1751449964016%7Chttps%3A%2F%2Fwww.mouser.cn%2FProductDetail%2FTAIYO-YUDEN%2FFBMH1608HM601-T%3Fqs%3DI6KAKw0tg2y6O4cu0afp%25252BA%253D%253D~1751450120563; bm_lso=DB94400ED29106848C43BC0EF832FE47CE7F4171A2A65603ECA9445838E3C073~YAAQLA1x3581SbGXAQAArnuPygQb2mI+3EJgzKy38vym0YBPWLGuCMeAbF1e17LJMUn1kHMqpRclzQVaB3GO6jVeTSTHqv87hiFs55C6wfBNBw8MwnxcdEWQhBtUFVdpeUoyoFBFfHaEGJrrmUJZuOy13PYOLC4EfObgswy8BxB4V4uwPoLIFMbkpoxaMUR0xuiY0qcaXHuj+B6kWB5jFoH/UNhArQ5AVu+G6XJxSrnXd8O2R0nhG9CSeeuzzAynWNlfLUPGyJmyO+fJdigOM4vLyPfBGDWfu7XMEoRGiF1FxKMBjb8/awBMyq2BitevWR1CLE6WmoN8uukHKDrgzUjKOPzZxME7OdQVzqpLYRfpvYqSvm5jpJG6NmmJTBqMPXQUGL3yT+zwaNlXuwxdol9kPIElwDowth6yMnDgtnbaeUCh9BYTv2+nMfhheeofFlXAaMro7VV3AAhjot4q^1751450120837; bm_so=2B58D5D1624F11DE343C5AED9318B371F8D4BD24B5549E48B7AB27641C0B13B7~YAAQLA1x3/9BSbGXAQAAE1qQygQ4xyu1fEcXn5XBU3WpAHjrFmDmCaZwun00YSWhxEd/7Z7FciyH5Ng1CfM9jFw3qC+JPUvLjar20tdgimHMDOq0jjWWbrqJYO/adwMlzUoMRJiyFK/6K3mDnYJYok10CbOX1N8mggVk2iss+QrcbY8o3lhZ574UrGM4hR3R1VRDl6JuwZyX6PAtZOkna+/egLIJ6t9+If3YxySRwHIv82Zdmn6mJh5ift3vFyLxtreSTWOvGqn3j4ytCq0ck5OkidPSzXM3GuPD1J9/antkGMRiQdTh39iIMyjodWyjYkvWSt7TR1qgpO91culCFjtP95pylkc7Z1qimyW3wWC42bw+LLLq+BQNQJxVIP4Utemei7jY7uJPwK6N70bjvo86gTJU3H/nId5B6QMZGJ33t/e4KARTIyf8YmQTyjayGJDVs6CjxeJln85UXFQ1; bm_sz=2F46830F37ADC34F1A9A59AD599B7F7F~YAAQLA1x3wBCSbGXAQAAE1qQyhy4QWW6T8PbIhr5oX8ROccxMfD74xR7iP0me6lap5eF43RjwENbFbP2nrpAKF9jTOE/56DYIAhqAGGBplrwFn9nrZPlW0tKRf/KV0v5ulOXzjBQlJDbVqEoshIbrAh60JtAbj2o091ATOof0UyZPclK/j+9/AB7qghAYHhifI0ceHZZ3lwuC4qiOLbb7bS1De4bEkN7eNEJpoHCjA90jRw4kj408qSzC3SxPgXvyRSIfxp406VOJIUycLMzI5CWYrMYosBhRfpyyKX2a2nCYuI75Mv9t6MZYfH9Lu6Lh6ynLGBsmUIrYIvGOcPxIawVvUKiRZ9wtsxVotcI/Cc0DhOhArisEj9xHy94sWzTPkQRjftjwP0a1kvlWgWKTBv1T7We0pGk+bBVGisDOHcmaZaqv0++Fycwiz0p8zfEF9EK851f7a0vyCY+eFyGYzeQqmoO0RKWybHqMllzpWG1GgI=~4339251~3158072; RT="z=1&dm=mouser.cn&si=d86db160-3bc7-44ce-9fe8-2ab446950a3a&ss=mclrhng9&sl=6&tt=r76&obo=5"; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Jul+02+2025+17%3A55%3A46+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202501.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=1c10bb45-e5b8-4f68-90d5-7e768d0dc7d7&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0001%3A1%2CC0002%3A1%2CC0004%3A1&intType=1&geolocation=CN%3BGD&AwaitingReconsent=false; OptanonAlertBoxClosed=2025-07-02T09:55:46.326Z; _ga_15W4STQT4T=GS2.1.s1751446376$o1$g1$t1751450146$j1$l0$h0; _ga=GA1.2.481766169.1751446376; _abck=C3D2A3C2C169422EE13DF3E48FEFEADA~-1~YAAQLA1x311CSbGXAQAA9GCQyg64UhxOH61T3GiDAdp3ILgce/7wiLaz7mxK4qsD7An30eJPTo8neEyWs72FEc27qE0mBYkYx9qEQH3PQzr1V++6Emh+kLEkzx80vzfRukf3dBEAoibB996APFxltbssdZgo3W/odCKSxt62BbT7B1dYfl+O/Z8oLfiE3OSrcyFEYfJlde3oTBjC4G919+ZkeICwXQypINrF0U40DPczeZ42Uv1oL0BJ/kfcoU4lUGL7a0NmNrgnEOarRrUeULMN+HvcLAZe/vUZl34Pqg/SP2We00iU1MoelVQ4rVJmslau/CK6GMKxu6RtAL+gH+K81i5tw4NvhL0Hmmk2FuVUbHnrEyZYj1x+08Wrj4SU+BEFsdFrmFPP26p2WWhEE6CRj7Choa4bH5nIfa+KwMIOkMH3ZpVSxUceEv9KGTHitq+xvic1Rkz+chmyciRzQRGQh5ZKgzoFI9yvXKcMZyCIAkL8R7gmsJdcS98P3He84dRYlMxtgFSygY5pRkELY5VbWI06Zz8mlXonq5MOcytgDCyKUxk8mG5djQOar1f0mSALSkQjCQl2qmcVy/e1C5RESFNzSS91d28ur0IVEXQ9qhZsWJLUdHrQ+t9F6N1QFXlLhTQFodfdvqiDHbZWB84z1UbugUCLSyW7tKDXQX5SYWkDB35EteFJf13yy4EpKggAfD4aNXa3gIu45gcbZkSIWcPMAGCvtfxBy8sPgTq8qmXiMJVN~-1~-1~-1; datadome=6fnGcQ_qKZiMrM20ssfW1iVHjleb_jekqeJVjP03IA6VjRM0mACpkA4gFyE_ODHQ0g_5tOZoJG8giSIwdLbKyRlLab7SR5Rs6KBIC_TBu7MrwyyAjZOtam_bMTzU0bJf; bm_s=YAAQLA1x32RCSbGXAQAASWGQygPg9e9r/H5UasiDmSVP6YSU7daFpGYNQRbCZq48UieFUPYSi3Ua12wXzTq5b4eczpOfiH/dtM2rOpNpm25eyetuTQEitRfJ8LbW+mrfwBvcSLJaNmujGSbrFiUE9eOPF+KGo2n/U5/mXpcVLTVaWG40Q5KIYgeYzTr/ReYGrA4Sk1puVqyeR40ngtS+os6oPls9xeXoiN5ub/wNihSx5Jsys1kifNbPeBCRWj5kPz71HqQMTZ/TNY9AU+XIaaJb7K0O60XeD2wpuSbXnYnXI8OxmlvZ5HOJF1l3epx/5FJ5V8qlW+TnFzbfWQTOusIsHkMX4p7onhEwiZX8+stvgWm/Q5VNqdXMrN+wIZEY7c/idOss85AJWuAw+PfAS8GVO4vZJyc/V5DS/RvLES/JusMBucdjiXmOEDdmo5ErMk190gJ+vRl0ZR0ZMrChc7QX9ff+CU4/Xlod31KFX3dULYe1ijH1U9COog6LsCjzQlrFjUYUfT5wHQS0Prs7/uLY8NPBe+qKCVijjWeX9h1SYoXGDarIlk7uWAAXSbqHnt7OTDLn3RQ=',  # 如需登录或验证，请取消注释并填写
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.mouser.cn/',
    'sec-ch-device-memory': '8',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.57", "Microsoft Edge";v="126.0.2592.56"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'x-requested-with': 'XMLHttpRequest',
}
domain = "https://www.mouser.cn/"

# ====== 配置区 ======
keywords = [
    'STM32F103C8T6',  # 精确物料编号
    '电容',            # 模糊关键字
    # ... 可继续添加
]
# 也可从txt读取
if os.path.exists('keywords.txt'):
    with open('keywords.txt', 'r', encoding='utf-8') as f:
        keywords = [line.strip() for line in f if line.strip()]

output_json_path = 'json/search_results.json'
output_csv_path = 'json/search_results.csv'

# ====== Selenium 启动配置 ======
options = uc.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_argument('--lang=zh-CN,zh')
# 不建议加 --headless，先用可视化模式

driver = uc.Chrome(options=options)

all_results = []

for keyword in keywords:
    print(f'正在查询: {keyword}')
    driver.get('https://www.mouser.cn/')
    time.sleep(2)

    # 显式等待搜索框出现
    try:
        search_box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-testid="global-search"]'))
        )
    except Exception:
        print("页面源码如下：")
        print(driver.page_source)
        # 保存源码，便于排查
        with open(f'debug_{keyword}.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        raise Exception('找不到搜索框，可能被反爬虫拦截或页面结构变动！')
    search_box.clear()
    search_box.send_keys(keyword)
    time.sleep(1)  # 等待输入框响应

    # 点击搜索按钮
    search_btn = driver.find_element(By.ID, 'hdrSrch')
    search_btn.click()
    time.sleep(3)  # 等待页面加载

    # 保存当前页面HTML源码
    safe_keyword = ''.join([c if c.isalnum() else '_' for c in keyword])
    with open(f'result_{safe_keyword}.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)

    # 等待至少有一个商品行出现
    try:
        rows = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, '//table[@id="SearchResultsGrid_grid"]/tbody/tr[@data-index]'))
        )
    except Exception:
        print("未找到商品行，保存页面源码以便排查。")
        with open(f'debug_{keyword}_no_rows.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        rows = []

    for row in rows:
        try:
            part_number = row.find_element(By.XPATH, ".//a[starts-with(@id, 'lnkMfrPartNumber_')]").text.strip()
        except Exception:
            part_number = ''
        try:
            manufacturer = row.find_element(By.XPATH, ".//a[starts-with(@id, 'lnkSupplierPage_')]").text.strip()
        except Exception:
            manufacturer = ''
        try:
            desc = row.find_element(By.XPATH, ".//td[contains(@class, 'desc-column')]/span").text.strip()
        except Exception:
            desc = ''
        try:
            supply_situation = row.find_element(By.XPATH, ".//span[contains(@class, 'available-amount')]").text.strip()
        except Exception:
            supply_situation = ''
        try:
            datasheet_url = row.find_element(By.XPATH, ".//a[contains(@href, 'pdf') and contains(@title, '数据表')]").get_attribute('href')
        except Exception:
            datasheet_url = ''
        try:
            image_url = row.find_element(By.XPATH, ".//img[contains(@id, 'defaultThumbImg_')]").get_attribute('src')
        except Exception:
            image_url = ''

        # 阶梯价提取
        price_ladder = []
        try:
            price_table = row.find_element(By.XPATH, './/table[contains(@class, "search-pricing-table")]')
            price_rows = price_table.find_elements(By.XPATH, './/tr[@data-qty]')
            for pr in price_rows:
                try:
                    qty = pr.find_element(By.XPATH, './/th|.//td').text.strip().replace(':', '').replace('剪切带', '').replace('卷轴', '')
                    price = pr.find_element(By.XPATH, './/span[contains(@class, \"text-nowrap\")]').text.strip()
                    price_ladder.append({'qty': qty, 'price': price})
                except Exception:
                    continue
        except Exception:
            pass

        result = {
            'keyword': keyword,
            'part_number': part_number,
            'manufacturer': manufacturer,
            'desc': desc,
            'supply_situation': supply_situation,
            'datasheet_url': datasheet_url,
            'image_url': image_url,
            'price_ladder': price_ladder
        }
        all_results.append(result)
    print(f"共获取到{len(rows)}条结果\n")
    time.sleep(2)  # 防止请求过快

driver.quit()

# 保存为 JSON
os.makedirs('json', exist_ok=True)
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)
print(f"已保存JSON: {output_json_path}")

# 保存为 CSV
df = pd.DataFrame(all_results)
df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
print(f"已保存CSV: {output_csv_path}")

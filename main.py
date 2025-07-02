import os
import time
import json
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from util import tools

# ========== 配置区 ==========
keywords = [
    'STM32F103C8T6',
    # 可继续添加
]
output_dir = 'output'
debug_dir = 'debug'
output_json_path = os.path.join(output_dir, 'search_results.json')
output_csv_path = os.path.join(output_dir, 'search_results.csv')

# ========== 主流程 ==========
def main():
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(debug_dir, exist_ok=True)
    all_results = []

    # 启动浏览器
    driver = uc.Chrome()

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
            tools.ensure_dir_and_save(os.path.join(debug_dir, f'debug_{keyword}.html'), driver.page_source)
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
        tools.ensure_dir_and_save(os.path.join(output_dir, f'result_{safe_keyword}.html'), driver.page_source)

        # 等待表格出现
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'SearchResultsGrid_grid'))
        )
        # 再等待至少一行数据出现
        rows = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, '//table[@id="SearchResultsGrid_grid"]/tbody/tr[@data-index]'))
        )

        for row in rows:
            row_data = tools.extract_row_data(row, keyword)
            all_results.append(row_data)
        print(f"共获取到{len(rows)}条结果\n")
        time.sleep(2)  # 防止请求过快

    driver.quit()

    # 保存为 JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"已保存JSON: {output_json_path}")

    # 保存为 CSV
    df = pd.DataFrame(all_results)
    df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    print(f"已保存CSV: {output_csv_path}")

if __name__ == '__main__':
    main()

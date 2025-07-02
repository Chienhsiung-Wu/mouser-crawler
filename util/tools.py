import os
from selenium.webdriver.common.by import By

def ensure_dir_and_save(file_path, content):
    dir_name = os.path.dirname(file_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def extract_text(element, by, selector):
    try:
        return element.find_element(by, selector).text.strip()
    except Exception:
        return ''

def extract_attr(element, by, selector, attr):
    try:
        return element.find_element(by, selector).get_attribute(attr)
    except Exception:
        return ''

def extract_price_ladder(row):
    price_ladder = []
    try:
        price_table = row.find_element(By.XPATH, './/table[contains(@class, "search-pricing-table")]')
        price_rows = price_table.find_elements(By.XPATH, './/tr[@data-qty]')
        for pr in price_rows:
            try:
                qty = pr.find_element(By.XPATH, './/th|.//td').text
                qty = qty.replace(':', '').replace('剪切带', '').replace('卷轴', '').replace(',', '').replace('\n', '').replace(' ', '').strip()
                price = pr.find_element(By.XPATH, './/span[contains(@class, "text-nowrap")]').text.strip()
                if qty and price:
                    price_ladder.append({'qty': qty, 'price': price})
            except Exception:
                continue
    except Exception:
        pass
    return price_ladder

def extract_row_data(row, keyword):
    def safe_find(by, selector):
        try:
            return row.find_element(by, selector)
        except Exception:
            return None

    def safe_text(by, selector):
        el = safe_find(by, selector)
        return el.text.strip() if el else ''

    def safe_attr(by, selector, attr):
        el = safe_find(by, selector)
        return el.get_attribute(attr) if el else ''

    image_url = safe_attr(By.CSS_SELECTOR, 'img', 'src')
    mouser_pn = safe_text(By.CSS_SELECTOR, 'span.mpart-number-lbl')
    part_number = safe_text(By.XPATH, ".//a[starts-with(@id, 'lnkMfrPartNumber_')]")
    manufacturer = safe_text(By.XPATH, ".//a[starts-with(@id, 'lnkSupplierPage_')]")
    desc = safe_text(By.CSS_SELECTOR, 'td.desc-column span')
    datasheet_url = safe_attr(By.XPATH, ".//a[contains(@href, 'pdf') and contains(@title, '数据表')]", 'href')
    supply = safe_text(By.CSS_SELECTOR, 'span.available-amount')
    rohs = '是' if safe_find(By.CSS_SELECTOR, '.fa-m-rohs') else '否'
    price_ladder = extract_price_ladder(row)
    return {
        'keyword': keyword,
        'image_url': image_url,
        'mouser_part_number': mouser_pn,
        'part_number': part_number,
        'manufacturer': manufacturer,
        'desc': desc,
        'datasheet_url': datasheet_url,
        'supply': supply,
        'rohs': rohs,
        'price_ladder': price_ladder
    } 
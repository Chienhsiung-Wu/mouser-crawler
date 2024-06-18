from lxml import etree
import json

# 读取 HTML 文件内容
html_file_path = 'mouser.html'
output_json_path = 'mouser_category_data.json'

with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# 解析 HTML 内容
parser = etree.HTMLParser()
tree = etree.HTML(html_content, parser)

# 提取数据
categories = []

# 使用 XPath 查找所有包含类别信息的 div 标签
panel_divs = tree.xpath('//div[@class="panel light-grey-panel"]')
for panel in panel_divs:
    main_category_name = panel.xpath('.//h2[@class="seoh2DefaultPage"]/text()')[0].strip()
    sub_categories = []

    sub_category_elements = panel.xpath('.//ul/li')
    for sub_category in sub_category_elements:
        sub_category_name = sub_category.xpath('.//a/text()')[0].strip()
        sub_category_link = sub_category.xpath('.//a/@href')[0].strip()
        sub_category_count = sub_category.xpath('.//span[@class="stat-count"]/text()')
        sub_category_count = sub_category_count[0] if sub_category_count else "0"

        sub_categories.append({
            "name": sub_category_name,
            "link": sub_category_link,
            "count": sub_category_count
        })

    categories.append({
        "main_category": main_category_name,
        "sub_categories": sub_categories
    })

with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(categories, json_file, ensure_ascii=False, indent=4)

print(f"JSON 数据已保存到 {output_json_path}")

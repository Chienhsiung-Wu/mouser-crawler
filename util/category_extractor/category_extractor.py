from lxml import etree
import json


class CategoryExtractor:
    def __init__(self, html_file_path, output_json_path):
        self.html_file_path = html_file_path
        self.output_json_path = output_json_path
        self.categories = []

    def read_html(self):
        """读取 HTML 文件内容"""
        with open(self.html_file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def parse_html(self, html_content):
        """解析 HTML 内容"""
        parser = etree.HTMLParser()
        return etree.HTML(html_content, parser)

    def extract_categories(self, tree):
        """提取类别数据"""
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

            self.categories.append({
                "main_category": main_category_name,
                "sub_categories": sub_categories
            })

    def save_to_json(self):
        """保存数据到 JSON 文件"""
        with open(self.output_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(self.categories, json_file, ensure_ascii=False, indent=4)
        print(f"JSON 数据已保存到 {self.output_json_path}")

    def run(self):
        """运行提取流程"""
        html_content = self.read_html()
        tree = self.parse_html(html_content)
        self.extract_categories(tree)
        self.save_to_json()

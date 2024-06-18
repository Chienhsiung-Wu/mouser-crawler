from util.category_extractor.category_extractor import CategoryExtractor


def main():
    html_file_path = r'C:\Users\IDhammaI\PycharmProjects\maoser-spider\test_html\mouser_all.html'  # 输入 HTML 文件路径
    output_json_path = r'C:\Users\IDhammaI\PycharmProjects\maoser-spider\json\category_data.json'  # 输出 JSON 文件路径

    extractor = CategoryExtractor(html_file_path, output_json_path)
    extractor.run()


if __name__ == "__main__":
    main()

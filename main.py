from util.category_extractor.category_extractor import CategoryExtractor


def main():
    # 输入 HTML 文件路径
    html_file_path = r'C:\Users\IDhammaI\PycharmProjects\maoser-spider\test_html\mouser_all.html'
    # 输出 JSON 文件路径
    output_json_path = r'C:\Users\IDhammaI\PycharmProjects\maoser-spider\json\category_data.json'

    # 更新元数据，保存本地json文件夹
    extractor = CategoryExtractor(html_file_path, output_json_path)
    extractor.run()

    # TODO: 根据json文件夹下的 category_data.json 进行request请求，爬取html结构解析该类别的 ①图像url,②零件编号,③制造商,④数据表url,⑤供货情况,⑥单价 ....



    # TODO: 异常处理 --> 更换代理IP



if __name__ == "__main__":
    main()

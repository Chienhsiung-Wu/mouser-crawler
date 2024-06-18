import time
from lxml import etree
import json
import requests
from util.category_extractor.category_extractor import CategoryExtractor
from urllib.parse import urljoin

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': 'CARTCOOKIEUUID=5354d9c5-44fe-494b-9599-db7e522d6425; _gcl_au=1.1.1764037813.1718090413; LPVID=NiZjUxZmJjZjNiYWEyY2Qz; __neoui=e1088477-79eb-40c7-a5a0-befb205a03e9; preferences=pl=zh-CN&pc_cn2=RMB; ASP.NET_SessionId=potijxrwix3y3jos2tjl2o1y; akacd_Default_PR=3896136703~rv=72~id=fb92b8ff2c17d8744442c3167331afde; ak_bmsc=6D0A997C2A8D8538AF30C4BE92CB5BD4~000000000000000000000000000000~YAAQrW2bG0wQhRGQAQAAf0GLKRhBJz0ip9obgqDf0+maa+3QPeZInadsNx/TYZ5PzvRuOIlnVqdKI419/O739SlGckNB3MhL9t0V811eFTmYR/NAua7dI7u60kqOH8Yx2JDCUAk9P1gTFmhShYVrSrX6L4JgM83wojqayzy3vJFx69yrvrqtmYI7MPJbJ8vmzAbo6JpHDG8HfdDZltTBt+pAKOv9GbL6Cd5Zq5Y/qITql1JpRceCjl2FtfqWVG7H7t4NerSPcmInAjvOtEGuh4dqIYAH7kXgqhlomd3WhtlA0CG2z9YN/+q6bB3hUoFS7sQrQbVStU6iWHyZ3834BLgfbovh/ljE1KqfPcgTZtB/Ik7Vldh9xE35TMk/fiDpVvuhf2OiLjGLXTB81s9uPk10PCJRYbP03X7gjOYAh8gvsgFFdEuLTSB9zZeaPX2jljbX3GTEQSpVIg==; LPSID-12757882=bjIqfqW9QyOACjT11A1OjA; __RequestVerificationToken=_f0OkhlqmzSoTzR62TfdtEEz00eTsWy9qmlV6GEM3BFJ2GyZZuZ0YRs5ZCOhdcvBsYktDaRpVg2tSeY9BZ86nnmNiQw1; enableFBPixel=true; _gid=GA1.2.1811481475.1718684021; Qs_lvt_553214=1718090414%2C1718093102%2C1718684020; Hm_lvt_3fa35b8bcb337f85238a44fa74ebff2b=1718090414,1718684021; QSI_HistorySession=https%3A%2F%2Fwww.mouser.cn%2Felectronic-components%2F~1718684095031; mediav=%7B%22eid%22%3A%221250535%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22*Xpe%5D%3De2%3D8%3Dfy-(%5D5vBJ%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22*Xpe%5D%3De2%3D8%3Dfy-(%5D5vBJ%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A0%7D; Hm_lpvt_3fa35b8bcb337f85238a44fa74ebff2b=1718684238; _ga=GA1.2.793794578.1718090414; Qs_pv_553214=1868442201036680000%2C4090842741355106300%2C515245147981805200%2C1116322752022973600%2C1715542305968117500; fs_uid=#Z1BBJ#17efe1a7-224a-407b-b00b-a853bcf7b818:d3f444f2-2810-4ebb-abff-94195897575f:1718684021418::5#/1749626500; RT="z=1&dm=mouser.cn&si=6f3b200f-c83e-4617-8d21-23160e098430&ss=lxjw36uh&sl=2&tt=1j9n&bcn=%2F%2F684d0d42.akstat.io%2F&ld=5m6e&ul=b588&hd=b5s1"; _ga_15W4STQT4T=GS1.1.1718684020.2.1.1718684537.60.0.0; _fbp=fb.1.1718685054793.299143179773650040; AKA_A2=A; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jun+18+2024+13%3A18%3A12+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202403.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=8c98f17b-40bf-4ca7-ba08-5de626df0437&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0004%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1&AwaitingReconsent=false&geolocation=CN%3BGD; OptanonAlertBoxClosed=2024-06-18T05:18:12.027Z; datadome=NdOO~UqblsaS9Dei9xz6mbmVifqioa1dQDB~EzkwrG2wuOiBI6a5puTCaa1uUllpT5F7Yj49gDWPFfrjZ23UW8rPbFiZHPcP11pFU27TzY6mNL7uL9H~5Lrx50az87VM; bm_sz=0EA96CCF2E293100F4A861F64FBEA850~YAAQtG2bG5S1IiCQAQAAmyPMKRiH4s+QvC2Xe6XkanHFjHecCCPOOvHK+2Jj11J+oyfqD8AP8J0grv4xiDT+z7E49tv6flkUnWheY0PaeJ8ht1PoNyM0j9XPFK0Zg2LliAx3JrZ0d5dTuv+B5bWnv5CyZ9oHUGcGG4Ylgwh5Kkxoj4UF0Smz3WnMB1LDwZKHW3OEyqiR3pV4MNGax6Q0pSgArQJDtMOWQUuOGdDO2ttIFnZHYO9RyD8FqNO3RmvnVqZ0Mxveztj47X1sOSoG0DAxyjJkOZ9gYm/5SDeBFbAZ6Zcp3rWhpO5UBx5m3AsHmMnvd3N9SlASrVJbYXZpwM7c9C3KutCTfYViQJ52bOYP3hFyweAwUzziM0TP/2HEnoVqBSNv0OLGTebXEw2UHwNBId028r9upycBvRdG4Y+ArMSZhW4Iw8YyjG1I2hlLmUZhXfZK3XRWJEdZe22jpGMJuzJpBt7SBZJPI112zCUl9caZhiOxa89juE1hTJcGcmE+uqlhZUiKB4dLCNaAUAcB/DM28786LqQAnqKlKQ==~3228977~4276806; _abck=B90EFBD5B969ACDC3A56094D0FA705F0~-1~YAAQtG2bG7C1IiCQAQAAvjPMKQyrGEahgwkH7ET0T42J5I1dHBnpX+0wrLj7Hyx7uHpBN3FN7mlzqg10iHRbYoQYeuOl0+dTSstgd2iX+UN6z2vVbsQLTXoQ4TJLw4hBXSLb5MEBEcAUe7TdfogT6Sr82isUZGTSAATeH5m3C2XgyqtVc47grb+CfSnGvKacx7HZ+hpG2CUJ05NNxBsWkcy+exNjGD0wrn9Ty0F+5clbR8fBP/bNkmR3NMekuw7YBNyr/l2NB4+wDxUYm1DjQ6gO5OAs3+uQmPm6OU3dAbRgez6VPGttY2Krm/IPtLgoaxuc+GldUfcAq0T3IKKSIGX8jdeQUCmBvgPQBn8yK6VRgRO4YllPn1gLll4Ci/eTEPPj4fSZB+s8mZSXFnX5aTIlXmbeevcLsUklHlOgTCt3RpY7TQ==~-1~-1~-1',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.mouser.cn/c/semiconductors/wireless-rf-semiconductors/pin-diodes/',
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


def main():
    # 输入 HTML 文件路径
    html_file_path = r'C:\Users\IDhammaI\PycharmProjects\maoser-spider\test_html\mouser_all.html'
    # 输出 JSON 文件路径
    output_json_path = r'C:\Users\IDhammaI\PycharmProjects\maoser-spider\json\category_data.json'

    # 更新元数据，保存本地json文件夹
    extractor = CategoryExtractor(html_file_path, output_json_path)
    extractor.run()

    # TODO: 根据json文件夹下的 category_data.json 依次进行request请求link字段，爬取html结构解析该类别的 ①图像url,②零件编号,③制造商,④数据表url,⑤供货情况,⑥单价 ....
    with open(output_json_path, 'r', encoding='utf-8') as f:
        category_data = json.loads(f.read())

    for index, item in enumerate(category_data):
        print(
            f"当前爬取目标类: {item['main_category']} 的 ({index + 1}/{len(item['sub_categories'])})子类--{item['sub_categories'][index]['name']}-{item['sub_categories'][index]['count']}个")

        try:
            response = requests.get(urljoin(domain, item['sub_categories'][index]['link']), headers=headers)
            if response.status_code == 200:
                tree = etree.HTML(response.text)

                # 图片由js动态加载，暂时不解决 ['/images/skeleton.png']
                # image = tree.xpath("//img[@id='defaultThumbImg_5']/@src")

                # 零件编号
                part_number = tree.xpath("//a[@id='lnkMfrPartNumber_1']")
                print(part_number[0].text)

                # 制造商
                manufacturer = tree.xpath("//a[@id='lnkSupplierPage_1']")
                print(manufacturer[0].text)

                # 描述
                desc = tree.xpath("//td[@class='column desc-column hide-xsmall']/span")
                print(desc[0].text)

                # 供货情况
                supply_situation = tree.xpath("//span[@class='available-amount']")
                print(supply_situation[0].text)

                # 单价//span[@id='lblPrice_1_1']
                price = tree.xpath("//span[@id='lblPrice_1_1']")
                print(price[0].text)

                # 保存 HTML
                # with open(output_json_path,'w',encoding='utf-8') as f:
                #     f.write(response.text)
                #     f.close()
                # print(f"HTML 数据已保存到 {output_json_path}")



                print("请求成功！")
            else:
                print("请求失败！")
        except Exception as e:
            print(f"出现异常:{e}")

        time.sleep(1000)

    # TODO: 异常处理 --> 更换代理IP


if __name__ == "__main__":
    main()

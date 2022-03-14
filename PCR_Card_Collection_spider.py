import requests
from bs4 import BeautifulSoup
import time
from pathlib import Path

while True: # while True表示永远循环，while False表示它不会执行
    try:
        port = int(input('请输入您的代理软件监控端口号\n例：clash默认端口7890\nshadowsocks默认端口1080\n请在此输入端口号：'))
    except ValueError:
        print("输入错误请重新输入，端口号应为一个整数")
        continue
    if type(port) == int:
        print(f'已成功设置代理，您输入的端口号为：{port}')
        break

path_config = 'Card_Collection'  # 设置图片的保存地址

Path(path_config).mkdir(parents = True, exist_ok = True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76'
}

proxy = {
    'http': f'http://localhost:{port}',
    'https': f'http://localhost:{port}'
}

time_start = time.time()

urls = [f'https://e-hentai.org/g/1518951/5a03e1ac32/?p={p}' for p in range(0, 29)]

img_num = 0
page_num = 0
error_num = 0
success_num = 0
for url in urls:
    page_num += 1
    try:
        resp = requests.get(url, headers=headers, proxies=proxy, timeout=90)
        print(f'第 {page_num} 页请求成功，即将开始下载...')
    except:
        print(f'第 {page_num} 页请求超时，请检查代理设置或网络连接')
        continue
    resp.encoding = 'utf-8'
    main_page = BeautifulSoup(resp.text, 'html.parser')
    alist = main_page.find('body').find('div', attrs={'id': 'gdt'}).find_all('a') # attrs表示标签属性，以字典形式输入

    for a in alist:
        href = a.get('href') # 直接通过get就可以拿到属性的值
        img_num += 1
        try:
            img_resp = requests.get(href, headers=headers, proxies=proxy, timeout=90)
        except:
            print(f'第 {img_num} 个图片页请求超时，请检查代理设置或网络连接')
            error_num += 1
            continue
        img_resp.encoding = 'utf-8'
        img_page = BeautifulSoup(img_resp.text, 'html.parser')
        img_src = img_page.find('body').find('div', attrs={'id': 'i3'}).find('img').get('src')
        img_name = img_src.split("/")[-1] # 以 / 为分割，将字符串拆分成一个列表，并读取倒数第一个值
        
        if not Path(path_config, img_name).exists():
            try:
                img_data = requests.get(img_src, headers = headers, proxies = proxy, timeout = 180).content
                # .content 拿到字节(二进制对象)
            except:
                error_num += 1
                print(f'error! 第 {img_num} 个图片下载失败：{img_name}')
                continue
            Path(path_config, img_name).write_bytes(img_data) # 以二进制方式写入文件
            success_num += 1
            print(f'第 {img_num} 个图片下载成功：{img_name}')
        else:
            print(f'文件 {img_name} 已存在，不再进行下载')

time_end = time.time()
use_time = int(time_end - time_start)
print(f'全部下载完成！共下载成功{success_num}个文件，失败{error_num}个文件，用时{use_time}秒')
print('程序将在10秒后结束...')
time.sleep(10)
import requests, bs4, time, random
path = "./wallpaper/爱上紫禁城"

catch = 0

for i in range(1, 119):
    # 组合请求 URL
    url = "https://www.dpm.org.cn/lights/royal/p/{}.html".format(i)
    # 发送请求
    response = requests.get(url)
    # 设定页面编码为 UTF-8
    response.encoding = "UTF-8"
    # 从 HTML 中解析数据
    soup = bs4.BeautifulSoup(response.text, "lxml")
    image = soup.find_all(name="div", class_="pic")
    # 循环输出图片
    for n in image:
        catch = catch + 1
        # 获得壁纸名称
        # 分类，不是以【爱上紫禁城】开头的壁纸都忽略
        img_name = n.a.img["title"]
        if img_name.startswith("明"):
            print("{}. {}".format(catch, n.a.img["title"]))
            # 组合获得壁纸页面
            url_1080 = "https://www.dpm.org.cn" + n.a["href"]
            # 请求高清版网页
            response_img = requests.get(url_1080)
            # 再次解析
            soup_img = bs4.BeautifulSoup(response_img.text, "lxml")
            # 获取页面中的图片
            data = soup_img.find_all(name="img")[0]
            # 获得壁纸图片的链接
            img_url = data["src"]
            # 保存图片
            pic = requests.get(img_url).content
            file_name = path + img_name + "-" + str(random.randint(100000, 999999)) + ".jpg"
            # 写入文件
            with open(file_name, "wb") as file:
                file.write(pic)
        
        else:
            print("!Ignore: " + img_name)
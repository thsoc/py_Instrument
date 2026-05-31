import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin  # 新增导入

def download_image_from_url(url, path=None, headers=None):
    # 访问网址并获取图片

    # 1. 设置目标网址 (请替换为实际网址)
    if url.startswith("http://") or url.startswith("https://"):
        pass
    else:
        url = "http://" + url

    # 模拟浏览器头，防止被反爬
    if not headers:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }

    # 2. 发送请求获取网页内容
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"  # 根据实际网页编码调整

    # 3. 检查请求是否成功
    if response.status_code == 200:
        # print(f"请求成功{response.text}")
        soup = BeautifulSoup(response.text, "html.parser")

        # 4. 查找所有图片标签 <img>
        img_tags = soup.find_all("img")

        # 创建保存图片的文件夹
        if not path:
            base_dir = os.getcwd()

        # 2. 确定图片保存的子文件夹 (例如 "images")
        save_dir = os.path.join(base_dir, "images")

        # 3. 一次性创建文件夹 (exist_ok=True 表示如果已存在也不报错)
        os.makedirs(save_dir, exist_ok=True)

        print(f"找到 {len(img_tags)} 张图片标签")

        # 5. 遍历并下载图片
        for i, img in enumerate(img_tags):
            # 【关键修改】优先获取 data-original (懒加载)，如果没有再获取 src
            img_url = img.get("data-original") or img.get("data-src") or img.get("src")
            if img_url:
                # 使用 urljoin 自动处理相对路径和绝对路径的拼接
                # 它会自动识别 img_url 是以 / 开头还是 http 开头
                # print(f"图片前缀: {url}")
                print(f"图片地址: {img_url}")
                full_url = urljoin(url, img_url)
                print(f"图片地址: {full_url}")

                # 如果 urljoin 处理后仍然不是 http/https 开头（比如 data:image...），则跳过
                if not full_url.startswith(("http:", "https:")):
                    continue
                # 跳过img_url不包含后缀的.的图片
                if "." not in img_url:
                    continue

                try:
                    # 获取图片内容
                    img_data = requests.get(
                        full_url, headers=headers, timeout=30
                    ).content
                    # 从 URL 中提取路径部分，再提取扩展名
                    parsed_path = img_url.split("?")[0]  # 去掉可能的参数
                    _, ext = os.path.splitext(
                        parsed_path
                    )  # 分离文件名和后缀，ext 会包含点，如 '.svg'

                    if not ext:
                        ext = ".jpg"  # 如果没有后缀，给一个默认值

                    file_name = f"images/image_{i}{ext}"
                    # 确定文件扩展名 (简单处理，默认jpg)

                    with open(file_name, "wb") as handler:
                        handler.write(img_data)
                    print(f"已保存: {file_name}")
                except Exception as e:
                    print(f"下载失败 {img_url}: {e}")
                    # continue
    else:
        print(f"请求失败，状态码: {response.status_code}")

if __name__ == "__main__":
    url = input("请输入网址: ")
    download_image_from_url(url)

        # 防止窗口关闭
    input("\n按回车键退出...")
import os
import requests
import zipfile
import shutil
from pathlib import Path

def download_font():
    print("开始下载字体文件...")
    url = "https://static.zitijia.com/file/item/202101/21/338332647849741369/f.zip"

    # 创建临时目录
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    zip_path = temp_dir / "font.zip"

    # 下载字体压缩包
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(zip_path, 'wb') as f:
        if total_size == 0:
            f.write(response.content)
        else:
            downloaded = 0
            total_size = int(total_size)
            for data in response.iter_content(chunk_size=4096):
                downloaded += len(data)
                f.write(data)
                done = int(50 * downloaded / total_size)
                print(f"\r下载进度: [{'=' * done}{' ' * (50-done)}] {downloaded}/{total_size} bytes", end='')
    print("\n下载完成！")

    # 解压文件
    print("正在解压字体文件...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # 移动字体文件
    font_file = next(temp_dir.glob("*.otf"))  # 找到 .otf 文件
    shutil.move(str(font_file), "Huiwen-mincho.otf")

    # 清理临时文件
    shutil.rmtree(temp_dir)
    print("字体文件设置完成！")

def setup():
    # 检查字体文件是否已存在
    if not Path("Huiwen-mincho.otf").exists():
        download_font()
    else:
        print("字体文件已存在，跳过下载。")

    # 创建 fonts 目录
    Path("fonts").mkdir(exist_ok=True)

    # 运行字体子集化
    print("\n开始字体子集化...")
    os.system("python font_subset.py")

if __name__ == "__main__":
    setup()
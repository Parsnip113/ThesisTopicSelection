# **🐔🧱**论文选题系统

## 项目简介

该项目旨在提供一个简洁易用的毕业论文选题信息获取和展示平台。由于某网提供的选题系统界面复杂、不够直观，本系统使用 Python 爬虫从知网论文选题页面爬取选题信息，并通过一个简洁的前端界面进行展示。

## 项目展示

[Screencast from 2024-11-16 16-22-38.webm](https://github.com/user-attachments/assets/632b4287-0a90-48e9-b6b2-cf248d7edb5f)

## 功能概述

- **数据爬取**：使用 Python 编写的爬虫程序，自动获取论文选题信息。
- **前端展示**：提供简洁直观的 HTML 页面，用于展示爬取的选题信息。
- **配置管理**：通过配置文件（`config.json`）管理爬虫所需的环境变量（如 Cookie 和 AuthToken 等），保证爬虫能够正常运行。

## 项目结构

```
.
├── config.json       # 存放爬虫所需的环境变量，如 cookie 和 authtoken 等
├── environment.yml        # conda依赖说明文件
├── crawl.py          # Python 爬虫脚本，负责获取选题信息
├── index.html        # 简洁的前端页面，展示爬取的选题信息
├── setup.py         # 安装字体
├── font_subset.py  # 字体裁剪
├── README.md         # 项目说明文件

```

## 安装和配置

### 1. 创建环境

首先，确保你的系统上已安装 Conda。

```shell
git clone https://github.com/Parsnip113/ThesisTopicSelection.git # 下载源码
cd ThesisTopicSelection


conda env create -f environment.yml # 安装依赖
conda activate jlu_topic_crawl # 启用环境
```

### 2. 配置 `config.json`

`config.json` 文件包含爬虫运行所需的环境变量（如 Cookie、AuthToken 等），请确保正确配置此文件。文件示例：

```json
{
  "COOKIE": "sadadsadaxxxxx",
  "AUTH_TOKEN": "6B6sd8dxxasxsxxxxx",
  "USER_AGENT": "xxxxxxx"
}
```

确保将示例中的 `"sadadsadaxxxxx"`,`"6B6sd8dxxasxsxxxxx"`和`"xxxxxxx"`替换为你从某网获取的有效信息。

### 3. 运行爬虫

在配置好环境变量之后，运行爬虫脚本来抓取选题数据：

```bash
python setup.py # 安装必要字体
python crawl.py # 运行爬虫获取选题信息
```

爬虫运行成功后，选题信息将被存储在一个本地 JSON 文件中，可以通过 `index.html` 页面查看。

### 4. 查看前端展示页面

```shell
python -m http.server # 开启http服务器
```

在浏览器中打开 `index.html` 文件，可以查看爬取的选题信息展示页面。

## 使用说明

1. **数据更新**：每次运行爬虫脚本，都会自动获取最新的选题信息并更新本地存储的数据。
2. **前端展示**：通过打开 `index.html` 文件，可以查看到一个简单的选题信息展示页面，展示了爬取的选题列表，便于用户快速浏览。

## 贡献

欢迎对本项目提出建议或贡献代码。你可以通过以下方式参与：

1. Fork 该项目并提交 Pull Request。
2. 提交 Issue，报告 Bug 或提出新功能需求。

---

## 其他说明

### 爬虫相关法律声明

本项目仅限于学习和研究用途，请遵守相关法律法规和知识产权保护条款。未经授权，请勿将爬虫应用于生产环境或商业目的。


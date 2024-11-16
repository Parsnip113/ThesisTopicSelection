import requests
import json
import time
import logging
import os

# 加载配置文件
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("请确保config.json文件存在")
    except json.JSONDecodeError:
        raise ValueError("config.json格式不正确")

CONFIG = load_config()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_common_headers():
    """返回通用的headers配置"""
    return {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': CONFIG['COOKIE'],
        'User-Agent': CONFIG['USER_AGENT']
    }

def get_common_data():
    """返回通用的data配置"""
    return {
        'authToken': CONFIG['AUTH_TOKEN'],
        'browserInfo': '',
        'dp': 'jlu'
    }

def get_project_list():
    url = 'https://co2.cnki.net/Handler/Project.ashx?action=GetStuChoiceProjectsList'
    headers = get_common_headers()
    data = {
        **get_common_data(),
        'isShowLoading': '0',
        'page': '1',
        'rows': '500'
    }

    try:
        logger.info('正在获取项目列表...')
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
        logger.info(f'成功获取项目列表,共 {len(result["rows"])} 个项目')
        return result
    except Exception as e:
        logger.error(f'获取项目列表失败: {str(e)}')
        raise

def get_project_details(ktbh):
    url = 'https://co2.cnki.net/Handler/Project.ashx?action=GetProjectDetails'
    headers = get_common_headers()
    data = {
        **get_common_data(),
        'ktbh': str(ktbh)
    }

    try:
        logger.debug(f'正在获取项目 {ktbh} 的详细信息...')
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f'获取项目 {ktbh} 的详细信息失败: {str(e)}')
        raise

def get_project_student_info(ktbh):
    url = 'https://co2.cnki.net/Handler/Project.ashx?action=GetProjectStuInfo'
    headers = get_common_headers()
    data = {
        **get_common_data(),
        'ktbh': str(ktbh),
        'type': '',
        'excellence': '0',
        'flag': '0',
        'mangshen': '0',
        'isCanSeeStu': '0'
    }

    try:
        logger.debug(f'正在获取项目 {ktbh} 的学生信息...')
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f'获取项目 {ktbh} 的学生信息失败: {str(e)}')
        raise

def main():
    try:
        # 检查配置文件中必要的字段是否存在
        required_fields = ['AUTH_TOKEN', 'COOKIE', 'USER_AGENT']
        missing_fields = [field for field in required_fields if field not in CONFIG]
        if missing_fields:
            raise ValueError(f"config.json 中缺少必要的配置项: {', '.join(missing_fields)}")

        logger.info('开始爬取数据...')
        start_time = time.time()

        # 获取项目列表
        project_list = get_project_list()

        # 准备数据结构存储所有信息
        complete_data = []

        # 遍历每个项目
        total_projects = len(project_list['rows'])
        for index, project in enumerate(project_list['rows'], 1):
            ktbh = project['课题编号']
            logger.info(f'正在处理第 {index}/{total_projects} 个项目 (课题编号: {ktbh})')

            # 获取详细信息
            details = get_project_details(ktbh)
            student_info = get_project_student_info(ktbh)

            # 组合信息
            project_data = {
                '基本信息': project,
                '详细信息': details['rows'][0] if details['rows'] else None,
                '学生信息': student_info['rows'][0] if student_info['rows'] else None
            }

            complete_data.append(project_data)

            # 添加延时，避免请求过于频繁
            time.sleep(1)

        # 保存到文件
        logger.info('正在保存数据到文件...')
        with open('projects_data.json', 'w', encoding='utf-8') as f:
            json.dump(complete_data, f, ensure_ascii=False, indent=2)

        end_time = time.time()
        duration = end_time - start_time
        logger.info(f'数据爬取完成! 耗时: {duration:.2f} 秒')
        logger.info(f'数据已保存到 projects_data.json')

    except Exception as e:
        logger.error(f'程序执行出错: {str(e)}')
        raise

if __name__ == '__main__':
    main()
import json
import re
from fontTools.ttLib import TTFont
from fontTools.subset import main as subsetter
from pathlib import Path
import hashlib
import unicodedata

def categorize_char(char):
    """对字符进行分类"""
    category = unicodedata.category(char)
    # Lo: Letter - Other (包括汉字)
    # Ll: Letter - Lowercase
    # Lu: Letter - Uppercase
    # Nd: Number - Decimal
    # Po: Punctuation - Other
    # Ps: Punctuation - Open
    # Pe: Punctuation - Close
    # Pd: Punctuation - Dash
    # Pi: Punctuation - Initial quote
    # Pf: Punctuation - Final quote
    # Zs: Separator - Space
    # Sm: Symbol - Math
    # Sc: Symbol - Currency
    # So: Symbol - Other
    return category

def extract_all_chars(text):
    """提取文本中的所有有效字符"""
    # 排除控制字符等
    return {char for char in text if not unicodedata.category(char).startswith('C')}

def analyze_chars(chars):
    """分析字符集组成"""
    analysis = {}
    for char in chars:
        category = categorize_char(char)
        if category not in analysis:
            analysis[category] = set()
        analysis[category].add(char)
    return analysis

def get_file_content(file_path):
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def process_json_file(json_path):
    """处理 JSON 文件中的所有字符"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    chars = set()
    
    def extract_from_dict(d):
        if isinstance(d, dict):
            for value in d.values():
                if isinstance(value, str):
                    chars.update(extract_all_chars(value))
                elif isinstance(value, (dict, list)):
                    extract_from_dict(value)
        elif isinstance(d, list):
            for item in d:
                extract_from_dict(item)
    
    extract_from_dict(data)
    return chars

def add_essential_chars():
    """添加必要的字符"""
    essential_chars = set()
    
    # 基本英文字母（大小写）
    essential_chars.update('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    
    # 数字
    essential_chars.update('0123456789')
    
    # 基本标点符号（中英文）
    essential_chars.update(',.!?:;\'\"()[]{}+-*/=_@#$%^&<>\\|～·、。！？：；""''（）【】《》￥…—')
    
    # 特殊符号
    essential_chars.update('✓✗★☆♥♦♠♣→←↑↓△▽□◇○●')
    
    # 空格和换行
    essential_chars.update(' \n\t')
    
    return essential_chars

def create_font_subset(original_font_path, output_path, text):
    """创建字体子集"""
    # 将文本写入临时文件
    temp_txt = 'temp_chars.txt'
    with open(temp_txt, 'w', encoding='utf-8') as f:
        f.write(''.join(sorted(text)))
    
    # 使用 fonttools 的 subset 模块创建子集
    subsetter([
        str(original_font_path),
        f'--text-file={temp_txt}',
        f'--output-file={output_path}',
        '--layout-features=*',
        '--name-languages=*',
        '--name-IDs=*',
        '--name-legacy',
        '--legacy-kern',
        '--notdef-outline',
        '--no-hinting',
        '--desubroutinize',
    ])
    
    # 删除临时文件
    Path(temp_txt).unlink()

def calculate_file_size(file_path):
    """计算文件大小并返回人类可读的格式"""
    size_bytes = Path(file_path).stat().st_size
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} GB"

def calculate_text_hash(text):
    """计算文本的 MD5 hash"""
    return hashlib.md5(''.join(sorted(text)).encode()).hexdigest()[:8]

def save_char_analysis(chars, filename):
    """保存字符分析结果"""
    analysis = analyze_chars(chars)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("字符集分析报告\n")
        f.write("=" * 50 + "\n\n")
        
        total_chars = len(chars)
        f.write(f"总字符数: {total_chars}\n\n")
        
        for category, char_set in analysis.items():
            category_desc = {
                'Lo': '其他字母（如汉字）',
                'Ll': '小写字母',
                'Lu': '大写字母',
                'Nd': '数字',
                'Po': '其他标点',
                'Ps': '左括号类',
                'Pe': '右括号类',
                'Pd': '破折号类',
                'Pi': '左引号类',
                'Pf': '右引号类',
                'Zs': '空格',
                'Sm': '数学符号',
                'Sc': '货币符号',
                'So': '其他符号'
            }.get(category, category)
            
            f.write(f"\n{category} ({category_desc}):\n")
            f.write(f"数量: {len(char_set)}\n")
            f.write(f"字符: {''.join(sorted(char_set))}\n")
            f.write("-" * 50 + "\n")

def main():
    # 配置路径
    html_path = 'index.html'
    json_path = 'projects_data.json'
    original_font_path = 'Huiwen-mincho.otf'
    
    # 使用固定的输出文件名
    output_font_path = 'fonts/Huiwen-mincho-subset.otf'
    analysis_file = 'fonts/charset_analysis.txt'
    
    # 确保 fonts 目录存在
    Path('fonts').mkdir(exist_ok=True)
    
    print("开始收集字符...")
    
    # 收集所有字符
    all_chars = set()
    
    # 从 HTML 文件中提取
    print("正在处理 HTML 文件...")
    html_content = get_file_content(html_path)
    all_chars.update(extract_all_chars(html_content))
    
    # 从 JSON 文件中提取
    print("正在处理 JSON 文件...")
    all_chars.update(process_json_file(json_path))
    
    # 添加必要的字符
    print("添加必要的字符...")
    all_chars.update(add_essential_chars())
    
    # 创建字体子集
    print(f"正在创建字体子集，共 {len(all_chars)} 个字符...")
    create_font_subset(original_font_path, output_font_path, all_chars)
    
    # 保存字符分析报告
    save_char_analysis(all_chars, analysis_file)
    
    # 输出结果
    original_size = calculate_file_size(original_font_path)
    subset_size = calculate_file_size(output_font_path)
    
    print("\n处理完成！")
    print(f"原始字体大小: {original_size}")
    print(f"子集字体大小: {subset_size}")
    print(f"字体文件已保存为: {output_font_path}")
    print(f"字符集分析报告已保存到: {analysis_file}")

if __name__ == '__main__':
    main()

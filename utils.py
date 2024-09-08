import webbrowser
import urllib.parse
import platform
import subprocess
import re
from urllib.parse import unquote, quote

def open_search_page(keywords):
    """
    使用给定的关键词打开万方数据专利搜索页面
    
    :param keywords: 搜索关键词
    """
    encoded_keywords = urllib.parse.quote(keywords)
    url = f'https://s.wanfangdata.com.cn/patent?q={encoded_keywords}'
    webbrowser.open(url)



def validate_patent_number(patent_no):
    """
    验证专利号格式
    
    规则：
    1. 可以带有或不带有前缀 'CN'
    2. 不能包含除 'CN' 以外的其他字母
    3. 数字部分必须以年份（4位数字）开头
    4. 总长度（包括可能的 'CN' 前缀）不少于12个字符
    5. 格式应该类似于 CN202311303481.9 或 202311303481.9
    
    :param patent_no: 要验证的专利号
    :return: 如果专利号有效返回 True，否则返回错误信息字符串
    """
    # 移除可能的空格
    patent_no = patent_no.strip()
    
    # 检查是否包含除 'CN' 以外的其他字母
    if re.search(r'[a-zA-Z]', patent_no.replace('CN', '', 1)):
        return "专利号不能包含除 'CN' 以外的其他字母"
    
    # 检查是否以 'CN' 开头，如果是，则移除
    if patent_no.upper().startswith('CN'):
        patent_no = patent_no[2:]
    
    # 使用正则表达式验证格式
    pattern = r'^(20\d{2})\d{7,8}\.\d$'
    
    if not re.match(pattern, patent_no):
        return "专利号格式不正确，应为 'CN' + 4位年份 + 7-8位数字 + '.' + 1位数字"
    
    # 检查总长度（包括可能的 'CN' 前缀）
    total_length = len(patent_no) + (2 if patent_no.upper().startswith('CN') else 0)
    if total_length < 12:
        return "专利号总长度（包括可能的 'CN' 前缀）不能少于12个字符"
    
    return True



def open_image(image_path):
    """
    跨平台打开图片文件
    """
    system = platform.system()

    if system == 'Darwin':  # macOS
        subprocess.call(('open', image_path))
    elif system == 'Windows':  # Windows
        os.startfile(image_path)
    else:  # Linux 和其他系统
        try:
            subprocess.call(('xdg-open', image_path))
        except FileNotFoundError:
            # 如果 xdg-open 不可用，尝试使用其他常见的图片查看器
            viewers = ['display', 'feh', 'eog', 'xv']
            for viewer in viewers:
                try:
                    subprocess.call((viewer, image_path))
                    break
                except FileNotFoundError:
                    continue
            else:
                print("无法打开图片文件。请手动打开：", image_path)


def smart_unquote(s):
    """智能解码URL编码的字符串"""
    while '%' in s:
        s = unquote(s)
    return s


def retry_or_exit():
    while True:
        choice = input("是否重试？(Y/N): ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("无效输入，请输入 Y 或 N")


def check_local_patent(patent_no):
    """检查本地是否存在包含指定专利号的文件"""
    if not os.path.exists(DIR_PATH):
        print(f"警告: 目录 {DIR_PATH} 不存在")
        return None

    print(f"正在检查目录: {DIR_PATH}")
    patent_no = re.escape(patent_no)  # 转义特殊字符
    pattern = re.compile(rf'.*{patent_no}.*\.pdf', re.IGNORECASE)

    for filename in os.listdir(DIR_PATH):
        print(f"检查文件: {filename}")
        if pattern.match(filename):
            full_path = os.path.join(DIR_PATH, filename)
            print(f"找到匹配文件: {full_path}")
            return full_path

    print(f"未找到包含专利号 {patent_no} 的文件")
    return None


def print_menu(title, options):
    """打印美化的菜单"""
    print("\n" + "=" * 40)
    print(f"{title:^40}")
    print("=" * 40)
    for key, value in options.items():
        print(f"{key}. {value}")
    print("=" * 40)
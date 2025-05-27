import pandas as pd
import zipfile
import os
import csv
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='tiktok_download.log'
)

# 判断文件类型
def check_file_type(file_path):
    with open(file_path, 'rb') as f:
        header = f.read(4)
    
    # 检查是否是ZIP文件（PK头）
    if header[:2] == b'PK':
        return 'zip'
    
    # 尝试作为文本文件读取前几行
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if ',' in first_line or ';' in first_line or '\t' in first_line:
                return 'text'
    except UnicodeDecodeError:
        pass
    
    return 'unknown'

# 处理ZIP文件
def process_zip_file(zip_path):
    extract_folder = os.path.splitext(zip_path)[0] + "_extracted"
    os.makedirs(extract_folder, exist_ok=True)
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
        
        # 查找CSV文件
        for root, dirs, files in os.walk(extract_folder):
            for file in files:
                if file.endswith('.csv'):
                    csv_path = os.path.join(root, file)
                    print(f"在ZIP文件中找到CSV: {csv_path}")
                    return csv_path
        
        # 如果没有CSV，查找可能包含URL的文本文件
        for root, dirs, files in os.walk(extract_folder):
            for file in files:
                if file.endswith('.txt'):
                    txt_path = './url.txt'
                    print(f"在ZIP文件中找到文本文件: {txt_path}")
                    # 转换为CSV
                    csv_path = txt_to_csv(txt_path)
                    if csv_path:
                        return csv_path
    except Exception as e:
        print(f"解压ZIP文件时出错: {e}")
    
    return None

# 将文本文件转换为CSV
def txt_to_csv(txt_path):
    urls = []
    
    # 尝试从文本文件中提取URL
    try:
        with open(txt_path, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                line = line.strip()
                if line.startswith('http'):
                    urls.append(line)
    except Exception as e:
        print(f"读取文本文件时出错: {e}")
    
    if urls:
        # 创建CSV文件
        csv_path = os.path.splitext(txt_path)[0] + ".csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['url'])  # 标题行
            for url in urls:
                writer.writerow([url])
        print(f"从文本文件中提取了{len(urls)}个URL并创建了CSV文件")
        return csv_path
    
    return None

# 手动输入URL
def manual_input_urls():
    print("\n没有找到有效的URL文件。请手动输入TikTok URL (每行一个，输入空行结束):")
    urls = []
    while True:
        url = input().strip()
        if not url:
            break
        if url.startswith('http'):
            urls.append(url)
        else:
            print(f"忽略无效URL: {url}")
    
    if not urls:
        return None
    
    # 创建CSV文件
    csv_path = "manual_tiktok_urls.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['url'])  # 标题行
        for url in urls:
            writer.writerow([url])
    print(f"已创建包含{len(urls)}个URL的CSV文件")
    return csv_path

# 主函数
def main():
    # 原始文件路径
    original_file_path = './E28_E25_KOL_AI打分标准 - 视频链接.csv'  # 替换为您的文件路径
    
    # 检查文件类型
    file_type = check_file_type(original_file_path)
    print(f"检测到的文件类型: {file_type}")
    
    url_csv_path = None
    
    if file_type == 'zip':
        # 处理ZIP文件
        url_csv_path = process_zip_file(original_file_path)
    elif file_type == 'text':
        # 直接使用文本文件
        url_csv_path = original_file_path
    
    # 如果仍然没有找到有效的CSV文件，请求手动输入
    if not url_csv_path:
        url_csv_path = manual_input_urls()
    
    if not url_csv_path:
        print("无法获取TikTok URL列表，程序退出。")
        return
    
    # 设置视频下载路径
    video_download_path = 'downloaded_videos'
    os.makedirs(video_download_path, exist_ok=True)
    
    # 修改GetTiktokVideo类的get_url_list方法
    from TT.get_video import GetTiktokVideo
    
    # 重写get_url_list方法，使其更健壮
    original_get_url_list = GetTiktokVideo.get_url_list
    
    def robust_get_url_list(self, url_csv_path):
        import re
        
        # 尝试不同的编码和分隔符
        encodings = ['utf-8', 'iso-8859-1', 'gbk', 'gb2312', 'latin1']
        separators = [',', ';', '\t']
        
        for encoding in encodings:
            for sep in separators:
                try:
                    df = pd.read_csv(url_csv_path, encoding=encoding, sep=sep, on_bad_lines='skip')
                    
                    # 检查是否有'url'列
                    if 'url' in df.columns:
                        urls = df['url'].dropna().tolist()
                    else:
                        # 查找可能的URL列
                        possible_url_cols = [col for col in df.columns if 'url' in col.lower() or 'link' in col.lower()]
                        
                        if possible_url_cols:
                            # 使用第一个可能的URL列
                            urls = df[possible_url_cols[0]].dropna().tolist()
                        else:
                            # 检查每一列是否包含URL
                            urls = []
                            for col in df.columns:
                                col_urls = [val for val in df[col].dropna().tolist() 
                                           if isinstance(val, str) and val.startswith('http')]
                                urls.extend(col_urls)
                    
                    # 验证URL
                    valid_urls = [url for url in urls if isinstance(url, str) and url.startswith('http')]
                    
                    if valid_urls:
                        print(f"使用编码 {encoding} 和分隔符 '{sep}' 成功读取了{len(valid_urls)}个URL")
                        return valid_urls
                
                except Exception as e:
                    print(f"使用编码 {encoding} 和分隔符 '{sep}' 读取失败: {e}")
        
        # 如果所有方法都失败，尝试直接从文件中提取URL
        try:
            with open(url_csv_path, 'r', encoding='latin1', errors='replace') as f:
                content = f.read()
            
            # 使用正则表达式提取URL
            urls = re.findall(r'https?://[^\s,"\';]+', content)
            
            if urls:
                print(f"通过文本分析提取了{len(urls)}个URL")
                return urls
        except Exception as e:
            print(f"直接从文件提取URL失败: {e}")
        
        # 如果还是失败，返回空列表
        print("无法从文件中提取任何有效URL")
        return []
    
    # 替换方法
    GetTiktokVideo.get_url_list = robust_get_url_list
    
    # 创建下载器并开始下载
    try:
        downloader = GetTiktokVideo(url_csv_path, video_download_path)
        if downloader.url_list:
            print(f"开始下载{len(downloader.url_list)}个TikTok视频...")
            downloader.download_video()
        else:
            print("没有找到有效的URL，无法开始下载")
    except Exception as e:
        print(f"下载过程中出错: {e}")

if __name__ == "__main__":
    main()
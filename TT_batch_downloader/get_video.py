from tiktok_data_collector import TikTokVideoCollector
import time
import pandas as pd
import csv
import os
import logging

class GetTiktokVideo:

    def __init__(self, url_csv_path, video_download_path):
        self.url_list = self.get_url_list(url_csv_path)
        self.video_download_path = video_download_path  # directory to download videos
        #self.id2url = "video/id2url.csv"
        #self.create_csv_with_headers(self.id2url)

    def get_url_list(self, url_csv_path):
        # 尝试使用ISO-8859-1编码，这是最通用的编码之一
        try:
            df = pd.read_csv(url_csv_path, encoding='iso-8859-1', on_bad_lines='skip')
            
            # 检查是否有'url'列
            if 'url' not in df.columns:
                # 如果没有'url'列，尝试推断列名（可能是第一行数据被误认为是标题）
                possible_url_columns = [col for col in df.columns if 'url' in col.lower() or 'link' in col.lower()]
                
                if possible_url_columns:
                    # 如果找到可能的URL列，使用第一个
                    url_column = possible_url_columns[0]
                    print(f"未找到'url'列，但找到了可能的URL列：'{url_column}'")
                else:
                    # 如果没有找到可能的URL列，尝试使用第一列
                    url_column = df.columns[0]
                    print(f"未找到'url'列，将使用第一列：'{url_column}'")
                
                urls = df[url_column].dropna().tolist()
            else:
                # 正常处理'url'列
                urls = df['url'].dropna().tolist()
            
            # 验证URL列表是否有效
            valid_urls = []
            for url in urls:
                # 检查是否是字符串类型
                if isinstance(url, str):
                    # 简单验证URL格式
                    if url.startswith('http') or url.startswith('www'):
                        valid_urls.append(url)
                    else:
                        print(f"忽略无效URL: {url}")
            
            print(f"成功读取了{len(valid_urls)}个有效URL")
            return valid_urls
            
        except Exception as e:
            print(f"读取CSV文件时出错: {e}")
            
            # 如果失败，尝试以文本方式读取文件并提取URL
            try:
                with open(url_csv_path, 'r', encoding='iso-8859-1') as f:
                    content = f.read()
                
                # 使用正则表达式提取URL
                import re
                urls = re.findall(r'https?://[^\s,"\';]+', content)
                
                if urls:
                    print(f"通过文本分析提取了{len(urls)}个URL")
                    return urls
                else:
                    raise ValueError("无法从文件中提取URL")
            
            except Exception as e2:
                print(f"尝试文本分析也失败: {e2}")
                raise ValueError(f"无法读取URL列表: {e}, {e2}")
        
        

    def retry_collect(self, collector, url, download_path, max_retries=3, delay=5):
        """
        带有重试机制的收集器调用函数。

        Args:
            collector: 收集器对象（如 TikTokVideoCollector、TikTokAudioCollector 等）。
            url: 要收集数据的 TikTok 视频 URL。
            download_path: 下载文件的存储路径。
            max_retries: 最大重试次数。
            delay: 每次重试之间的延迟时间（秒）。

        Returns:
            如果成功，则返回收集到的数据；否则返回 None。
        """
        retries = 0
        while retries < max_retries:
            result = collector.collect(url, download_path)
            if result is not None:
                return result
            retries += 1
            print(f"重试第 {retries} 次，等待 {delay} 秒后重试...")
            time.sleep(delay)
        print(f"在重试了 {max_retries} 次后仍然失败。")
        return ("","")

 
    # 创建一个包含表头的 CSV 文件
    def create_csv_with_headers(self, csv_file_path):
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # 写入表头
            writer.writerow(['url', 'video_path'])

    # 插入一条数据到 CSV 文件
    def insert_row_to_csv(self, csv_file_path, row):
        if len(row) != 2:
            raise ValueError("每一行数据必须包含两个元素")
        
        # 读取现有的CSV文件内容
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            existing_rows = list(reader)
            
        # 判断该行数据是否已经存在
        if row in existing_rows:
            print("该行数据已存在，跳过插入。")
            return
        
        # 如果不存在，才插入该行数据
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(row)
            print("成功插入新行数据。")


    def download_video(self):
        max_videos_per_folder = 100
        #video_base_path = 'data/eufylights/video'
        video_base_path = self.video_download_path
        #download_count = 0
        for index, url in enumerate(self.url_list):
            # log info
            logging.info(f"Start Downloading '{url}'.")

            # Calculate the subfolder index based on the current video index (starting from 1)
            subfolder_index = (index // max_videos_per_folder) + 1
            subfolder_name = f'video{subfolder_index}'
            subfolder_path = os.path.join(video_base_path, subfolder_name)

            # Create the subfolder if it doesn't exist
            os.makedirs(subfolder_path, exist_ok=True)

            # Set the path to the CSV file in the current subfolder
            csv_path = os.path.join(subfolder_path, "id2url.csv")

            # Load existing URLs from the CSV file (if it exists) into a set
            existing_urls = set()
            if os.path.exists(csv_path):
                # If the CSV already exists, load its content to avoid duplicates
                with open(csv_path, mode='r', newline='') as file:
                    reader = csv.reader(file)
                    next(reader, None)  # Skip header
                    for row in reader:
                        if row:
                            existing_urls.add(row[0])  # Add the URL to the set
            else:
                # If the CSV does not exist, create it and add a header
                with open(csv_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["url", "Video Path"])  # Add a header row for CSV

            # Check if the current URL is already processed (i.e., in id2url.csv)
            if url in existing_urls:
                logging.info(f"Video for URL {url} already exists in id2url.csv. Skipping download.")
                continue

            # Update the video download path to include the subfolder
            tiktok_video_collector = TikTokVideoCollector()

            # Collect video data and handle return values
            video, metadata = self.retry_collect(tiktok_video_collector, url, subfolder_path)
            if not video:
                #print(f"视频 {url} 收集失败。")
                logging.info(f"视频 {url} 收集失败。")
                continue
            
            # Check if the video file already exists in the target folder
            video_filename = os.path.join(subfolder_path, f"{metadata.id}.mp4")
            # if os.path.exists(video_filename):
            #     logging.info(f"Video file {video_filename} already exists. Skipping download.")
            #     #print(f"Video file {video_filename} already exists. Skipping download.")
            #     continue

            # Print all the metadata collected from TikTok
            print(metadata)
            print('video download path:' + video.downloaded_path)
            # Append the URL and video metadata to the CSV file within the same subfolder
            with open(csv_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([url, video_filename])

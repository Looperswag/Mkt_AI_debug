# run_video_processing/video_utils.py
import cv2

def format_time(seconds):
    """将秒数格式化为 HH:MM:SS 格式"""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{seconds:.2f}"

def format_duration(seconds):
    """将秒数格式化为 xx min, xx s 格式"""
    minutes, seconds = divmod(int(seconds), 60)
    if minutes > 0:
        return f"{minutes} min, {seconds} s"
    else:
        return f"{seconds} s"

def get_video_duration(video_path):
    """获取视频文件的时长（以秒为单位）"""
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"无法打开视频文件: {video_path}")
            return 0.0
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if fps > 0:
            duration = frame_count / fps
        else:
            duration = 0.0
        cap.release()
        return duration
    except Exception as e:
        print(f"获取视频时长失败: {e}")
        return 0.0
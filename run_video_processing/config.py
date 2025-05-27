# run_video_processing/config.py

KEY_PATH = "../idc-ipc-1dc332fa2fe3.json" # 确保路径正确

DEFAULT_GEMINI_PROJECT_ID = "idc-ipc"
DEFAULT_GEMINI_LOCATION = "global"

VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
# 移除了 DEFAULT_SCENE_DETECT_THRESHOLD 和 DEFAULT_MIN_SCENE_LENGTH_FRAMES
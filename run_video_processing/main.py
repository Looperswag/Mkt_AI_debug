# run_video_processing/main.py
import os
import sys

from .video_labeler import label_entire_videos # 注意函数名已更改
from . import config

if __name__ == "__main__":
    print("--- 视频批量标注程序 ---") # 更新程序名称

    key_path_from_config = config.KEY_PATH
    potential_key_path = ""
    if os.path.isabs(key_path_from_config):
        potential_key_path = key_path_from_config
    else:
        potential_key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), key_path_from_config))

    if not os.path.exists(potential_key_path):
        print(f"错误：Google API 密钥文件在配置的路径未找到: {potential_key_path}")
        project_root_guess = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        alternate_key_path = os.path.join(project_root_guess, os.path.basename(key_path_from_config))
        if os.path.exists(alternate_key_path):
            print(f"提示：在备用项目根目录位置找到密钥文件: {alternate_key_path}")
            potential_key_path = alternate_key_path
        else:
            print(f"错误：备用路径 {alternate_key_path} 也未找到密钥文件。")
            print(f"请在 run_video_processing/config.py 中正确配置 KEY_PATH，或将密钥文件放置在项目根目录。")
            sys.exit(1)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = potential_key_path

    user_name = input("请输入您的英文名（全部小写，例如 'testuser'）：").lower().strip()
    if not user_name:
        print("错误：未输入用户名。")
        sys.exit(1)

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    user_base_folder = os.path.join(project_root, 'user')
    user_specific_folder = os.path.join(user_base_folder, user_name)

    if not os.path.exists(user_specific_folder):
        try:
            os.makedirs(user_specific_folder)
            print(f"已为您创建好文件夹: {user_specific_folder}")
            print("请传入待打标视频文件到相应的 'original_scene' 文件夹后重新运行程序。")
            sys.exit(0)
        except OSError as e:
            print(f"错误：无法创建用户文件夹 {user_specific_folder}: {e}")
            sys.exit(1)
    else:
        print(f"用户文件夹 {user_specific_folder} 已存在，继续处理。")

    input_video_folder = os.path.join(user_specific_folder, 'original_scene')
    # 输出文件夹名可以保持不变，或者改为更通用的名字如 'Labeled_Videos'
    output_result_folder = os.path.join(user_specific_folder, 'Result_folder_labeled') # 可以改名

    for folder_path in [input_video_folder, output_result_folder]:
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                print(f"已创建子文件夹: {folder_path}")
                if folder_path == input_video_folder:
                    print(f"请确保视频文件已放入 {input_video_folder} 中。")
            except OSError as e:
                print(f"错误：无法创建子文件夹 {folder_path}: {e}")
                sys.exit(1)
    
    if not os.listdir(input_video_folder):
        print(f"提示：输入文件夹 {input_video_folder} 为空。请添加视频文件后再运行。")
        sys.exit(0)

    print(f"\n配置信息:")
    print(f"  输入视频文件夹: {input_video_folder}")
    print(f"  输出结果文件夹: {output_result_folder}")
    # 移除了场景检测相关的配置打印

    # 调用已修改的核心处理函数
    label_entire_videos( # 注意函数名已更改
        input_folder=input_video_folder,
        output_folder=output_result_folder,
        project_id=config.DEFAULT_GEMINI_PROJECT_ID,
        location=config.DEFAULT_GEMINI_LOCATION
    )
    print("--- 程序执行完毕 ---")
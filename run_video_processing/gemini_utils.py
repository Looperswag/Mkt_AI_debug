# run_video_processing/gemini_utils.py
import os
from google import genai
from google.genai import types

def setup_gemini_client(project_id="your_project_id", location="your_location"):
    """
    设置并返回 Gemini API 客户端。
    """
    client = genai.Client(
        vertexai=True,
        project=project_id,
        location=location,
    )
    return client

def label_video_with_gemini(client, video_path):
    """
    使用 Gemini API 对视频进行标注。
    """
    try:
        with open(video_path, "rb") as f:
            video_data = f.read()
        
        video_part = types.Part.from_bytes(
            data=video_data,
            mime_type="video/mp4",
        )
        
        prompt = '''
        请分析此扫地机器人产品视频，并根据以下四个标准进行打标。每个标准输出“合格”或“不合格”。

        在此处填写标签需求；可用1、2、3、4分点来描述
        '''
        text_part = types.Part.from_text(text=prompt)
        
        contents = [
            types.Content(
                role="user",
                parts=[
                    video_part,
                    text_part
                ]
            )
        ]
        
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            seed=0,
            max_output_tokens=8192,
            response_modalities=["TEXT"],
        )
        
        model = "gemini-2.5-flash-preview-05-20" # 注意：这里可能需要根据实际可用的模型更新
        
        response_text = ""
        # 注意：以下调用 client.models.generate_content_stream 依赖于您 genai 库版本和客户端对象的结构。
        # 如果 genai.Client(vertexai=True) 返回的客户端对象不支持此方法，
        # 您可能需要调整为 client.get_generative_model(model).generate_content(..., stream=True) 或类似方法。
        # 此处保留原始脚本中的流式 API 调用方式。
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config, # 参数名在某些版本中可能是 generation_config
        ):
            if chunk.text:
                response_text += chunk.text
        
        print(f"Gemini 原始标签: {response_text}")
        return response_text.strip()
        
    except Exception as e:
        print(f"Gemini API 调用失败: {e}")
        # 考虑打印更详细的错误信息，例如 e.__traceback__
        return "标签生成失败"

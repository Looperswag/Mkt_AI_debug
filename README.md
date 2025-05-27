# Mkt短视频中台AI审核分析工具集 V1.0 🚀

旨在帮助用户高效地从网络平台（如 TikTok）批量下载短视频，并利用先进的 AI 多模态技术对视频内容进行自动化审核与标签化处理。

**主要组件:**

1.  **TikTok 数据收集器 (`tiktok_downloader_module`)**:
    *   一个用于批量下载 TikTok 视频及其元数据的工具。
    *   支持从多种格式的URL列表（CSV, TXT, ZIP压缩包）或手动输入中读取视频链接。
    *   核心下载功能由 `yt-dlp` 驱动。
2.  **AI 视频内容审核系统 (`run_video_processing_module`)**:
    *   利用 Google Gemini 多模态 AI 模型对视频内容进行自动化审核。
    *   根据预设标准（如环境、特定功能展示、品牌识别等）为视频打上“合格”或“不合格”的标签，并给出最终审核评分。
    *   生成详细的 HTML 和 JSON 处理报告。

**目录层级假设:**

为了使以下说明清晰，我们假设您的项目目录结构如下：

    your_project_root/
    ├── tiktok_downloader_module/      # TikTok 数据收集器相关代码
    │   ├── main.py
    │   ├── tiktok_data_collector.py
    │   ├── models.py
    │   └── TT/                       # 假设的 GetTiktokVideo 模块所在目录
    │       └── get_video.py          # (此文件内容未提供，但被 main.py 引用)
    ├── run_video_processing_module/   # AI 视频内容审核系统相关代码
    │   ├── main.py
    │   ├── video_labeler.py
    │   ├── gemini_utils.py
    │   ├── video_utils.py
    │   ├── report_generator.py
    │   └── config.py
    ├── iit-ai-f2161462981d.json       # (示例名) Google API 密钥，供审核系统使用
    └── README.md                      # 本文件


---

## 模块一：TikTok 数据收集器 (`tiktok_downloader_module`) 📥

此模块专注于从 TikTok 批量下载视频及其关联的元数据。

### ✨ 功能特性 (TikTok 下载器)

*   **批量下载**: 支持从列表一次性下载多个 TikTok 视频。
*   **强大的下载核心**: 使用 `yt-dlp` 库获取视频信息并执行下载，保证了较高的成功率和对平台变化的适应性。
*   **灵活的 URL 输入源**:
    *   可以直接读取 CSV 文件中的 URL 列表。
    *   能够处理包含 CSV 或 TXT 文件的 ZIP 压缩包。
    *   如果未提供文件或文件无效，支持用户手动逐行输入 URL。
*   **智能文件处理**:
    *   自动检测输入文件类型（ZIP, 文本/CSV）。
    *   对 ZIP 文件进行解压并查找内部的 URL 文件。
    *   将纯文本文件中的 URL 列表转换为临时的 CSV 格式进行处理。
*   **健壮的 CSV 解析**: `main.py` 中的逻辑会尝试多种编码和分隔符来读取 CSV 文件，提高了对不同格式 CSV 的兼容性。
*   **元数据提取**: 下载视频的同时，提取关键元数据，如视频 ID、标题、时长、观看次数、作者、描述和发布日期 (存储在 `Metadata` 对象中)。
*   **结构化数据模型 (`models.py`)**: 定义了 `Video`, `Metadata` 等类来组织收集到的数据。
*   **日志记录**: 将下载过程中的关键信息和错误记录到 `tiktok_download.log` 文件中。
*   **路径管理**: 自动创建 `downloaded_videos` 文件夹用于存放下载的视频。

### 📁 文件结构 (TikTok 下载器)

    your_project_root/
    └── tiktok_downloader_module/
    │   ├── main.py                     # 主程序入口，处理输入、调用下载
    │   ├── tiktok_data_collector.py    # 包含 TikTokVideoCollector 类，执行下载
    │   ├── models.py                   # 定义数据模型 (Video, Metadata 等)
    │   ├── TT/
    │   │   └── get_video.py            # (推测) 包含 GetTiktokVideo 类，被 main.py 修改和使用
    │   ├── E28_E25_KOL_AI打分标准 - 视频链接.csv # (示例) 默认的输入URL列表文件
    │   ├── downloaded_videos/          # (自动创建) 存放下载视频的目录
    │   └── tiktok_download.log         # (自动创建) 下载日志文件


### 🔧 环境准备 (TikTok 下载器)

1.  **Python**: Python 3.7 或更高版本。
2.  **yt-dlp**:
    *   `yt-dlp` 是一个强大的命令行下载工具。Python 脚本通过其库接口进行调用。
    *   通常，安装 `yt-dlp` Python 包即可：`pip install yt-dlp`
3.  **Pandas**: 用于处理 CSV 文件。
    *   安装：`pip install pandas`

### 🛠️ 安装与配置 (TikTok 下载器)

1.  **获取代码**: 克隆或下载 `tiktok_downloader_module` 文件夹到您的项目目录。
2.  **安装依赖**:
    ```bash
    pip install yt-dlp pandas
    ```
3.  **准备 URL 列表文件**:
    *   默认情况下，`main.py` 会尝试读取位于 `tiktok_downloader_module` 目录下的 `E28_E25_KOL_AI打分标准 - 视频链接.csv` 文件。
    *   您可以修改 `main.py` 中 `original_file_path` 变量指向您的 URL 列表文件。
    *   文件可以是 `.csv` (包含名为 `url` 的列，或其他可被智能识别的URL列)，`.txt` (每行一个URL)，或包含这类文件的 `.zip` 压缩包。

### 🚀 使用方法 (TikTok 下载器)

1.  **确保文件和目录就位**:
    *   将 `tiktok_downloader_module` 文件夹放置在您的项目根目录。
    *   确保您的 URL 列表文件 (例如 `E28_E25_KOL_AI打分标准 - 视频链接.csv`) 放在 `tiktok_downloader_module` 目录下，或者修改 `main.py` 中的路径。
2.  **运行下载脚本**:
    在项目根目录下，打开终端并执行：
    ```bash
    python -m tiktok_downloader_module.main
    ```
    *   脚本会自动检测输入文件类型。
    *   如果文件无效或未找到，会提示您手动输入 TikTok URL。
    *   下载过程中的信息会打印到控制台，并记录在 `tiktok_download.log`。
3.  **查看结果**:
    *   下载的视频文件将保存在 `tiktok_downloader_module/downloaded_videos/` 目录下，文件名通常为 `<视频ID>.mp4`。
    *   查看 `tiktok_downloader_module/tiktok_download.log` 获取详细的下载日志。

### 📝 注意事项 (TikTok 下载器)

*   **`TT/get_video.py` 模块**: `main.py` 引用了 `from TT.get_video import GetTiktokVideo` 并对其 `get_url_list` 方法进行了动态修改（Monkey Patching），以增强 URL 列表的读取能力。这意味着项目中应存在一个 `TT` 子目录及 `get_video.py` 文件，其中定义了 `GetTiktokVideo` 类。**此文件的具体实现未在您提供的内容中给出，但它是下载流程能完整运行的关键部分。**
*   **Cookies**: `tiktok_data_collector.py` 中提到了 `cookies.txt` 和 `cookiesfrombrowser` 选项（主要在 INS 视频测试的注释部分）。对于某些需要登录才能访问的 TikTok 内容，配置 Cookie 可能是必要的。当前脚本主要针对公开视频。
*   **平台限制与IP封禁**: 大量频繁下载可能导致被 TikTok 平台限制速率或封禁 IP。`yt-dlp` 内置了一些反制措施，但仍需谨慎使用。
*   **法律与版权**: 请确保您有权下载和使用这些视频内容，遵守相关法律法规和平台的服务条款。

---

## 模块二：AI 视频内容审核系统 (`run_video_processing_module`) 🤖👁️

此模块利用 Google Gemini AI 对视频内容进行自动化审核和评分。

*(这部分内容与您上一个请求中生成的 README 高度相似，并已根据当前上下文调整。)*

### ✨ 功能特性 (AI 审核系统)

*   **批量视频处理**: 支持处理指定文件夹内的所有视频文件。
*   **AI 多模态分析**: 集成 Google Gemini API，对完整的视频内容进行深度理解和分析。
*   **自定义审核标准**:
    *   通过精心设计的提示词 (Prompt)，引导 Gemini 模型根据多维度标准进行评估。
    *   当前版本针对特定产品（如扫地机器人广告）设定了四个审核维度：拍摄环境、特定功能/认证展示、特定文案/口播出现、品牌识别。
*   **结构化标签输出**: Gemini 模型为每个审核维度输出“合格”或“不合格”的明确标签。
*   **最终审核评分**: 根据各维度标签自动计算视频的总体“最终得分”。
*   **自动化文件命名**: 处理后的视频将根据原始文件名和部分AI生成的标签信息进行重命名。
*   **用户隔离的文件管理**:
    *   启动时要求输入用户名，为不同用户创建独立的输入和输出文件夹结构。
*   **详尽的处理报告**:
    *   **HTML 报告**: 包含处理摘要、各视频详情、最终得分及**内嵌视频播放器**。
    *   **JSON 摘要**: 提供机器可读的处理结果。
*   **模块化代码结构** 与 **灵活配置**。

### 📁 文件结构 (AI 审核系统)

    your_project_root/
    └── run_video_processing_module/
        ├── __init__.py
        ├── main.py                 # 程序主入口
        ├── video_labeler.py        # 核心视频标注逻辑
        ├── gemini_utils.py         # Gemini API 交互
        ├── video_utils.py          # 视频处理辅助函数
        ├── report_generator.py     # 报告生成
        └── config.py               # 配置文件


以及用户数据目录：

    your_project_root/
    └── user/                               # 用户数据根目录 (自动创建)
        └── <username>/                     # 特定用户的文件夹
            ├── original_scene/             # 存放待审核的原始视频文件
            └── Result_folder_labeled/      # 存放审核结果和报告
                ├── <original_video_name_1>/
                │   └── <processed_video_1.mp4>
                ├── processing_report.html
                └── processing_summary.json


并且，Google API 密钥文件 (例如 `iit-ai-f2161462981d.json`) 应放置在 `your_project_root/` 目录下。

### 🔧 环境准备 (AI 审核系统)

1.  **Python**: Python 3.7+。
2.  **Google Cloud Platform (GCP) 项目**: 启用 Vertex AI API。
3.  **Google API 服务账号密钥**: JSON 格式，具有 Vertex AI 访问权限。
4.  **FFmpeg (推荐)**: `opencv-python` 可能依赖它处理视频。

### 🛠️ 安装与配置 (AI 审核系统)

1.  **获取代码**: 克隆或下载 `run_video_processing_module` 文件夹。
2.  **安装 Python 依赖**:
    ```bash
    pip install google-generativeai opencv-python
    ```
3.  **配置 API 密钥**:
    *   将您的 Google API 服务账号 JSON 密钥文件放置在项目根目录下 (与 `run_video_processing_module` 文件夹同级)。
    *   确保 `run_video_processing_module/config.py` 中的 `KEY_PATH` (默认为 `../your-key-name.json`) 正确指向此密钥文件。例如，如果您的密钥文件名为 `iit-ai-f2161462981d.json`，则 `KEY_PATH` 应为 `../iit-ai-f2161462981d.json`。
4.  **检查/修改配置 (`config.py`)**:
    *   确认 `KEY_PATH`。
    *   可修改 `DEFAULT_GEMINI_PROJECT_ID` 和 `DEFAULT_GEMINI_LOCATION`。

### 🚀 使用方法 (AI 审核系统)

1.  **准备视频文件**:
    *   程序首次运行时会根据您输入的用户名在 `your_project_root/user/` 下创建相应文件夹。
    *   将待审核的视频放入 `your_project_root/user/<your_username>/original_scene/`。
2.  **运行审核程序**:
    在项目根目录下，打开终端并执行：
    ```bash
    python -m run_video_processing_module.main
    ```
    *   程序会提示输入您的英文名。
    *   处理开始，信息会打印到控制台。
3.  **查看结果**:
    *   审核后的视频及报告在 `your_project_root/user/<your_username>/Result_folder_labeled/`。
    *   打开 `processing_report.html` 查看详细报告和视频预览。

### 🔍 Gemini 审核标准 (AI 审核系统)

当前审核标准定义在 `run_video_processing_module/gemini_utils.py` 的 `prompt` 中，包括：
1.  **环境**: 室内/室外。
2.  **清洁/认证展示**: 特定画面或 TUV logo。
3.  **特定文案/口播**: "hydrojet" 和 "deepclean"。
4.  **品牌识别**: "Eufy"。

Gemini 返回格式如：“合格-不合格-合格-合格”。若所有标准均为“合格”，则最终得分为“合格”。












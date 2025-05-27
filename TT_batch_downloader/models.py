class MediaItem:
    """
    媒体项目基类：MediaItem
    用于存储通用的媒体属性，如ID，并定义一个通用的字符串表示方法。
    
    Attributes:
        id (str): 项目ID。
    """

    def __init__(self, id):
        """
        初始化 MediaItem 实例。

        Args:
            id (str): 项目ID。
        """
        self.id = id

    def __str__(self):
        """
        返回一个格式化的字符串，包含项目的基本信息。

        Returns:
            str: 格式化的项目信息字符串。
        """
        return f"ID: {self.id}"


class Metadata(MediaItem):
    """
    元数据类：Metadata
    用于存储与视频相关的元数据，如标题、时长、观看次数等。
    
    Attributes:
        title (str): 视频标题。
        length (int): 视频时长（秒）。
        views (int): 视频观看次数。
        author (str): 视频作者。
        description (str): 视频描述。
        publish_date (datetime): 视频发布日期。
    """

    def __init__(self, id, title, length, views, author, description, publish_date):
        """
        初始化 Metadata 实例。

        Args:
            id (str): 视频ID。
            title (str): 视频标题。
            length (int): 视频时长（秒）。
            views (int): 视频观看次数。
            author (str): 视频作者。
            description (str): 视频描述。
            publish_date (datetime): 视频发布日期。
        """
        super().__init__(id)
        self.title = title
        self.length = length
        self.views = views
        self.author = author
        self.description = description
        self.publish_date = publish_date
    
    def __str__(self):
        """
        返回一个格式化的字符串，包含所有元数据信息。

        Returns:
            str: 格式化的元数据字符串。
        """
        return (super().__str__() + "\n"
                f"title: {self.title}\n" 
                f"length: {self.length}\n" 
                f"views: {self.views}\n"
                f"author: {self.author}\n"
                f"publish_date: {self.publish_date}")


class Video(MediaItem):
    """
    视频类：Video
    用于存储下载的视频的ID和文件路径。
    
    Attributes:
        downloaded_path (str): 视频下载路径。
    """

    def __init__(self, id, downloaded_path):
        """
        初始化 Video 实例。

        Args:
            id (str): 视频ID。
            downloaded_path (str): 视频下载路径。
        """
        super().__init__(id)
        self.downloaded_path = downloaded_path

    def __str__(self):
        """
        返回一个格式化的字符串，包含视频ID和下载路径。

        Returns:
            str: 格式化的视频信息字符串。
        """
        return (super().__str__() + "\n"
                f"downloaded_path: {self.downloaded_path}")


class Audio(MediaItem):
    """
    音频类：Audio
    用于存储提取的音频的ID和文件路径。
    
    Attributes:
        audio_path (str): 音频文件路径。
    """

    def __init__(self, id, audio_path):
        """
        初始化 Audio 实例。

        Args:
            id (str): 音频ID。
            audio_path (str): 音频文件路径。
        """
        super().__init__(id)
        self.audio_path = audio_path

    def __str__(self):
        """
        返回一个格式化的字符串，包含音频ID和文件路径。

        Returns:
            str: 格式化的音频信息字符串。
        """
        return (super().__str__() + "\n"
                 f"audio_path: {self.audio_path}")


class Comment(MediaItem):
    """
    评论类：Comment
    用于存储视频评论的信息，如视频ID、评论作者、评论内容和发布时间。
    
    Attributes:
        author (str): 评论作者。
        text (str): 评论内容。
        published_at (str): 评论发布时间。
    """

    def __init__(self, video_id, author, text, published_at):
        """
        初始化 Comment 实例。

        Args:
            video_id (str): 视频ID。
            author (str): 评论作者。
            text (str): 评论内容。
            published_at (str): 评论发布时间。
        """
        super().__init__(video_id)
        self.author = author
        self.text = text
        self.published_at = published_at

    def __str__(self):
        """
        返回一个格式化的字符串，包含评论的所有信息。

        Returns:
            str: 格式化的评论信息字符串。
        """
        return (super().__str__() + "\n"
                f"Author: {self.author}\n"
                f"Comment: {self.text}\n"
                f"Published at: {self.published_at}\n"
                + "-" * 80)


class Text(MediaItem):
    """
    文本类：Text
    用于存储视频的所有文本信息，包括评论、标签和字幕。
    
    Attributes:
        comments (list): 评论列表。
        hashtags (list): 标签列表。
        captions (str): 字幕文本。
    """

    def __init__(self, video_id):
        """
        初始化 Text 实例。

        Args:
            video_id (str): 视频ID。
        """
        super().__init__(video_id)
        self.comments = []
        self.hashtags = []
        self.captions = None

    def add_comment(self, comment):
        """
        添加评论到评论列表。

        Args:
            comment (Comment): 要添加的评论对象。
        """
        self.comments.append(comment)

    def add_hashtags(self, hashtags):
        """
        添加标签到标签列表。

        Args:
            hashtags (list): 要添加的标签列表。
        """
        self.hashtags.extend(hashtags)

    def add_captions(self, captions):
        """
        设置字幕文本。

        Args:
            captions (str): 字幕文本。
        """
        self.captions = captions

    def __str__(self):
        """
        返回一个格式化的字符串，包含所有文本信息。

        Returns:
            str: 格式化的文本信息字符串。
        """
        hashtags_str = ", ".join(self.hashtags)
        comments_str = "\n".join(str(comment) for comment in self.comments)
        captions_str = self.captions if self.captions else "No captions available"
        return (super().__str__() + f"\nHashtags: {hashtags_str}\nComments:\n{comments_str}\nCaptions:\n{captions_str}")

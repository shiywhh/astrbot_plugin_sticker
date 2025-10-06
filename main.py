from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star
from astrbot.api.message_components import Image, Plain
from astrbot.api import logger
import os
import random


class StickerPlugin(Star):
    """表情包插件
    "astrbot_plugin_sticker",
    "shiywhh",
    "doro、capoo、cheshire、chiikawa四大表情包发送",
    "1.0.0",
    "https://github.com/shiywhh/astrbot_plugin_sticker"
    """

    def __init__(self, context: Context):
        super().__init__(context)
        # 定义所有表情包类别及其对应的命令和别名
        self.sticker_categories = {
            'doro': {'alias': {'Doro'}},
            'capoo': {'alias': {'Capoo', '猫猫虫', '咖波', '西诶批欧欧', '🐷🐷虫'}},
            'cheshire': {'alias': {'Cheshire', '柴郡'}},
            'chiikawa': {'alias': {'Chiikawa', '乌萨奇'}}
        }
        # 动态注册所有命令处理函数
        self._register_handlers()

    def _register_handlers(self):
        """动态注册所有表情包命令的处理函数"""
        for category, config in self.sticker_categories.items():
            # 为每个类别创建对应的命令处理函数
            handler = self._create_handler(category)
            # 使用装饰器注册命令
            decorated_handler = filter.command(category, alias=config['alias'])(handler)
            # 将装饰后的方法设置为实例方法
            setattr(self, category, decorated_handler)

    def _create_handler(self, category: str):
        """为指定类别创建命令处理函数"""

        async def handler(event: AstrMessageEvent):
            """随机抽取一张{category}并发送"""
            return await self._send_random_image(event, category)

        # 更新文档字符串
        handler.__doc__ = f"随机抽取一张{category}并发送"
        return handler

    async def _send_random_image(self, event: AstrMessageEvent, category: str):
        """发送随机图片的通用方法

        Args:
            event: 消息事件
            category: 图片类别
        """
        image_folder = os.path.join(os.path.dirname(__file__), category)

        # 检查文件夹是否存在
        if not os.path.exists(image_folder):
            logger.warning(f"图片文件夹不存在: {image_folder}")
            return event.plain_result(f"{category}文件夹不存在，请检查插件目录")

        try:
            # 获取所有图片文件
            image_files = [
                f for f in os.listdir(image_folder)
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
            ]

            if not image_files:
                logger.warning(f"图片文件夹为空: {image_folder}")
                return event.plain_result(f"{category}文件夹中没有图片")

            # 随机选择一张图片
            random_image_file = random.choice(image_files)
            image_path = os.path.join(image_folder, random_image_file)

            # 验证文件是否存在且可读
            if not os.path.isfile(image_path):
                logger.error(f"图片文件不存在: {image_path}")
                return event.plain_result("图片文件不存在")

            return event.chain_result([Image.fromFileSystem(image_path)])

        except (OSError, IOError) as e:
            # 文件操作相关异常
            logger.error(f"文件操作错误 [{category}]: {str(e)}", exc_info=True)
            return event.plain_result("文件读取失败，请检查图片文件")
        except Exception as e:
            # 其他未预期的异常
            logger.error(f"未预期的错误 [{category}]: {str(e)}", exc_info=True)
            return event.plain_result("发送图片时出错了，请联系管理员")
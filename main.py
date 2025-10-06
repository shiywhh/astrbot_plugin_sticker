from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star
from astrbot.api.message_components import Image, Plain
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
        # 定义所有支持的图片类别及其别名
        self._image_categories = {
            "doro": {"Doro"},
            "capoo": {"Capoo", "猫猫虫", "咖波", "西诶批欧欧", "🐷🐷虫"},
            "cheshire": {"Cheshire", "柴郡"},
            "chiikawa": {"Chiikawa", "乌萨奇"}
        }

    async def _send_random_image(self, event: AstrMessageEvent, category: str):
        """发送随机图片的通用方法

        Args:
            event: 消息事件
            category: 图片类别
        """
        image_folder = os.path.join(os.path.dirname(__file__), category)

        # 检查文件夹是否存在
        if not os.path.exists(image_folder):
            return event.plain_result(f"{category}文件夹不存在，请检查插件目录")

        # 获取所有图片文件
        image_files = [
            f for f in os.listdir(image_folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
        ]

        if not image_files:
            return event.plain_result(f"{category}文件夹中没有图片")

        # 随机选择一张图片
        try:
            random_image_file = random.choice(image_files)
            image_path = os.path.join(image_folder, random_image_file)
            return event.chain_result([Image.fromFileSystem(image_path)])
        except Exception as e:
            return event.plain_result(f"发送图片时出现错误: {str(e)}")

    def _register_image_commands(self):
        """动态注册所有图片命令"""
        for category, aliases in self._image_categories.items():
            # 为每个类别创建命令处理方法
            async def command_handler(event: AstrMessageEvent, cat=category):
                return await self._send_random_image(event, cat)

            # 设置方法的文档字符串
            command_handler.__doc__ = f"随机抽取一张{category}并发送"

            # 注册命令
            command_decorator = filter.command(category, alias=aliases)
            setattr(self, category, command_decorator(command_handler))

    async def activate(self):
        """插件激活时调用"""
        self._register_image_commands()
        await super().activate()
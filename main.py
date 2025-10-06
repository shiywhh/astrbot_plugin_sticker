from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star
from astrbot.api.message_components import Image, Plain
from astrbot.api import logger
import os
import random

# 配置表情包的元数据
# KEY: 文件夹名, VALUE: (命令名, 别名列表)
STICKER_CONFIG = {
    "doro": ("doro", {'Doro'}),
    "capoo": ("capoo", {'Capoo', '猫猫虫', '咖波', '西诶批欧欧', '🐷🐷虫'}),
    "cheshire": ("cheshire", {'Cheshire', '柴郡'}),
    "chiikawa": ("chiikawa", {'Chiikawa', '乌萨奇'}),
}


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

    async def _send_random_image(self, event: AstrMessageEvent, category: str):
        """发送随机图片的通用方法

        Args:
            event: 消息事件
            category: 图片类别 (对应文件夹名)
        """
        # 使用 os.path.dirname(__file__) 确保路径相对于插件文件
        image_folder = os.path.join(os.path.dirname(__file__), category)

        # 检查文件夹是否存在
        if not os.path.exists(image_folder):
            logger.warning(f"图片文件夹不存在: {image_folder}")
            # 返回一个 Plain 结果
            return event.plain_result(f"{category}文件夹不存在，请检查插件目录")

        try:
            # 获取所有图片文件
            image_files = [
                f for f in os.listdir(image_folder)
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
            ]

            if not image_files:
                logger.warning(f"图片文件夹为空: {image_folder}")
                # 提前处理空列表情况
                return event.plain_result(f"{category}文件夹中没有图片")

            # 随机选择一张图片
            random_image_file = random.choice(image_files)
            image_path = os.path.join(image_folder, random_image_file)

            # 验证文件是否存在且可读
            if not os.path.isfile(image_path):
                # 理论上应该在 os.listdir 后就确定，但作为防御性编程保留
                logger.error(f"图片文件不存在: {image_path}")
                return event.plain_result("图片文件不存在")

            # 使用 Image.fromFileSystem 发送图片
            return event.chain_result([Image.fromFileSystem(image_path)])

        except (OSError, IOError) as e:
            # 文件操作相关异常（权限、读取错误等）
            logger.error(f"文件操作错误 [{category}]: {str(e)}", exc_info=True)
            return event.plain_result("文件读取失败，请检查图片文件或权限")
        except Exception as e:
            # 其他未预期的异常
            logger.error(f"未预期的错误 [{category}]: {str(e)}", exc_info=True)
            return event.plain_result("发送图片时出错了，请联系管理员")

    # 使用循环和 exec/type(self).__dict__ 无法优雅地在 Star 类中动态添加 @filter.command 装饰的方法
    # 在 astrbot 框架下，最可读且实际的方法是继续使用显式定义，但将逻辑抽象到 _send_random_image 中。

    @filter.command(**STICKER_CONFIG["doro"][0], alias=STICKER_CONFIG["doro"][1])
    async def doro(self, event: AstrMessageEvent):
        """随机抽取一张doro并发送"""
        return await self._send_random_image(event, "doro")

    @filter.command(**STICKER_CONFIG["capoo"][0], alias=STICKER_CONFIG["capoo"][1])
    async def capoo(self, event: AstrMessageEvent):
        """随机抽取一张capoo并发送"""
        return await self._send_random_image(event, "capoo")

    @filter.command(**STICKER_CONFIG["cheshire"][0], alias=STICKER_CONFIG["cheshire"][1])
    async def cheshire(self, event: AstrMessageEvent):
        """随机抽取一张cheshire并发送"""
        return await self._send_random_image(event, "cheshire")

    @filter.command(**STICKER_CONFIG["chiikawa"][0], alias=STICKER_CONFIG["chiikawa"][1])
    async def chiikawa(self, event: AstrMessageEvent):
        """随机抽取一张chiikawa并发送"""
        return await self._send_random_image(event, "chiikawa")
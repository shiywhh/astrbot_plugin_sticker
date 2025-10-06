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
        except IndexError:
            # random.choice 在空列表上调用（理论上不会发生，但保持防御性）
            logger.error(f"随机选择时遇到空列表 [{category}]", exc_info=True)
            return event.plain_result("图片选择失败")
        except Exception as e:
            # 其他未预期的异常
            logger.error(f"未预期的错误 [{category}]: {str(e)}", exc_info=True)
            return event.plain_result("发送图片时出错了，请联系管理员")

    @filter.command("doro", alias={'Doro'})
    async def doro(self, event: AstrMessageEvent):
        """随机抽取一张doro并发送"""
        return await self._send_random_image(event, "doro")

    @filter.command("capoo", alias={'Capoo', '猫猫虫', '咖波', '西诶批欧欧', '🐷🐷虫'})
    async def capoo(self, event: AstrMessageEvent):
        """随机抽取一张capoo并发送"""
        return await self._send_random_image(event, "capoo")

    @filter.command("cheshire", alias={'Cheshire', '柴郡'})
    async def cheshire(self, event: AstrMessageEvent):
        """随机抽取一张cheshire并发送"""
        return await self._send_random_image(event, "cheshire")

    @filter.command("chiikawa", alias={'Chiikawa', '乌萨奇'})
    async def chiikawa(self, event: AstrMessageEvent):
        """随机抽取一张chiikawa并发送"""
        return await self._send_random_image(event, "chiikawa")
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Image
import os
import random


@register(
    "astrbot_plugin_sticker",
    "shiywhh",
    "doro、capoo、cheshire、chiikawa四大表情包发送",
    "1.0.0",
    "https://github.com/shiywhh/astrbot_plugin_sticker"
)
class StickerPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def _send_sticker(self, event: AstrMessageEvent, sticker_type: str):
        """发送表情包的通用方法"""
        folder = os.path.join(os.path.dirname(__file__), sticker_type)
        if not os.path.exists(folder):
            yield event.plain_result(f"{sticker_type}文件夹不存在，请检查插件目录")
            return

        image_files = [f for f in os.listdir(folder)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        if not image_files:
            yield event.plain_result(f"{sticker_type}文件夹中没有图片")
            return

        random_image = random.choice(image_files)
        image_path = os.path.join(folder, random_image)

        yield event.chain_result([Image.fromFileSystem(image_path)])

    @filter.command("doro", alias={'Doro'})
    async def doro(self, event: AstrMessageEvent):
        '''随机抽取一张doro并发送'''
        async for result in self._send_sticker(event, "doro"):
            yield result

    @filter.command("capoo", alias={'Capoo', '猫猫虫', '咖波', '西诶批欧欧', '🐷🐷虫'})
    async def capoo(self, event: AstrMessageEvent):
        '''随机抽取一张capoo并发送'''
        async for result in self._send_sticker(event, "capoo"):
            yield result

    @filter.command("cheshire", alias={'Cheshire', '柴郡'})
    async def cheshire(self, event: AstrMessageEvent):
        '''随机抽取一张cheshire并发送'''
        async for result in self._send_sticker(event, "cheshire"):
            yield result

    @filter.command("chiikawa", alias={'Chiikawa', '乌萨奇'})
    async def chiikawa(self, event: AstrMessageEvent):
        '''随机抽取一张chiikawa并发送'''
        async for result in self._send_sticker(event, "chiikawa"):
            yield result
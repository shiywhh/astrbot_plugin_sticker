from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import At, Image, Plain
import os
import random

@register(
    "astrbot_plugin_doro_today",
    "Futureppo",
    "今天doro是什么结局？",
    "1.0.0",
    "https://github.com/your-repo/astrbot_plugin_doro_today"
)
class StickerPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def _send_random_image(self, event: AstrMessageEvent, category: str):
        '''一个通用的发送随机图片的辅助方法'''
        image_folder = os.path.join(os.path.dirname(__file__), category)
        if not os.path.exists(image_folder):
            yield event.plain_result(f"{category}文件夹不存在，请检查插件目录")
            return

        image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if not image_files:
            yield event.plain_result(f"{category}文件夹中没有图片")
            return

        random_image_file = random.choice(image_files)
        image_path = os.path.join(image_folder, random_image_file)

        yield event.chain_result([Image.fromFileSystem(image_path)])

    @filter.command("doro", alias={'Doro'})
    async def dorotoday(self, event: AstrMessageEvent):
        '''随机抽取一张doro并发送'''
        await self._send_random_image(event, "doro")

    @filter.command("capoo", alias={'Capoo', '猫猫虫', '咖波', '西诶批欧欧', '🐷🐷虫'})
    async def capootoday(self, event: AstrMessageEvent):
        '''随机抽取一张capoo并发送'''
        await self._send_random_image(event, "capoo")

    @filter.command("cheshire", alias={'Cheshire', '柴郡'})
    async def cheshiretoday(self, event: AstrMessageEvent):
        '''随机抽取一张cheshire并发送'''
        await self._send_random_image(event, "cheshire")

    @filter.command("chiikawa", alias={'Chiikawa', '乌萨奇'})
    async def chiikawatoday(self, event: AstrMessageEvent):
        '''随机抽取一张chiikawa并发送'''
        await self._send_random_image(event, "chiikawa")

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star
from astrbot.api.message_components import Image
import os
import random
import time


class StickerPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.cd = 10  # 默认冷却时间为 10 秒
        self.last_usage = {}  # 存储每个用户上次使用指令的时间

    def _check_cd(self, event: AstrMessageEvent) -> bool:
        """检查用户是否在冷却中，返回True表示可以执行，False表示冷却中"""
        user_id = event.get_sender_id()
        now = time.time()

        if user_id in self.last_usage and (now - self.last_usage[user_id]) < self.cd:
            return False
        return True

    def _get_remaining_time(self, event: AstrMessageEvent) -> float:
        """获取剩余冷却时间"""
        user_id = event.get_sender_id()
        now = time.time()
        if user_id in self.last_usage:
            elapsed = now - self.last_usage[user_id]
            return max(0, self.cd - elapsed)
        return 0

    def _update_cd(self, event: AstrMessageEvent):
        """更新用户最后使用时间"""
        user_id = event.get_sender_id()
        self.last_usage[user_id] = time.time()

    async def _send_sticker(self, event: AstrMessageEvent, sticker_type: str):
        """发送表情包的通用方法"""
        # 检查冷却
        if not self._check_cd(event):
            remaining_time = self._get_remaining_time(event)
            yield event.plain_result(f"冷却中，请等待 {remaining_time:.1f} 秒后重试。")
            return

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

        # 更新冷却时间
        self._update_cd(event)
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

    @filter.command("stkcd")
    async def set_sticker_cd(self, event: AstrMessageEvent, cd: int):
        if cd <= 0:
            yield event.plain_result("冷却时间必须大于 0。")
            return
        self.cd = cd
        yield event.plain_result(f"指令冷却时间已设置为 {cd} 秒。")

    @filter.command("stkhelp")
    async def stkhelp(self, event: AstrMessageEvent):
        help_text = """
    **表情包插件帮助**

    **可用指令:**
	   - **doro指令**：`/doro`、`/Doro`
	   - **capoo指令**：`/capoo`、`/Capoo`、`/咖波`、`/猫猫虫`、`/西诶批欧欧`、`/🐷🐷虫`
	   - **cheshire指令**：`/cheshire`、`/Cheshire`、`/柴郡`
	   - **chiikawa指令**：`/chiikawa`、`/Chiikawa`、`/乌萨奇`


    **使用方法:**
       - 直接发送对应即可获取一张对应人物表情包。
       - 使用 `/stkcd <int>` 将冷却时间设置为 <int> 秒。

    **注意:**
       - 冷却时间默认为 10 秒。
       - 图片需人工储存至插件目录中。
        """
        yield event.plain_result(help_text)
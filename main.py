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
class DoroTodayPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("doro", alias={'Doro'})
    async def dorotoday(self, event: AstrMessageEvent):
        '''随机抽取一张doro并发送'''
        # 获取发送者的ID和昵称
        sender_id = event.get_sender_id()
        try:
            sender_name = event.get_sender_name()
        except AttributeError:
            sender_name = str(sender_id)


        doro_folder = os.path.join(os.path.dirname(__file__), "doro")
        if not os.path.exists(doro_folder):
            yield event.plain_result("doro文件夹不存在，请检查插件目录")
            return
        
        # 获取doro文件夹中的所有图片文件
        image_files = [f for f in os.listdir(doro_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        
        if not image_files:
            yield event.plain_result("doro文件夹中没有图片")
            return
        
        random_image = random.choice(image_files)
        image_path = os.path.join(doro_folder, random_image)
        image_name = os.path.splitext(random_image)[0] 
        
        message_chain = [
            Image.fromFileSystem(image_path)  
        ]
        
        # 发送消息
        yield event.chain_result(message_chain)
    
    @filter.command("capoo", alias={'Capoo','猫猫虫','咖波','西诶批欧欧','🐷🐷虫'})
    async def capootoday(self, event: AstrMessageEvent):
        '''随机抽取一张capoo并发送'''
        # 获取发送者的ID和昵称
        sender_id = event.get_sender_id()
        try:
            sender_name = event.get_sender_name()
        except AttributeError:
            sender_name = str(sender_id)


        doro_folder = os.path.join(os.path.dirname(__file__), "capoo")
        if not os.path.exists(doro_folder):
            yield event.plain_result("capoo文件夹不存在，请检查插件目录")
            return
        
        # 获取capoo文件夹中的所有图片文件
        image_files = [f for f in os.listdir(doro_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        
        if not image_files:
            yield event.plain_result("capoo文件夹中没有图片")
            return
        
        random_image = random.choice(image_files)
        image_path = os.path.join(doro_folder, random_image)
        image_name = os.path.splitext(random_image)[0] 
        
        message_chain = [
            Image.fromFileSystem(image_path)  
        ]
        
        # 发送消息
        yield event.chain_result(message_chain)
        
    @filter.command("cheshire", alias={'Cheshire','柴郡'})
    async def cheshiretoday(self, event: AstrMessageEvent):
        '''随机抽取一张cheshire并发送'''
        # 获取发送者的ID和昵称
        sender_id = event.get_sender_id()
        try:
            sender_name = event.get_sender_name()
        except AttributeError:
            sender_name = str(sender_id)


        doro_folder = os.path.join(os.path.dirname(__file__), "cheshire")
        if not os.path.exists(doro_folder):
            yield event.plain_result("cheshire文件夹不存在，请检查插件目录")
            return
        
        # 获取cheshire文件夹中的所有图片文件
        image_files = [f for f in os.listdir(doro_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        
        if not image_files:
            yield event.plain_result("cheshire文件夹中没有图片")
            return
        
        random_image = random.choice(image_files)
        image_path = os.path.join(doro_folder, random_image)
        image_name = os.path.splitext(random_image)[0] 
        
        message_chain = [
            Image.fromFileSystem(image_path)  
        ]
        
        # 发送消息
        yield event.chain_result(message_chain)
        
    @filter.command("chiikawa", alias={'Chiikawa','乌萨奇'})
    async def chiikawatoday(self, event: AstrMessageEvent):
        '''随机抽取一张chiikawa并发送'''
        # 获取发送者的ID和昵称
        sender_id = event.get_sender_id()
        try:
            sender_name = event.get_sender_name()
        except AttributeError:
            sender_name = str(sender_id)


        doro_folder = os.path.join(os.path.dirname(__file__), "chiikawa")
        if not os.path.exists(doro_folder):
            yield event.plain_result("chiikawa文件夹不存在，请检查插件目录")
            return
        
        # 获取chiikawa文件夹中的所有图片文件
        image_files = [f for f in os.listdir(doro_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        
        if not image_files:
            yield event.plain_result("chiikawa文件夹中没有图片")
            return
        
        random_image = random.choice(image_files)
        image_path = os.path.join(doro_folder, random_image)
        image_name = os.path.splitext(random_image)[0] 
        
        message_chain = [
            Image.fromFileSystem(image_path)  
        ]
        
        # 发送消息
        yield event.chain_result(message_chain)
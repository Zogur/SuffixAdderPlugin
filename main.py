import os
from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost
import logging
from typing import Union
from mirai import At

@register(name="SuffixAdderPlugin", description="为每次回复的消息添加后缀", version="1.0.1", author="Zogur,ErJiQwQ")
class SuffixAdderPlugin(Plugin):
    """
    为每条 AI 回复添加自定义后缀的插件。
    支持通过命令动态设置后缀。
    """

    def __init__(self, plugin_host: PluginHost):
        self.plugin_host = plugin_host
        self.suffix = " -- 由南京城市职业学院人工智能社团提供，仅供参考。"
        self.feedback_url="https://docs.qq.com/form/page/DSmFsaHVERlBNd2pG"
        self.freshman_registration_handbook="https://alidocs.dingtalk.com/i/nodes/Y1OQX0akWm99YP9DFpAMQlAgWGlDd3mE?utm_scene=team_space"
        self.logger = logging.getLogger("SuffixAdderPlugin")
        self.logger.setLevel(logging.DEBUG)
        self.logger.info(f"SuffixAdderPlugin 插件已加载，当前后缀：{self.suffix}")
        

    @on(PersonCommandSent)
    @on(GroupCommandSent)
    def process_command(self, event: EventContext, **kwargs):
        command_event: Union[PersonCommandSent, GroupCommandSent] = event.event
        if command_event.command == 'set_suffix':
            event.prevent_default()
            event.prevent_postorder()
            if command_event.is_admin:
                if len(command_event.params) == 0:
                    event.add_return('reply', ["[SuffixAdderPlugin] 请指定要设置的后缀，例如: !set_suffix 新后缀"])
                else:
                    new_suffix = " ".join(command_event.params)
                    self.suffix = f" -- {new_suffix}"
                    event.add_return('reply', [f"[SuffixAdderPlugin] 后缀已设置为: {self.suffix}"])
                    self.logger.info(f"后缀已更新为: {self.suffix}")
            else:
                event.add_return('reply', ["[SuffixAdderPlugin] 您不是管理员，无法使用此命令"])


    # @on(PersonNormalMessageReceived)
    # @on(GroupNormalMessageReceived)
    # def normal_message_received(self, event: EventContext,host: PluginHost, **kwargs):
    #     pass

    # 当收到GPT回复时触发
    @on(NormalMessageResponded)
    def normal_message_responded(self, event: EventContext, **kwargs):
        response_text:str = kwargs['response_text']
        print('='*100)
        print(response_text)
        if self.suffix :
            print('='*100)
            print("我有一个小尾巴")
            event.add_return("reply", response_text+os.linesep+self.suffix+os.linesep+f"如有疑问或异议可通过下面的链接进行反馈：{self.feedback_url}"+os.linesep+f"新生报到手册:"+os.linesep+f"{self.freshman_registration_handbook}")
            # event.prevent_default()
    def __del__(self):
        self.logger.info("SuffixAdderPlugin 插件已卸载")
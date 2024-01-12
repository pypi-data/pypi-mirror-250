#  Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
from __future__ import unicode_literals
import json
import logging
from json import JSONDecodeError

from langchain.prompts import PromptTemplate
from pydantic.typing import NoneType

from pangukitsappdev.agent.agent_action import AgentAction
from pangukitsappdev.agent.agent_session import AgentSession
from pangukitsappdev.api.agent.base import AbstractAgent
from pangukitsappdev.api.llms.base import LLMApi, to_message_in_req
from pangukitsappdev.prompt.prompt_tmpl import PromptTemplates

logger = logging.getLogger(__name__)


class ReactPanguAgent(AbstractAgent):
    TOOL_START_MARK = "[unused11]"
    TOOL_END_MARK = "[unused12]"
    MARK_PLUGIN_FIX = "[unused11]工具调用:"
    DEFAULT_SYS_PROMPT = "你的名字叫智子，是由华为开发的智能助手"
    VERTICAL_SEPERATOR = "|"
    MODULE_VERSION_PREFIX_38B = "38B"
    TEMPLATE_VERSION_PLUGIN_V2 = "plugin_v2"
    TEMPLATE_VERSION_UNIFY = "unify"

    def __init__(self, llm: LLMApi):
        super(ReactPanguAgent, self).__init__(llm)

    def react(self, agent_session: AgentSession):
        actions = agent_session.history_action
        # 超过最大迭代次数限制，不再执行
        if self.need_interrupt(agent_session):
            return

        # 构造React prompt
        react_tp = self.get_react_template()
        actions_list = []
        for action in actions:
            action_dict = action.dict(exclude_none=True, exclude={"action_json", "action_input"})
            if action.action_json:
                action_dict["actionJson"] = action.action_json
            if action.action_input:
                action_dict["actionInput"] = action.action_input
            actions_list.append(action_dict)

        messages = []
        for message in agent_session.messages:
            msg_dict = to_message_in_req(message)
            messages.append({'role': {'text': msg_dict.get('role'),
                                      'desc': self.convert_role_to_desc(msg_dict.get('role'))},
                             'content': msg_dict.get('content')})

        default_sys_prompt = self.DEFAULT_SYS_PROMPT if self.is_plugin_v1_version(self.get_template_version()) else ""
        sys_prompt = self.get_system_prompt(
            agent_session) if self.get_system_prompt(agent_session) is not None else default_sys_prompt
        final_prompt = react_tp.format(sys_prompt=sys_prompt,
                                       tool_desc=self.get_tool_desc(),
                                       messages=messages,
                                       actions=actions_list)
        normalize_prompt = self.normalize(final_prompt, True)
        # 调用llm
        if self.llm.get_llm_config().llm_param_config.stream:
            tokens = self.llm.ask(normalize_prompt)
            answer = ""
            for token in tokens:
                answer += token
        else:
            answer = self.llm.ask(normalize_prompt).answer
        normalized_answer = self.normalize(answer, False)

        # 获取工具，例如：reserve_meeting_room|{'meetingRoom':'2303','start':'03:00','end':'08:00'}\n\n
        tool_use = self.sub_str_before(self.sub_str_between(normalized_answer,
                                                            self.MARK_PLUGIN_FIX,
                                                            self.TOOL_END_MARK), self.TOOL_START_MARK)
        tool_id = self.sub_str_before(tool_use, "|")
        # 未找到工具则返回
        if tool_id == "":
            action = AgentAction(req=normalize_prompt,
                                 resp=answer,
                                 thought=answer,
                                 action=self.FINAL_ACTION,
                                 action_input=answer)
            agent_session.current_action = action
            self.notice_session_end(agent_session)
            return
        tool = self.tool_map.get(tool_id)
        action = AgentAction(req=normalize_prompt,
                             resp=answer,
                             thought=self.sub_str_before(normalized_answer, self.TOOL_START_MARK),
                             action_json="",
                             action=tool_id)
        agent_session.current_action = action

        # 提取工具参数
        action.action_input = self.sub_str_after(tool_use, self.VERTICAL_SEPERATOR).strip(self.VERTICAL_SEPERATOR)
        try:
            if tool.input_type in [int, float, str, bool]:
                json_obj = json.loads(action.action_input)
                if not json_obj or len(json_obj.values()) != 1:
                    raise ValueError(f"the action input is not a single input, require: {tool.get_pangu_function()},"
                                     f" action return: {action.action_input}")
                # 这里添加容错，对单个参数的字段名不做限制{}
                tool_input = list(json_obj.values())[0]
            elif tool.input_type is NoneType:
                tool_input = "{}"
            else:
                tool_input = json.loads(action.action_input)
        except JSONDecodeError:
            tool_input = action.action_input

        # 执行工具
        self.tool_execute(tool, tool_input, agent_session)
        logger.info("actions = %s", "\n".join([action.json(ensure_ascii=False) for action in actions]))
        # 执行下一迭代
        self.react(agent_session)

    def get_tool_desc(self):
        return self.get_tool_desc_template().format(tools=[
            {"panguFunction": self.tool_map[tool].get_pangu_function()} for tool in self.tool_map])

    def normalize(self, prompt_str: str, is_input: bool) -> str:
        return self.normalize_placeholder(prompt_str, is_input) if self.is_38b_module() else prompt_str

    @staticmethod
    def normalize_placeholder(prompt_str: str, is_input: bool) -> str:
        """
        诺亚模型38B和71B/135B使用了不同的占位符，对应关系如下，左边为38B，右边为71B/135B
        <unused0> -> [unused9]
        <unused1> -> [unused10]
        <unused2> -> [unused11]
        <unused3> -> [unused12]
        统一归一成71B/135B的占位符，当且仅当sdk.llm.pangu.model-version配置为38B时，进行归一
        :param prompt_str: 需要做占位符归一化的字符串
        :param is_input: true：输入；false：输出
        :return: 归一化后的字符串
        """
        if is_input:
            return prompt_str.replace("[unused9]", "<unused0>")\
                .replace("[unused10]", "<unused1>")\
                .replace("[unused11]", "<unused2>")\
                .replace("[unused12]", "<unused3>")
        else:
            return prompt_str.replace("<unused0>", "[unused9]")\
                .replace("<unused1>", "[unused10]")\
                .replace("<unused2>", "[unused11]")\
                .replace("<unused3>", "[unused12]")

    def is_38b_module(self) -> bool:
        module_version = self.llm.get_llm_config().llm_module_config.module_version
        return module_version.startswith(self.MODULE_VERSION_PREFIX_38B)

    def is_plugin_v1_version(self, template_version) -> bool:
        return template_version not in [self.TEMPLATE_VERSION_PLUGIN_V2, self.TEMPLATE_VERSION_UNIFY]

    def get_template_version(self) -> str:
        module_version = self.llm.get_llm_config().llm_module_config.module_version
        return self.sub_str_after(module_version, "_")

    def get_react_template(self) -> PromptTemplate:
        template_version = self.get_template_version()
        if template_version == self.TEMPLATE_VERSION_PLUGIN_V2:
            return PromptTemplates.get("agent_react_pangu_2")
        elif template_version == self.TEMPLATE_VERSION_UNIFY:
            return PromptTemplates.get("agent_react_pangu_unify")
        else:
            return PromptTemplates.get("agent_react_pangu")

    def get_tool_desc_template(self) -> PromptTemplate:
        template_version = self.get_template_version()
        if template_version == self.TEMPLATE_VERSION_PLUGIN_V2 or template_version == self.TEMPLATE_VERSION_UNIFY:
            return PromptTemplates.get("agent_tool_desc_pangu_2")
        else:
            return PromptTemplates.get("agent_tool_desc_pangu")

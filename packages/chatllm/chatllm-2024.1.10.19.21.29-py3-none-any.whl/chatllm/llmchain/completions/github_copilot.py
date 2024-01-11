#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : copilot
# @Time         : 2023/12/6 13:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 不准白嫖 必须 star, todo: 兜底设计、gpt/图片
# https://github.com/CaoYunzhou/cocopilot-gpt/blob/main/main.py
#
import openai
from meutils.pipe import *
from meutils.cache_utils import ttl_cache
from meutils.decorators.retry import retrying
from meutils.queues.uniform_queue import UniformQueue
from meutils.notice.feishu import send_message

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

from chatllm.llmchain.completions import openai_completions

GITHUB_BASE_URL = os.getenv('GITHUB_BASE_URL', 'https://api.github.com')
GITHUB_COPILOT_BASE_URL = os.getenv('GITHUB_COPILOT_BASE_URL', 'https://api.githubcopilot.com')

send_message = partial(
    send_message,
    title="github_copilot",
    url="https://open.feishu.cn/open-apis/bot/v2/hook/e2f5c8eb-4421-4a0b-88ea-e2d9441990f2"
)


class Completions(object):
    def __init__(self, **client_params):
        self.api_key = client_params.get('api_key')
        self.access_token = self.get_access_token(self.api_key)
        self.completions = openai_completions.Completions(api_key=self.access_token)

    def create(self, messages: List[Dict[str, Any]], **kwargs):  # ChatCompletionRequest: 定义请求体

        data = {
            "model": 'gpt-4',
            "messages": messages,
            **kwargs
        }

        data['model'] = data.get('model', 'gpt-4').startswith('gpt-4') and 'gpt-4' or 'gpt-3.5-turbo'

        # logger.debug(data)

        if data.get('stream'):
            stream = self.completions.create(**data)
            # return stream

            interval = data.get('interval')
            interval = interval or (0.05 if "gpt-4" in data['model'] else 0.01)
            return UniformQueue(stream).consumer(interval=interval, break_fn=self.break_fn)

        else:
            return self.completions.create(**data)

    def create_sse(self, **data):
        response = self.create(**data)
        if data.get('stream'):
            from sse_starlette import EventSourceResponse
            generator = (chunk.model_dump_json() for chunk in response)
            return EventSourceResponse(generator, ping=10000)
        return response

    @staticmethod
    @retrying
    @ttl_cache(ttl=15 * 60)
    def get_access_token(api_key: Optional[str] = None):

        api_key = api_key or os.getenv("GITHUB_COPILOT_TOKEN")
        assert api_key

        headers = {
            'Host': 'api.github.com',
            'authorization': f'Bearer {api_key}',
            'Editor-Version': 'vscode/1.85.1',
            'Editor-Plugin-Version': 'copilot-chat/0.11.1',
            'User-Agent': 'GitHubCopilotChat/0.11.1',
            'Accept': '*/*',
            "Accept-Encoding": "gzip, deflate, br"
        }

        url = f"{GITHUB_BASE_URL}/copilot_internal/v2/token"
        response = requests.get(url, headers=headers)

        logger.debug(response.json().get('sku'))

        return response.json().get('token')

    @staticmethod
    def break_fn(line: ChatCompletionChunk):
        return line.choices and line.choices[0].finish_reason

    @classmethod
    def chat(cls, data: dict):  # TEST
        """
            Completions.chat(data)
        """
        with timer('聊天测试'):
            _ = cls().create(**data)

            print(f'{"-" * 88}\n')
            if isinstance(_, Generator) or isinstance(_, openai.Stream):
                for i in _:
                    content = i.choices[0].delta.content
                    print(content, end='')
            else:
                print(_.choices[0].message.content)
            print(f'\n\n{"-" * 88}')


if __name__ == '__main__':
    # 触发风控
    s = """
    Question:已知节点类型只有六种：原因分析、排故方法、故障时间、故障现象、故障装备单位、训练地点，现在我给你一个问题，你需要根据这个句子来推理出这个问题的答案在哪个节点类型中，问题是”管道细长、阻力太大时的轴向柱塞泵故障如何解决？“,输出格式形为：["节点类型1"], ["节点类型2"], …。除了这个列表以外请不要输出别的多余的话。
['排故方法']

Question:已知节点类型只有六种：原因分析、排故方法、故障时间、故障现象、故障装备单位、训练地点，现在我给你一个问题，你需要根据这个句子来推理出这个问题的答案在哪个节点类型中，问题是”转向缸出现爬行现象，但是压力表却忽高忽低，相对应的解决方案是？“输出格式形为：["节点类型1"], ["节点类型2"], …。除了这个列表以外请不要输出别的多余的话。
['原因分析']、['排故方法']

Question:已知节点类型只有六种：原因分析、排故方法、故障时间、故障现象、故障装备单位、训练地点，现在我给你一个问题，你需要根据这个句子来推理出这个问题的答案在哪个节点类型中，问题是”在模拟训练场A，轴向柱塞马达出现过什么故障？“输出格式形为：["节点类型1"], ["节点类型2"], …。除了这个列表以外请不要输出别的多余的话。

['故障现象']

已知节点类型只有六种：原因分析、排故方法、故障时间、故障现象、故障装备单位、训练地点，现在我给你一个问题，你需要根据这个句子来推理出这个问题的答案在哪个节点类型中，问题是”密封圈挤出间隙的解决方法是什么？“。输出格式形为：["节点类型1"], ["节点类型2"], …。除了这个列表以外请不要输出别的多余的话。
    """

    # s = "1+1"
    # s = '树上9只鸟，打掉1只，还剩几只'
    # s = '讲个故事'

    data = {
        'model': 'gpt-4',
        'messages': [
            {'role': 'system', 'content': "你是gpt4, Let's think things through one step at a time."},
            {'role': 'user', 'content': s}
        ],
        'stream': False
    }

    Completions.chat(data)
    data['stream'] = True
    Completions.chat(data)

    # async def main():
    #     _ = await Completions().acreate(**data)
    #
    #     content = ''
    #     for i in _:
    #         content += i.choices[0].delta.content
    #     return content
    #
    #
    # print(arun(main()))

    # with timer('异步'):
    #     print([Completions().acreate(**data) for _ in range(10)] | xAsyncio)

    # data = {
    #     'model': 'gpt-xxx',
    #     'messages': [{'role': 'user', 'content': '讲个故事。 要足够长，这对我很重要。'}],
    #     'stream': False,
    #     # 'max_tokens': 16000
    # }
    # data = {
    #     'model': 'gpt-4',
    #     'messages': '树上9只鸟，打掉1只，还剩几只',  # [{'role': 'user', 'content': '树上9只鸟，打掉1只，还剩几只'}],
    #     'stream': False,
    #     'temperature': 0,
    #     # 'max_tokens': 32000
    # }
    #
    # for i in tqdm(range(1000)):
    #     _ = Completions().create(**data)
    #     print(_.choices[0].message.content)
    #     break

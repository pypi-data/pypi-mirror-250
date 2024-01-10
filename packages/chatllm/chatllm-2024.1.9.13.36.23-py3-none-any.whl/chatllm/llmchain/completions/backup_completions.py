#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : barkup
# @Time         : 2024/1/9 09:50
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

from openai import OpenAI
from chatllm.schemas.openai_types import chat_completion_error, chat_completion_chunk_error


def create(**data):
    try:
        data['model'] = "backup-gpt"  # todo: 模型加前缀, 更加通用
        _ = (
            OpenAI(api_key=os.getenv("BARKUP_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))
            .chat.completions.create(**data)
        )
        # logger.debug(_)
        return _
    except Exception as e:
        if data.get('stream'):
            chat_completion_chunk_error.choices[0].delta.content = str(e)
            return chat_completion_chunk_error
        else:
            chat_completion_error.choices[0].message.content = str(e)
            return chat_completion_error


if __name__ == '__main__':
    data = {
        'model': 'gpt-4',
        'messages': [
            {'role': 'system', 'content': "你是gpt4, Let's think things through one step at a time."},
            {'role': 'user', 'content': '1+1'}
        ],
        'stream': False}

    print(create(**data))

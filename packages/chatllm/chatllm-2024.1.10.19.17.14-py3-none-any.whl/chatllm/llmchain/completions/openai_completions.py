#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : barkup
# @Time         : 2024/1/9 09:50
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://github.com/openai/openai-python
# todo: 设计更加通用的兜底方案【首先得有靠谱的渠道（多个兜底渠道，作双兜底）】

from meutils.pipe import *
from meutils.notice.feishu import send_message

from openai import OpenAI
from chatllm.schemas.openai_types import chat_completion_error, chat_completion_chunk_error, completion_keys

send_message = partial(
    send_message,
    title="Backup Completions",
    url="https://open.feishu.cn/open-apis/bot/v2/hook/e2f5c8eb-4421-4a0b-88ea-e2d9441990f2"
)


@lru_cache()
class Completions(object):
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, **kwargs):
        # 需要兜底的模型
        params = dict(
            api_key=api_key,
            base_url=base_url or 'https://api.githubcopilot.com',
            default_headers={'Editor-Version': 'vscode/1.85.1'},
        )
        self.client = OpenAI(**params)  # todo: 异步

        self.backup_client = OpenAI(
            api_key=os.getenv("BACKUP_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.chatllm.vip/v1")
        )

    def create(self, **data) -> Any:
        data = {key: data.get(key) for key in completion_keys if key in data}  # 去除多余key
        try:
            response = self.client.chat.completions.create(**data)

            if data.get('stream'):
                return self.post_process(response, data)
            else:
                return response

        except Exception as primary_error:  # 走兜底
            _ = f"Primary client failed: {primary_error}"
            logging.error(_)
            try:
                return self._backup_create(**data)
            except Exception as backup_error:
                _ = f"Backup client failed: {backup_error}"
                send_message(_)
                logging.error(_)
                return self._handle_error(data, backup_error)

    def post_process(self, response, data):
        """兜底判断"""
        for chunk in response:
            # 走兜底
            logger.debug(chunk.model_dump_json())
            if not chunk.choices or chunk.choices[0].finish_reason == 'content_filter':
                yield from self._backup_create(**data)
                break

            if chunk.choices[0].delta.content or chunk.choices[0].finish_reason:
                yield chunk

    def _backup_create(self, **data):
        """恢复模型名"""
        backup_data = data.copy()
        backup_data['model'] = "backup-gpt-4" if data['model'].startswith('gpt-4') else "backup-gpt"  # todo: 4v
        backup_response = self.backup_client.chat.completions.create(**backup_data)

        send_message(str(data))  # 兜底监控

        if data.get('stream'):
            def gen():
                for chunk in backup_response:
                    chunk.model = data['model']
                    yield chunk

            return gen()
        else:
            backup_response.model = data['model']

        return backup_response

    def _handle_error(self, data: Dict[str, Any], error: Exception) -> Any:
        """
        Handle errors and return an appropriate response.
        """
        if data.get('stream'):
            # Assuming chat_completion_chunk_error is defined elsewhere
            chat_completion_chunk_error.choices[0].delta.content = str(error)
            return chat_completion_chunk_error
        else:
            # Assuming chat_completion_error is defined elsewhere
            chat_completion_error.choices[0].message.content = str(error)
            return chat_completion_error


if __name__ == '__main__':
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': "你是gpt4, Let's think things through one step at a time."},
            {'role': 'user', 'content': '艹你'}
        ],
        'stream': False
    }

    for i in range(3):
        print(Completions().create(**data))
        break

    data['stream'] = True
    for i in Completions().create(**data):
        print(i)

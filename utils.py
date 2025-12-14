import base64

from typing import Any


def get_final_response(ai_response: dict[str, Any]) -> str:
    last_message = ai_response['messages'][-1].content

    if isinstance(last_message, str):
        return last_message
    elif isinstance(last_message, list):
        text = []
        for content in last_message:
            if content['type'] == 'text':
                text.append(content['text'])
        return ' '.join(text)
    
    raise ValueError('Unsupported message format')


def base64_to_string(base64_str) -> str:
    decoded_bytes = base64.b64decode(base64_str)
    return decoded_bytes.decode('utf-8')
import json


class Config:
    def __init__(self):
        self.system_prompt = ""
        self.llm_model = ""


def load_config() -> Config:
    s = json.load(open('config.json'))
    config = Config()
    config.system_prompt = s['system_prompt']
    config.llm_model = s['llm_model']
    return config
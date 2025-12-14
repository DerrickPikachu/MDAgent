import json
import asyncio

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.messages.base import BaseMessage

from tool import (
    get_secret, 
    search_markdown, 
    retrieve_markdown_by_id, 
    retrieve_markdown_by_name,
    upload_markdown,
)
from utils import get_final_response
from logger import LoggerMiddleware

load_dotenv()

model = init_chat_model(
    # "google_genai:gemini-2.0-flash",
    "claude-3-5-haiku-latest",
    temperature=0.1,
)

agent = create_agent(
    model=model,
    tools=[get_secret, search_markdown, retrieve_markdown_by_id, retrieve_markdown_by_name, upload_markdown],
    system_prompt="You are a helpful assistant. Use the tools provided to you if needed. Plan the steps before starting to answer or action.",
    middleware=[LoggerMiddleware()],
)


async def main():
    conversation = list[BaseMessage]()

    print('Ctrl+C to exit the agent loop.')
    while True:
        print('=' * 20)
        user_prompt = input('User: ')
        conversation.append(HumanMessage(content=user_prompt))
        print('-' * 20)
        response = await agent.ainvoke({
            'messages': conversation,
        })
        conversation = response['messages']
        print(f'Agent: {get_final_response(response)}')


if __name__ == '__main__':
    asyncio.run(main())
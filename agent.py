import json

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.messages.base import BaseMessage

from tool import get_secret
from utils import get_final_response

load_dotenv()

model = init_chat_model(
    # "google_genai:gemini-2.0-flash",
    "claude-3-5-haiku-latest",
    temperature=0.1,
)

agent = create_agent(
    model=model,
    tools=[get_secret],
    system_prompt="You are a helpful assistant. Use the tools provided to you if needed. Plan the steps before starting to answer or action.",
)

conversation = list[BaseMessage]()


print('Ctrl+C to exit the agent loop.')
while True:
    print('=' * 20)
    user_prompt = input('User: ')
    conversation.append(HumanMessage(content=user_prompt))
    response = agent.invoke({
        'messages': conversation,
    })
    conversation = response['messages']
    print('-' * 20)
    print(f'Agent: {get_final_response(response)}')
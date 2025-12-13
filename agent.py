from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.messages.base import BaseMessage

load_dotenv()

model = init_chat_model(
    "google_genai:gemini-2.5-flash",
    temperature=0.1,
)

conversation = list[BaseMessage]()
conversation.append(SystemMessage(content="You are a helpful assistant. Use the tools provided to you if needed. Plan the steps before starting to answer or action."))


print('Ctrl+C to exit the agent loop.')
while True:
    print('=' * 20)
    user_prompt = input('User: ')
    conversation.append(HumanMessage(content=user_prompt))
    response = model.invoke(conversation)
    conversation.append(response)
    print('-' * 20)
    print(f'Agent: {response.content}')
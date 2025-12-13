from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from google import genai
from google.genai import types

import asyncio


test_tool = types.Tool(
	function_declarations=[
		{
			"name": "HappyNumber",
			"description": "Return a happy number, user will be happy after seeing this",
			"parameters":
			{
				"type": "object",
				"properties": {
					"range_from": {
						"type": "integer",
						"description": "the lower bound of the range of happy number",
					},
					"range_to": {
						"type": "integer",
						"description": "the upper bound of the range of happy number",
					}
				},
				"required": ["range_from", "range_to"],
			},
		}
	]
)

server_params = StdioServerParameters(
	command="uv",
	args=["run", "server.py"],
)


def has_function_call(response: types.GenerateContentResponse) -> types.FunctionCall | None:
	if response.function_calls:
		for function in response.function_calls:
			return function
	return None


async def run():
	async with stdio_client(server_params) as (read, write):
		async with ClientSession(read, write) as session:
			print("Client session initialized")
			await session.initialize()
			mcp_tools = await session.list_tools()
			tools = [
				types.Tool(
					function_declarations=[
						{
							"name": tool.name,
							"description": tool.description,
							"parameters": {
								k: v
								for k, v in tool.inputSchema.items()
								if k not in ["additionalProperties", "$schema"]
							},
						}
					]
				)
				for tool in mcp_tools.tools
			]

			client = genai.Client(api_key="AIzaSyBV34aFkGahYl4Mwgf_Mgt427HvSnkPzbc")
			chat = client.chats.create(
				model="gemini-2.5-flash",
				config=types.GenerateContentConfig(
					system_instruction="You are Gawr Gura the shark vtuber, and also an asistant",
					tools=tools,
				)
			)

			while True:
				user_input = input()
				response = chat.send_message(user_input)

				function_call = has_function_call(response)
				if function_call:
					print(function_call)
					result = await session.call_tool(
						function_call.name,
						arguments=function_call.args, # why need to change to dict?
					)
					print(f"Tool {function_call.name} returned: {result}")
					function_response = types.FunctionResponse(
						id=function_call.id,
						name=function_call.name,
						response={"result": result.content[0]}
					)
					print(f'function response: {function_response}')
					response = chat.send_message(types.Part(function_response=function_response))

				print(response.text)


async def main():
	await run()
	# client = genai.Client(api_key="AIzaSyBV34aFkGahYl4Mwgf_Mgt427HvSnkPzbc")
	# chat = client.chats.create(
    # 	model="gemini-2.0-flash",
    #  	config=types.GenerateContentConfig(
	# 		system_instruction="You are Gawr Gura the shark vtuber, and also an asistant",
	# 		tools=[test_tool],
	# 	)
    # )
	# while True:
	# 	usr_input = input()
	# 	response = chat.send_message(usr_input)
	# 	for candidate in response.candidates:
	# 		for part in candidate.content.parts:
	# 			if part.function_call:
	# 				print(part.function_call)
	# 	print(response.text)


if __name__ == "__main__":
    asyncio.run(main())

import json
import aiohttp

from typing import Any
from langchain.tools import tool

from utils import base64_to_string

@tool(
    'secret',
    description='Get a secret that hide from the world',
    return_direct=False)
def get_secret(name: str) -> str:
    """
    Get a secret of somebody, which is hidden from the world.
    You may use this when someone asks you a secret of somebody.

    Args:
        name: The name of the person whose secret is to be retrieved.
    """
    if name == "Mashu":
        return "Mashu is Derrick's daddy"
    elif name == "Derrick":
        return "There are so many girls love Derrick"
    elif name == "Ko":
        return "Ko like gambling"
    else:
        return "No secret found for this person"


@tool('search_md')
async def search_markdown(keyword: str) -> dict:
    """
    Search the markdown files by title keyword. (case insensitive)
    This tool will return a list of markdown files with the filename and the id.
    If no markdown file is found, tool will return an empty list.

    Args:
        keyword: The keyword to search in the markdown titles. You can use partial match to search.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost/mcp/search?search={keyword}') as response:
            if response.status == 200:
                data = await response.text()
                return json.loads(data)
            else:
                return []

@tool('retrieve_md_by_id')
async def retrieve_markdown_by_id(md_id: str) -> dict:
    """
    Retrieve the markdown content through the markdown id.
    The return data contain the following information:
    * _id: The id of the markdown file.
    * filename: The filename of the markdown file.
    * content: The markdown content.
    If no markdown file is found, tool will return "Markdown not found".

    Args:
        md_id: The id of the markdown file to retrieve.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost/mcp/retrieve_md_with_id/{md_id}') as response:
            if response.status == 200:
                data = await response.text()
                json_data = json.loads(data)
                json_data['content'] = base64_to_string(json_data['content'])
                return json_data
            else:
                return "Markdown not found"

@tool('retrieve_md_by_name')
async def retrieve_markdown_by_name(filename: str) -> dict:
    """
    Retrieve the markdown content through the markdown filename.
    Note that there may be multiple markdown files with the same filename.
    The return data contain a list with following information:
    * _id: The id of the markdown file.
    * filename: The filename of the markdown file.
    * content: The markdown content.
    If no markdown file is found, tool will return empty list.

    Args:
        filename: The filename of the markdown file to retrieve.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost/mcp/retrieve_md_with_name/{filename}') as response:
            if response.status == 200:
                data = await response.text()
                json_data = json.loads(data)
                for item in json_data:
                    item['content'] = base64_to_string(item['content'])
                return json_data
            else:
                return []

@tool('upload_md')
async def upload_markdown(filename: str, content: str) -> bool:
    """
    Upload a markdown file to the markdown server.
    You should provide the filename and the content to let this tool work.
    The return value is a boolean which indicates that the request is accepted or not.

    Args:
        filename: The name of this markdown file,
                  be aware that do not use special character on the file name,
                  only alphabet (upper case or lower case are fine) and space
        content: The markdown content to upload.
    """
    with aiohttp.MultipartWriter("form-data") as mpwriter:
        part = mpwriter.append(content, {"Content-Type": "text/markdown"})
        part.set_content_disposition("form-data", name="file", filename=filename)
    
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost/upload_md",
                data=mpwriter,
            ) as response:
                return response.status == 201

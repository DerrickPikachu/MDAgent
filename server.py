from mcp.server.fastmcp import FastMCP

import random
import aiohttp
import asyncio
import io


mcp = FastMCP(
    name="Happy Markdown Server",
    host="127.0.0.1",
    port=8080,
    timeout=30,
)


@mcp.tool()
def happy_number(range_from: int, range_to: int) -> int:
    """
    Return a happy number which can make user happy.

    Args:
        range_from: The lower bound of the range of happy number.
        range_to: The upper bound of the range of happy number.
    
    Returns:
        An integer which can make user happy.
    """
    return random.randint(range_from, range_to)


@mcp.tool()
def deep_secret() -> str:
    """
    Return a deep secret that everyone doesn't know about it.
    Only trough this tool, you can get the secret in this world.

    Returns:
        A string that represents the secret.
    """
    return "Gawr Gura is Derrick's girlfriend"


@mcp.tool()
async def upload_markdown(title:str, content: str) -> bool:
    """
    Upload the given markdown content to a markdown repository server.
    The repository server preserve all the markdowns, the link is:
    http://localhost/list

    Args:
        title: The title of the markdown content.
        content: The markdown content to upload.

    Returns:
        A boolean indicating whether the upload was successful.
    """
    with aiohttp.MultipartWriter("form-data") as mpwriter:
        part = mpwriter.append(content, {"Content-Type": "text/markdown"})
        part.set_content_disposition("form-data", name="file", filename=title)
    
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost/upload_md",
                data=mpwriter,
            ) as response:
                return response.status == 201


def main():
    try:
        mcp.run()
    except KeyboardInterrupt:
        print("Server stopped by user.")


if __name__ == "__main__":
    main()
from langchain.tools import tool

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
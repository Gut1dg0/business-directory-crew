from crewai.tools import tool
import requests

@tool("WordPress Publisher Tool")
def publish_to_wordpress(content: str, title: str) -> str:
    """
    Publishes HTML content to a WordPress site using the REST API.
    Make sure to set your credentials in the `auth` section.
    """
    url = "https://philt178.sg-host.com/wp-json/wp/v2/pages"
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "title": title,
        "content": content,
        "status": "publish"
    }

    # Insert your credentials here
    auth = ("support", "K2YVu9B54H28FzqsWl9fQbuK")

    response = requests.post(url, json=data, headers=headers, auth=auth)

    if response.status_code == 201:
        return response.json().get("link", "No link returned.")
    else:
        return f"Failed to publish: {response.status_code} - {response.text}"

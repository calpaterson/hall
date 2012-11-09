import os

import requests

def i_put_a_file():
    title = "The Fresh Prince"
    contents = "This is a story..."
    content_type = "text/plain; charset=utf-8"
    response = requests.post("http://localhost:{port}/contents/{title}".format(
            port = int(os.environ["HOM_PORT"]),
            title = title), data=contents, headers={"Content-Type": content_type})
    assert response.status_code == 201
    return title, contents, content_type

def i_get_a_file():
    title = "The Fresh Prince"
    response = requests.get("http://localhost:{port}/contents/{title}".format(
            port = int(os.environ["HOM_PORT"]),
            title = title))
    assert response.status_code == 200
    return title, response.text, response.headers["Content-Type"]


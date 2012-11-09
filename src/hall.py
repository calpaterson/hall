#!/usr/bin/python

from urllib import unquote
from wsgiref.simple_server import make_server
import json
import os

from boto.s3.key import Key
from bottle import Bottle, request, response
import boto


settings = {}

app = Bottle()

connection = boto.connect_s3()
bucket = None

@app.get("/")
def list():
    results = []
    for key in bucket.list():
        results.append(key.key)
    response.set_header("Content-Type", "application/json")
    return json.dumps(results, indent=4)

@app.post("/contents/<encoded_url>")
def post(encoded_url):
    key = Key(bucket)
    key.key = unquote(encoded_url)
    key.set_metadata("mime", request.headers["Content-Type"])
    key.set_contents_from_file(request.body)
    response.status = 201
    return request.body

@app.get("/contents/<encoded_url>")
def get(encoded_url):
    key = bucket.get_key(unquote(encoded_url))
    content_type = key.get_metadata("mime")
    response.set_header("content-type", content_type)
    return key.get_contents_as_string()

def main():
    global bucket
    bucket = connection.get_bucket(settings["HOM_BUCKET"])
    http_server = make_server("", int(settings["HOM_PORT"]), app)
    http_server.serve_forever()

if __name__ == '__main__':
    for name in os.environ:
        if name.startswith("HALL_"):
            settings[name] = os.environ[name]
    try:
        assert "HALL_BUCKET" in settings
        assert "HALL_PORT" in settings
    except AssertionError:
        print("You need to set the environment variables HALL_BUCKET " +
              "and HALL_PORT")
        exit(1)
    main()

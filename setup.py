import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
name = "REST-Service",
version = "0.0.1",
author = "iTzNoX",
author_email = "timothykropp39@gmail.com",
description = "A simple ToDo application with a local register and login function",
long_description = long_description,
long_description_content_type = "text/markdown",
url = "https://github.com/iTzNoX/REST-Service",
project_urls = "https://github.com/iTzNoX/REST-Service", 
license="MIT",
packages = ["FLASK"],
python_requires >= "3.11",
)

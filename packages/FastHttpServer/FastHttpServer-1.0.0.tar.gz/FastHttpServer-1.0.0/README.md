# FastHttpServer - Simple, Lightweight, and Fast HTTP Server

## Overview

**FastHttpServer** is a pip package that offers a simple, lightweight, and fast HTTP server implemented in Python. This server provides a minimalistic solution for serving static content and handling basic HTTP requests. It is designed to be easy to set up, efficient in serving web content, and accessible as a pip-installable package.

## Installation

To install FastHttpServer, use the following pip command:

```bash
pip install FastHttpServer
```

Also make sure the python 'socket' package is installed


## Usage

1. After installation, you can import and run the package:


```python
from FastHttpServer import App
app = App()
```

or, if App is already reserved:

```python
import FastHttpServer
app = FastHttpServer.App()
```

2. Specify the routes of the server

use the app route wrapper and specify the route path. Make sure the proceeding function has a request parameter:

```python
@app.route('/')
def index(request):
    return '<h1>Success!</h1>'
```

by default the route only accepts GET requests if you want to accept POST or any other, specify in the methods parameter of the route wrapper:

```python
@app.route('/', methods=['GET', 'POST'])
def index(request):
    if request['method'] == 'GET':
        return '<h1>Success</h1>'
    else:
        return {'message': 'Success!'}
```

It automatically detects html and json so no need to use json.dumps!

3. Run the server:

First, run the server by calling the listen function of 'app':

```python
app.listen()
```
By default, it runs on localhost port 3000 you can specify parameters to change both of those:

```python
app.listen(PORT=8000, ADDRESS='127.0.0.1')
```

Open your web browser and navigate to [http://localhost:3000](http://localhost:3000) (or the custom port and address you specified). You should see a success or 404 indicating that the server is running.


## Notes

- This server is suitable for serving static content in development and testing environments. For production use, consider security and scalability aspects.

- FastHttpServer is intentionally kept advanced and minimalistic.
 
- Make sure the server listen is called last the routes below it wont work.

Feel free to use and contribute to FastHttpServer. Keep your web serving simple and enjoy the speed!
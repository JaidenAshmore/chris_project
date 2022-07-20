# WSGI stands for 'Web Server Gateway Interface'
# it's a simple calling convention for web servers to forward requests to web applications or framworks written in Python

from app import app

if __name__ == '__main__':
    app.run()
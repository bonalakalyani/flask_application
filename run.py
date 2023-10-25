import os


if __name__ == '__main__':
    from wsgi import app

    app.run(debug=True)

import traceback

from flask import Flask, send_from_directory

app = Flask(__name__)


@app.route('/', defaults=dict(filename=None))
@app.route('/<path:filename>', methods=['GET', 'POST'])
def index(filename):
    filename = filename or 'index.html'
    # if request.method == 'GET':
    return send_from_directory('.', filename)


def main():
    while True:
        try:
            app.run(host="0.0.0.0", port=80)
        except:
            traceback.print_exc()


if __name__ == '__main__':
    main()

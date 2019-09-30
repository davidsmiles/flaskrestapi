from flask import Flask

app = Flask(__name__)


# endpoint => the request
@app.route('/')     # http://www.google.com/    -> homepage endpoint
def home():
    return 'hello david james' # the response


if __name__ == '__main__':
    app.run(port=5000, debug=True)
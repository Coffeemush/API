from flask import Flask

app = Flask(__name__)

#test
@app.route('/')
def index():
    return 'Connected to MongoDB!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
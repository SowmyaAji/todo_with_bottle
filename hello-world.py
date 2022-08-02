from bottle import Bottle, run, template
# from bottle import route, run
app = Bottle()


@app.route('/')
@app.route('hello')
def hello():
    return "Hello World!"


@app.route('/hello/<name>')
def greet(name="Stranger"):
    return template("Hello {{ name }}, how are you?", name=name)


@app.route('/hello/<name>')
def greet(name="Sowmya"):
    return template("Hello {{ name }}, how are you?", name=name)


if __name__ == "__main__":
    run(app=app, host="localhost", port=8080, debug=True)

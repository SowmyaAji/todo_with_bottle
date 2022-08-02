import sqlite3
from bottle import Bottle, run, debug, template, request, static_file, error
import os

# create instance of Bottle class
app = Bottle()

# set app basic url to root


@app.route("/")
# create todo endpoint
@app.route('/todo')
# assign secondary name to the same endpoint
@app.route('/my_todo_list')
# function to call the DB and display the list of todos
def todo_list():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    output = template('make_table', rows=result)
    return output

# create new todo items functionality


@app.route('/new', method='GET')
def new_item():
    # bottle's way of doing the get
    if request.GET.save:

        new = request.GET.task.strip()
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        # insert into sqlite3 db table todo (todo.db)file
        c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new, 1))
        # get the next id
        new_id = c.lastrowid

        conn.commit()
        c.close()

        return '<p>The new task was inserted into the database, the ID is %s</p>' % new_id
    else:
        return template('new_task.tpl')

# edit todo list


@app.route('/edit/<no:int>', method='GET')
def edit_item(no):

    if request.GET.save:
        edit = request.GET.task.strip()
        status = request.GET.status.strip()

        if status == 'open':
            status = 1
        else:
            status = 0

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute(
            "UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (edit, status, no))
        conn.commit()

        return '<p>The item number %s was successfully updated</p>' % no
    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no),))
        cur_data = c.fetchone()

        return template('edit_task', old=cur_data, no=no)

# use regex to retrieve and display data


@app.route('/item<item:re:[0-9]+>')
def show_item(item):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (item,))
    result = c.fetchall()
    c.close()
    if not result:
        return 'This item number does not exist!'
    else:
        return 'Task: %s' % result[0]

# get help to see routes -- serve up help static file


@app.route('/help')
def help():
    cwd = os.getcwd()
    path = cwd + '/static'
    return static_file('help.html', root=path)

# show results as json


@app.route('/json<json:re:[0-9]+>')
def show_json(json):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (json,))
    result = c.fetchall()
    c.close()

    if not result:
        return {'task': 'This item number does not exist!'}
    else:
        return {'task': result[0]}

# return error message


@app.error(403)
def mistake403(code):
    return 'The parameter you passed has the wrong format!'

# return error message


@app.error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'

# delete functionality for app


@app.route('/delete<item:re:[0-9]+>')
def delete(item):
    print(f'Item: {item}')
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (item,))
    res = ""
    result = c.fetchall()
    if not result:
        res = 'The item ID %s does not exist!' % item
    else:
        c.execute("DELETE FROM todo WHERE id=?", (item,))
        conn.commit()
        res = 'The item ID %s has been deleted' % item
    c.close()
    return res


debug(True)
if __name__ == "__main__":
    run(app=app, reloader=True)

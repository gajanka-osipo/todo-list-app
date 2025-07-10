from flask import Flask, render_template, redirect, url_for, make_response, request
from form import TaskForm
from config import Config
import json
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)


@app.route('/', methods=['POST','GET'])
def index():
    form = TaskForm()

    tasks_cookie = request.cookies.get('tasks')
    if tasks_cookie:
        tasks = json.loads(tasks_cookie)
    else:
        tasks = []

    id_counter = request.cookies.get('id_counter')
    if id_counter:
        id_counter = int(id_counter)
    else:
        id_counter = 1

    if form.validate_on_submit():
        new_task = {'id':id_counter,
                    'text':form.task.data,
                    'done':False}
        tasks.append(new_task)

        id_counter += 1

        res = make_response(redirect(url_for('index')))
        res.set_cookie('tasks', json.dumps(tasks), max_age = 60*60*24*365)
        res.set_cookie('id_counter',str(id_counter), max_age = 60*60*24*365)
        return res
    
    res = make_response(render_template("index.html", form=form, tasks=tasks))
    
    if not tasks:
        res.delete_cookie("tasks")
        res.delete_cookie("id_counter")
    
    return res

@app.route('/done/<int:task_id>')
def mark_done(task_id):
    tasks_cookie = request.cookies.get('tasks')

    if tasks_cookie:
        tasks = json.loads(tasks_cookie)
        for task in tasks:
            if task['id'] == task_id:
                task['done'] = True
                break
    else:
        tasks = []
                
    res = make_response(redirect(url_for('index')))
    res.set_cookie('tasks', json.dumps(tasks), max_age = 60*60*24*365)
    return res

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks_cookie = request.cookies.get('tasks')
    if tasks_cookie:
        tasks = json.loads(tasks_cookie)
        tasks = [task for task in tasks if task['id'] != task_id]
    else:
        tasks = []
    
    res = make_response(redirect(url_for('index')))
    res.set_cookie('tasks', json.dumps(tasks), max_age = 60*60*24*365)
    return res

@app.route('/delete_cookie')
def delete_cookie():
    res = make_response(redirect('/'))
    res.set_cookie('tasks', '', max_age=0)
    res.set_cookie('id_counter', '', max_age=0)
    return res

@app.route('/edit/<int:task_id>', methods=['POST','GET'])
def edit_task(task_id):
    form = TaskForm()
    tasks_cookie = request.cookies.get('tasks')

    if tasks_cookie:
        tasks = json.loads(tasks_cookie)
    else:
        tasks = []
    
    if form.validate_on_submit():
        for task in tasks:
            if task['id'] == task_id:
                task['text'] = form.task.data
                break
        res = make_response(redirect(url_for('index')))
        res.set_cookie('tasks', json.dumps(tasks), max_age = 60*60*24*365)
        return res
    return render_template('edit_task.html', form=form, tasks=tasks, task_id=task_id)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port = 5005, debug=True)
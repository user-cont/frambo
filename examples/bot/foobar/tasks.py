# create app attribute which celery looks for during start
from frambo.celery_app import app
from foobar.foobar import FooBarBot


# @app.task: create a task from any callable by using task() decorator
# see http://docs.celeryproject.org/en/latest/userguide/tasks.html#basics
# decorator arguments:
#   name: task name
#         see http://docs.celeryproject.org/en/latest/userguide/tasks.html#names
#         keep the 'task.yourbotname.taskname' scheme
@app.task(name="task.foobar.rebuild_now")
def rebuild_now(*args, **kwargs):
    bot = FooBarBot(task_name="task.foobar.rebuild_now")
    return bot.process(args[0])

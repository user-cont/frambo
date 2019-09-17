from frambo.celery_app import app

import time

if __name__ == "__main__":
    # Define which tasks go to which queue
    # http://docs.celeryproject.org/en/latest/userguide/routing.html#automatic-routing
    # http://docs.celeryproject.org/en/latest/userguide/tasks.html#names
    app.conf.update(task_routes={"task.foobar.rebuild_now": {"queue": "queue.foobar"}})

    # Submit task
    # http://docs.celeryproject.org/en/latest/reference/celery.html#celery.Celery.send_task
    # http://docs.celeryproject.org/en/latest/userguide/tasks.html#names
    result1 = app.send_task(name="task.foobar.rebuild_now", args=("foobar_ongoing",))

    # Give Celery some time to pick up the message from queue and run the task
    time.sleep(2)
    print("Task finished? ", result1.ready())
    print("Task result: ", result1.result)

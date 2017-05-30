from django.db import models
# Create your models here.


def get_userdata():
    import random
    notifications = {
        'updates': 0,
        'messages': 0,
        'tasks': 0,
        'comments': 0,
        'payments': 0,
        'projects': 0,
    }
    for k in notifications:
        n = random.randint(-50, 100)
        if n < 0:
            notifications[k] = 0
            continue
        for d in range(100, 0, -10):
            if n > d:
                n = str(d) + "+"
                break
        notifications[k] = n
    userdata = {
        'notifications': notifications,
        'avatar': str(random.randint(1, 8)) + ".jpg",
        'username': "d2emon",
        'email': "d2emonium@gmail.com",
    }
    return userdata

from django.db import models
from django.db import connection
import cx_Oracle
from django.views import View


class Person(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self):
        return self.name

class Feedback(models.Model):
    feed = models.CharField(max_length=1000)
    def __str__(self):
          return self.feed

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
class MY_UTIL():
    def getData(self):
        with connection.cursor() as dcursor:
            cursor = dcursor.connection.cursor()
            l_cur = cursor.var(cx_Oracle.CURSOR)
            cursor.callproc("TEST_PROC", [l_cur])
            res = l_cur.getvalue().fetchall()
            cursor.close()
        return res
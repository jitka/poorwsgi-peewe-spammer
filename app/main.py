from wsgiref.simple_server import make_server
from poorwsgi import Application, state
from poorwsgi.response import TextResponse, JSONResponse
from traceback import format_tb
import os
import peewee
import logging
from sys import exc_info
from random import shuffle

log = logging.getLogger('spammer')
app = Application('test')
db = peewee.MySQLDatabase(
    host=os.environ['MYSQL_HOST'],
    passwd=os.environ['MYSQL_PASSWORD'],
    user='root',
    database='spammer',
    charset='utf8mb4')


class Mess(peewee.Model):
    class Meta:
        database = db
    id = peewee.IntegerField(primary_key=True)
    next = peewee.IntegerField()


def shuffle_n(n: int):
    Mess.delete().execute()
    mess = list(range(n))
    shuffle(mess)
    for i in range(n):
        line = Mess.create(id=mess[i], next=mess[(i + 1) % n])
        line.save()


@app.http_state(state.HTTP_INTERNAL_SERVER_ERROR, state.METHOD_ALL)
@app.http_state(state.HTTP_SERVICE_UNAVAILABLE, state.METHOD_ALL)
def internal_server_error(req):
    """500/503 Internal Server Error handler."""
    type_, error, traceback = exc_info()
    traceback = format_tb(traceback)
    log.error('\n%s%s', ''.join(traceback), repr(error))
    kwargs = {}
    # printer and camera gets response as small as possible
    if app.debug:
        kwargs["traceback"] = traceback
        kwargs["error"] = str(error)
        kwargs["error_type"] = str(type_)
    return JSONResponse("SERVICE_UNAVAILABLE", status_code=503, **kwargs)


@app.route('/shuffle/<n:int>')
def shuffle_fce(req, n):
    shuffle_n(n)
    return TextResponse(str(n))


if __name__ == '__main__':
    shuffle_n(13)
    httpd = make_server('127.0.0.1', 8080, app)
    httpd.serve_forever()
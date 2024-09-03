import datetime
import re2
import time
from flask import Flask, render_template, request
from black.strings import lines_with_leading_tabs_expanded
from django.utils.translation.trans_real import get_language_from_request
from django.utils.translation import get_language
from django.http.response import HttpResponse
from django.utils.text import Truncator
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
# from embedchain.loaders.json import JSONLoader
from semgrep.meta import get_repo_name_from_repo_url
from semgrep.meta import get_url_from_sstp_url
from oauthlib.uri_validate import is_absolute_uri
from cleo import ui
from cleo.io.buffered_io import BufferedIO

from cleo.ui.table import Table
from cleo.ui.table_cell import TableCell
from cleo.ui.table_separator import TableSeparator
from cleo.ui.table_style import TableStyle
from cleo.ui.table_cell_style import TableCellStyle
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def root(): 
    return render_template("index.html")

def create_payload(char_length: int):
     return "\t" * char_length

def create_embedchain(char_length: int):
    url = "http://" + 'a' * char_length 
    return f'{{"name": "John Doe", "url": "{url}"}}'

@app.route("/black", methods=['GET', 'POST'])
def simple_app():
    # start_time = time.time()
    headers = request.headers
    content_type = headers.get('payload')
    print(request.headers)
    if content_type:
        start_time = time.time()
        content_len = len(content_type)
        print(content_len)
        lines_with_leading_tabs_expanded(create_payload(content_len))
        print("Time taken=============> ", time.time()-start_time)
    return "Ok"

@app.route("/django", methods=['GET', 'POST'])
def django_truncate():
    start_time = time.time()
    headers = request.headers
    print(headers)
    payload = headers.get('payload')
    if payload:
        Truncator(payload).words(3, truncate='...', html=True) 
        end_time = time.time()
        print('[INFO] Truncator().words() took %lf seconds' % (end_time - start_time))
    return "Ok"

@app.route("/intcomma", methods=['GET', 'POST'])
def django_intcomma():
    start_time = time.time()
    headers = request.headers
    payload = headers.get('payload')
    if payload:
        intcomma(payload)
        end_time = time.time()
        print('[INFO] Intcomma took %lf seconds' % (end_time - start_time))
    return "Ok"

def validate_url(url):
    validator = URLValidator()
    try:
        validator(url)
        return True
    except ValidationError:
        return False

@app.route("/URLValidator", methods=['GET', 'POST'])
def url_validator():
    start_time = time.time()
    headers = request.headers
    url = headers.get('payload')
    if url:
        validate_url(url)
        end_time = time.time()
        print('[INFO] URLValidator took %lf seconds' % (end_time - start_time))
    return "Ok"

# @app.route("/embedchain", methods=['GET', 'POST'])
# def embedchain():
#     start_time = time.time()
#     headers = request.headers
#     payload = headers.get('payload')
#     if payload:
#         print(payload, type(payload))
#         try:
#             content_len = len(payload)
#             content = create_embedchain(content_len)
#             result = JSONLoader.load_data(payload)
#             end_time = time.time()
#             print('[INFO] embedchain took %lf seconds' % (end_time - start_time))   
#         except ValueError as e:
#             print(f"An error occurred: {e}")
#     return "Ok"

@app.route("/semgrep", methods=['GET', 'POST'])
def semgrep():
    start_time = time.time()
    headers = request.headers
    payload = headers.get('payload')
    if payload:
        print(payload, type(payload))
        try:
            content_len = len(payload)
            payl = 'git://' + '@' * content_len
            try:
                get_repo_name_from_repo_url(payl)
            except:
                pass
            end_time = time.time()
            print('[INFO] semgrep took %lf seconds' % (end_time - start_time))   
        except ValueError as e:
            print(f"An error occurred: {e}")
    return "Ok"

@app.route("/oauthlib", methods=['GET', 'POST'])
def oauthlib():
    start_time = time.time()
    headers = request.headers
    payload = headers.get('payload')
    if payload:
        print(payload, type(payload))
        try:
            content_len = len(payload)
            try:
                is_absolute_uri("http://["+":"*content_len+"]/path")
            except:
                pass
            end_time = time.time()
            print('[INFO] oauthlib took %lf seconds' % (end_time - start_time))   
        except ValueError as e:
            print(f"An error occurred: {e}")
    return "Ok"

def column_style(i):
    io = BufferedIO()
    table = Table(io)
    table.set_headers(["ISBN", "Title", "Author", "Price"])

    table.set_rows([
                ["99921-58-10-7", "Divine Comedy", "Dante Alighieri"],
                TableSeparator(),
                [TableCell('<0=,' + '000=0'*i + '00=0>', colspan=3,style=TableCellStyle())],
                TableSeparator(),
                [TableCell("Arduino: A Quick-Start Guide", colspan=2), "Mark Schmidt"],
                TableSeparator(),
                ["9971-5-0210-0", TableCell("A Tale of \nTwo Cities", colspan=2)],
            ])

    style = TableStyle()
    style.set_pad_type("left")
    table.set_column_style(3, style)
    table.set_column_style(2, style)
    table.render()

@app.route("/celo", methods=['GET', 'POST'])
def celo():
    start_time = time.time()
    headers = request.headers
    payload = headers.get('payload')
    if payload:
        print(payload, type(payload))
        try:
            content_len = len(payload)
            try:
                column_style(content_len)
            except:
                pass
            end_time = time.time()
            print('[INFO] celo took %lf seconds' % (end_time - start_time))   
        except ValueError as e:
            print(f"An error occurred: {e}")
    return "Ok"


if __name__ == "__main__":
#     # This is used when running locally only. When deploying to Google App
#     # Engine, a webserver process such as Gunicorn will serve the app. This
#     # can be configured by adding an `entrypoint` to app.yaml.
#     # Flask's development server will automatically serve static files in
#     # the "static" directory. See:
#     # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
#     # App Engine itself will serve those files as configured in app.yaml.
#     app.run(host="127.0.0.1", port=8080, debug=True)
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=8080, debug=True)
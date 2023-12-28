import os
from flask import Flask, render_template, request
from markdown import markdown



app = Flask(__name__)


@app.route('/')
@app.route('/<file_name>/<edit>/<add_new>')
def index(file_name="framework_doc.md", edit="false", add_new="false"):
    all_docs = os.listdir("docs")
    with open(f"docs/{file_name}", "r", encoding="utf-8") as f:
        md_data = f.read()
    data = markdown(md_data, extensions=["fenced_code", "codehilite"])
    return render_template('index.html', data=data, md_data=md_data, current_file=file_name, docs=all_docs, edit=edit,
                           add_new=add_new)


@app.route('/save/<file_name>', methods=['POST'])
def save(file_name):
    if request.method == 'POST':
        rdata = request.get_data().decode("utf-8")
        with open(f"docs/{file_name}", "w", encoding="utf-8") as f:
            f.write(rdata)
    return "Success"


@app.route('/create/<file_name>', methods=['POST'])
def create(file_name):
    if request.method == 'POST':
        rdata = request.get_data().decode("utf-8")
        with open(f"docs/{file_name}", "w+", encoding="utf-8") as f:
            f.write(rdata)
    return "Success"


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=6677)

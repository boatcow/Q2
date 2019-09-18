import os
from utils import json_response
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
import pdfkit
app = Flask(__name__)
'''
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a1 = db.Column(db.String(200), default="")

    def __repr__(self):
        return '<Task %r>' % self.id

'''
'''
class List():
    def __init__(self, name,title,Description,ext):
        self.name=name
        self.title=title
        self.Description=Description
        self.ext=ext
'''

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['png', 'gif', 'jpeg', 'jpg'])

tmpl_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'static')

app = Flask(__name__, template_folder=tmpl_dir,
            static_folder=static_dir, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Limit uploads to 16MB. They'll get an
# Error 413 Request entity too large
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    """
    allowed_file just checks the acceptable extensions
      it could be extended to check the fileheader/mimetype
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/v/<item>")
def uploaded_file(item):
    return send_from_directory(app.config['UPLOAD_FOLDER'], item)

@app.route("/download",methods=['GET', 'POST'])
def download():
    pdfkit.from_url('http://0.0.0.0:5001/', 'out.pdf')
    return redirect(url_for("download")) 




@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        #choices=request.form["Templatechoices"]
        print("choices")
        print("yolo")
        a1=[]
        a2=[]
        a3=[]
        a4=[]
        line = file.readline()
        print(line)

        while True:
            # read line
            line = file.readline()
            line=line.decode("utf-8") 
            # in python 2, print line
            # in python 3
            #print(line)

            if("Function  :" in line):
                name=line
                name=name.replace("/*! \\Function  :","")
                name=name.replace(" ","")
                name=name.replace("/","")
                name=name[:-1]
                a1.append(name)
                #print(name)
            if("#define" in line):
                title=line
                title=title.replace('#define',"")
                title=title.replace(" ","")
                title=title[:-1]
                a2.append(title)
                #print(title)
            if("Description :" in line):
                Description=line
                Description=Description.replace("/*!Description :","")
                Description=Description.replace(" ","")
                Description=Description[:-1]
                a3.append(Description)
                #print(Description)
            if("extern" in line):
                ext=line
                ext=ext.replace("extern ","")
                ext=ext[:-1]
                a4.append(ext)
                #print(ext)
            # check if line is not empty
            if not line:
                break
        print(a1)
        print(a2)
        print(a3)
        print(a4)    
        '''
        for i in a2:
            b=Todo(a2=a2)
        
        for i in a3:
            c=Todo(a3=a3)
        
        for i in a4:
            d=Todo(a4=a4)
        '''
        #db.session.add(a)
        #tasks = Todo.query.all()
        return render_template('output.html',a1=a1,a2=a2,a3=a3,a4=a4,limit1=5,limit2=2)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    files = dict(
        zip(os.listdir(app.config['UPLOAD_FOLDER']),
            ["/v/{}".format(k) for k in os.listdir(app.config['UPLOAD_FOLDER'])]))
    return render_template('/file_list.html', file_list=files)


@app.route("/upload", methods=['POST'])
def upload():
    """
    Plugin should be able to upload here and give us back a URL/item ID for us
      to reuse to download and populate using AJAX magic
    """
    file = None
    if 'file' in request.files:
        file = request.files['file']
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return json_response(
            message="Upload successful",
            result="/v/{}".format(filename)
        )
    return json_response(
        message="Invalid filename or extension (jpg, png, gif)",
        status_code=500
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)

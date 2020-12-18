from flask import Flask,render_template,redirect,url_for,request,session,flash
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.secret_key = "saran"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:vsvsmanikanta@localhost/information"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
conn = psycopg2.connect(database = "information", user= 'postgres', password = 'vsvsmanikanta', host = '127.0.0.1', port= '5432')
conn.autocommit = True
cursor = conn.cursor()
db = SQLAlchemy(app)
length =0
length_inf =0
inf =[]
num =0
result = ''
class Faculty(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer,primary_key = True)
    faculty_name = db.Column(db.String(50))
    mobile = db.Column(db.String(50))
    degignation = db.Column(db.String(50))
    department = db.Column(db.String(50))

class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer,primary_key = True)
    subject_name = db.Column(db.String(50))
    subject_code = db.Column(db.String(50))
    regulation = db.Column(db.String(50))
    faculty_name = db.Column(db.String(50))
    department = db.Column(db.String(50))


@app.route('/')
def index():
    cursor.execute("select faculty_name from data")
    result = cursor.fetchall()
    length = len(result)
    print(result)

    return render_template('frame.html',result = result,length = length,length_inf = 0,inf = 0)
    # return redirect(url_for('faculty'))

@app.route('/faculty',methods=["POST","GET"])
def faculty():
    
    cursor.execute("select faculty_name from data")
    result = cursor.fetchall()
    length = len(result)
    # conn.close()
    if request.method == "POST":

        fac_name = request.form['fac_name']
        mobile = request.form['mobile']
        degignation = request.form['degignation']
        department = request.form['department']
        
        fac_details = Faculty(faculty_name = fac_name.lower(),mobile = mobile,degignation = degignation,department = department)
        db.session.add(fac_details)
        db.session.commit()
        cursor.execute("select faculty_name from data")
        result = cursor.fetchall()
        length = len(result)
        print(result)
        flash('Faculty Added Successfully')
        return redirect('/')

    
    return render_template('frame.html',result = result,length = length,length_inf = length_inf,inf = inf)

@app.route('/subject',methods = ['POST','GET'])
def subject():

    if request.form['subject'] == 'subject':

        # fac_name = request.form['fac_name']
        sub_name = request.form['sub_name']
        sub_code = request.form['sub_code']

        department = request.form['branch']
        regulation = request.form['regulation']
        faculty = request.form['faculty']

        cursor.execute("select faculty_name from data")
        result = cursor.fetchall()
        length = len(result)
        print(result)

        details = Subject(subject_name= sub_name, subject_code = sub_code,regulation = regulation,faculty_name = faculty,department = department)

        db.session.add(details)
        db.session.commit()

        flash('subject added successfully')
        return render_template('frame.html',result = result,length = length,length_inf = length_inf,inf = inf)
    return render_template('frame.html',result = result,length = length,length_inf = length_inf,inf = inf)

@app.route('/search',methods =['POST','GET'])
def search():
   
    cursor.execute('select faculty_name from data ')
    result = cursor.fetchall()
    length = len(result)
    # print(session['sub_name'])
    if request.method == 'POST':
        # if request.form['submit'] == ['submit']:
        search = request.form['department']

        cursor.execute("select * from subject where department = %s",[search])
        inf = cursor.fetchall()
        length_inf = len(inf)
        print(inf,length_inf) 
        return render_template('frame.html',length_inf = length_inf, inf = inf, result = result,length = length)
    
    return render_template('frame.html',length_inf = length_inf,inf = inf,result = result,length = length)

@app.route('/delete',methods =['POST','GET'])
def delete():
    

    if request.method == 'POST':

        delete1 = request.form['delete']


        Subject.query.filter_by(faculty_name = delete1).delete()
        Faculty.query.filter_by(faculty_name = delete1.lower()).delete()
        db.session.commit()

        flash("Faculty deleted Successfully")
        return redirect('/')
        # return render_template('frame.html',length_inf = 0,inf = [],result = result,length = length)

    return render_template('frame.html',length_inf = 0,inf = [],result = result,length = length)

@app.route('/task',methods = ['POST','GET'])
def task():
    if request.method == "POST":

        name = request.form['fname']
        code = request.form['code']
        subject = request.form['subject']
        reg = request.form['reg']
        cursor = conn.cursor()
        cursor.execute('select * from data where faculty_name = %s',[name])
        form = cursor.fetchmany(1)
        print(form) 
        form_len = len(form)
        return render_template('task.html',form = form,form_len = form_len)
    return render_template('task.html',form = form,form_len = form_len)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
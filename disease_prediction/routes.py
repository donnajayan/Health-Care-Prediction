from flask import Flask, render_template, request, redirect,  flash, abort, url_for
# from disease_prediction import app,db,bcrypt,mail
from disease_prediction import app,db,mail
from disease_prediction import app
from disease_prediction.models import *
from disease_prediction.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from random import randint
import os
from PIL import Image
from flask_mail import Message


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/predict')
def predict():
    import clean_code
    return render_template("user_index.html")


@app.route('/gallery')
def gallery():
    return render_template("gallery.html")




@app.route('/')
def index():
    return render_template("index.html")


@app.route('/services')
def services():
    return render_template("services.html")




@login_required
@app.route('/admin_index')
def admin_index():
    return render_template("admin_index.html")

@login_required
@app.route('/doctor_index/<id>')
def doctor_index(id):
    return render_template("doctor_index.html")


@login_required
@app.route('/user_index/<id>')
def user_index(id):
    return render_template("user_index.html")





@app.route('/login', methods=["GET","POST"])
def login():
     form = LoginForm()
     if form.validate_on_submit():
         admin = Login.query.filter_by(username=form.username.data, password=form.password.data,usertype= 'admin').first()
         doctor=Login.query.filter_by(username=form.username.data,password=form.password.data, usertype= 'doctor').first()
         user=Login.query.filter_by(username=form.username.data,password=form.password.data, usertype= 'user').first()
        #  public=Login.query.filter_by(username=form.username.data, usertype= 'public').first()
         if admin:
             login_user(admin)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect('/admin_index') 
             
         if doctor:
             login_user(doctor)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect('/doctor_index/'+str(doctor.id))
         
         if user:
             login_user(user)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect('/user_index/'+str(user.id)) 
         
        #  if public:
        #      login_user(public)
        #      next_page = request.args.get('next')
        #      return redirect(next_page) if next_page else redirect('/public_index') 

     return render_template("login.html", form = form)



@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')


@app.route('/add_doctor',methods=['GET', 'POST'])
@login_required
def add_doctor():
    form=AddDoctorForm()
    if form.validate_on_submit():
        if form.image.data:
            pic_file = save_picture(form.image.data)
            view = pic_file
        print(view)  
        em=form.email.data
        pswd=form.password.data
        obj1 = Doctor(name=form.name.data,image=view,email=form.email.data,specialisation = form.specialisation.data,department = form.department.data,contact=form.contact.data,password=form.password.data)
        obj2=Login(username=form.email.data,password = form.password.data,usertype="doctor",name=form.name.data,contact=form.contact.data)
        db.session.add(obj1)
        db.session.add(obj2)
        db.session.commit()
        ad_sendmail(em,pswd)
        # flash('Product added')
        return redirect('/admin_index')
    return render_template("add_doctor.html",form=form)



def ad_sendmail(em,pswd):
    
    msg = Message('Password',
                  recipients=[em])
    msg.body = f'''  You can login using your Mail ID and Your Password is {pswd} '''
    mail.send(msg)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)



def save_picture(form_picture):
    random_hex = random_with_N_digits(14)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@login_required
@app.route('/view_doctor',methods=["GET","POST"])
def view_doctor():
    obj = Doctor.query.all()
    return render_template("view_doctor.html",obj=obj)


@login_required
@app.route('/view_users',methods=["GET","POST"])
def view_users():
    obj = User.query.all()
    return render_template("view_users.html",obj=obj)



@login_required
@app.route('/admin_view_users',methods=["GET","POST"])
def admin_view_users():
    obj = User.query.all()
    return render_template("admin_view_users.html",obj=obj)


@login_required
@app.route('/admin_view_feedbacks',methods=["GET","POST"])
def admin_view_feedbacks():
    obj = Feedback.query.all()
    return render_template("admin_view_feedbacks.html",obj=obj)


@login_required
@app.route('/view_doctor_feedbacks',methods=["GET","POST"])
def view_doctor_feedbacks():
    obj = DoctorFeedback.query.all()
    return render_template("view_doctor_feedbacks.html",obj=obj)


@login_required
@app.route('/doctor_view_feedbacks',methods=["GET","POST"])
def doctor_view_feedbacks():
    obj = Feedback.query.all()
    return render_template("doctor_view_feedbacks.html",obj=obj)



@login_required
@app.route('/doctor_view_query',methods=["GET","POST"])
def doctor_view_query():
    obj = User2.query.all()
    return render_template("doctor_view_query.html",obj=obj)

@login_required
@app.route('/user_view_query',methods=["GET","POST"])
def user_view_query():
    obj = User3.query.all()
    return render_template("user_view_query.html",obj=obj)


@login_required
@app.route('/doctor_reply',methods=["GET","POST"])
def doctor_reply():
    obj = User2.query.all()
    return render_template("doctor_reply.html",obj=obj)

@login_required
@app.route('/view_query',methods=["GET","POST"])
def view_query():
    obj = User3.query.all()
    return render_template("view_query.html",obj=obj)

@login_required
@app.route('/user_view_doctor',methods=["GET","POST"])
def user_view_doctor():
    obj = Doctor.query.all()
    return render_template("user_view_doctor.html",obj=obj)


@login_required
@app.route('/edit_doctor/<int:id>', methods=['GET', 'POST'])
def edit_doctor(id):
    obj = Doctor.query.get_or_404(id)
    if request.method == 'POST':
        obj.name = request.form['name']
        obj.email = request.form['email']
        obj.specialisation = request.form['specialisation']
        obj.department = request.form['department']
        obj.contact = request.form['contact']
        db.session.commit()
        return redirect('/view_doctor')
    return render_template('edit_doctor.html', obj=obj)

@app.route('/delete_doctor/<int:id>')
@login_required
def delete_doctor(id):
    delet = Doctor.query.get_or_404(id)

    try:
        db.session.delete(delet)
        db.session.commit()
        return redirect('/view_doctor')
    except:
        return 'There was a problem deleting that task'


@app.route('/register_user',methods=['GET', 'POST'])
def register_user():
    form=AddUserForm()
    if form.validate_on_submit():
        obj1 = User(name=form.name.data,age = form.age.data,gender = form.gender.data,address= form.address.data,place = form.place.data,email=form.email.data,contact=form.contact.data,password = form.password.data)
        obj2=Login(username=form.email.data,password = form.password.data,usertype="user",name=form.name.data,contact=form.contact.data)
        db.session.add(obj1)
        db.session.add(obj2)
        db.session.commit()
     
        # flash('Product added')
        return redirect('/')
    return render_template("register_user.html",form=form)


def sendmail():
    msg = Message('successful',
                  recipients=[current_user.email])
    msg.body = f''' Your Registeration is successful... Login using the link   'http://127.0.0.1:5000/login' '''
    mail.send(msg)




@login_required
@app.route('/user_contact/<id>', methods = ['GET','POST'])
def user_contact(id):
    h=Login.query.filter_by(id=id).first()
 
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']
        my_data = Feedback(name=name, email=email,phone=phone,subject=subject,message=message)
        db.session.add(my_data) 
        db.session.commit()
        sendmail()
        return redirect('/user_index/'+str(current_user.id))
    else :
        return render_template("user_contact.html",h=h)

def sendmail():
    msg = Message('successful',
                  recipients=[current_user.username])
    msg.body = f''' Thanks for sending your valuable feedback' '''
    mail.send(msg)

@login_required
@app.route('/doctor_contact/<id>', methods = ['GET','POST'])
def doctor_contact(id):
    h=Login.query.filter_by(id=id).first()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']
        my_data = DoctorFeedback(name=name, email=email,phone=phone,subject=subject,message=message)
        db.session.add(my_data) 
        db.session.commit()
        sendmail()
        return redirect('/doctor_index/'+str(current_user.id))
    else :
        return render_template("doctor_contact.html",h=h)



@app.route('/contact', methods = ['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']
        my_data = Feedback(name=name, email=email,phone=phone,subject=subject,message=message)
        db.session.add(my_data) 
        db.session.commit()
        return redirect('/')
    else :
        return render_template("contact.html")

@login_required
@app.route('/user_make_query/<id>', methods = ['GET','POST'])
def user_make_query(id):
    h=Login.query.filter_by(id=id).first()
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        message = request.form['message']
        my_data = User2(name=name, subject=subject,message=message)
        db.session.add(my_data)
        db.session.commit()
        return redirect('/user_index/'+str(current_user.id))
    return render_template("user_make_query.html",h=h)



@app.route('/doctor_add_reply/<int:id>', methods=['GET', 'POST'])
@login_required
def doctor_add_reply(id):
    d = User2.query.get_or_404(id)
    if request.method == 'POST':
        d.name = request.form['name']
        d.subject = request.form['subject'] 
        d.message = request.form['message']
        reply = request.form['reply']
        my_data = User3(name=d.name, subject=d.subject,message=d.message,reply=reply)
        db.session.add(my_data)
        db.session.delete(d)
        db.session.commit()
        return redirect('/doctor_index/'+str(current_user.id))
    return render_template('doctor_add_reply.html', d=d)

@login_required
@app.route('/view_query_response/<int:id>', methods=['GET', 'POST'])
def view_query_response(id):
    d = User3.query.get_or_404(id)
    if request.method == 'POST':
        d.name = request.form['name']
        d.subject = request.form['subject']
        d.message = request.form['message']
        d.reply = request.form['reply']
        return redirect('/doctor_index/'+str(current_user.id))
    return render_template('view_query_response.html', d=d)
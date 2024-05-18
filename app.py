from flask import Flask,flash,redirect,render_template,url_for,request,jsonify,session,abort
from flask_session import Session
import mysql.connector
from datetime import date
from datetime import datetime
from sdmail import sendmail
from tokenreset import token
from itsdangerous import URLSafeTimedSerializer
from key import *
from stoken1 import token1
app=Flask(__name__)
app.secret_key='hello'
app.config['SESSION_TYPE'] = 'filesystem'
mydb=mysql.connector.connect(host="localhost",user="root",password="admin",db='faculty')
Session(app)
@app.route('/')
def index():
    return render_template('index.html')
#=========================================Faculty login and register
@app.route('/flogin',methods=['GET','POST'])
def flogin():
    if session.get('faculty'):
        return redirect(url_for('faculty_dashboard'))
    if request.method=='POST':
        username=request.form['id1']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('SELECT count(*) from faculty where faculty_id=%s and password=%s',[username,password])
        count=cursor.fetchone()[0]
        if count==1:
            session['faculty']=username
            return redirect(url_for("faculty_dashboard"))
        else:
            flash('Invalid username or password')
            return render_template('faculty_login.html')
    return render_template('faculty_login.html')

@app.route('/fregistration',methods=['GET','POST'])
def fregistration():
    if request.method=='POST':
        id1=request.form['id']
        username = request.form['username']
        password=request.form['password']
        email=request.form['email']
        phnumber=request.form['phone_number']
        
        address=request.form['address']
        role=request.form['role']
        ccode=request.form['ccode']
        Dob=request.form['date_of_birth']
        sex=request.form['gender']
        dept=request.form['department']
        Doj=request.form['joining_date']
        bloodgrp=request.form['blood_group']
        supervisor=request.form['supervisor']
       
        print(Dob,sex,dept,Doj,bloodgrp)
        code="codegnan@9"
        if code == ccode:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from faculty where faculty_id=%s',[id1])
            count=cursor.fetchone()[0]
            cursor.execute('select count(*) from faculty where email=%s',[email])
            count1=cursor.fetchone()[0]
            cursor.close()
            if count==1:
                flash(f'{username} already in use')
                return render_template('faculty_login.html',count=count)
            elif count1==1:
                flash('Email already in use')
                return render_template('faculty_login.html',count1=count1)
            
            data={'faculty_id':id1,'username':username,'password':password,'email':email,'phone_number':phnumber,'address':address,'role':role,'Dob':Dob,'sex':sex,'dept':dept,'Doj':Doj,'bg':bloodgrp,'supervisor':supervisor}
            subject='Email Confirmation'
            body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('fconfirm',token=token(data,salt),_external=True)}"
            sendmail(to=email,subject=subject,body=body)
            flash('Confirmation link sent to mail')
            return redirect(url_for('fregistration'))
        else:
            flash("faculty code is wrong unauthorized access!")
            return redirect(url_for('fregistration'))
    return render_template('faculty_login.html')
@app.route('/fconfirm/<token>')
def fconfirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
      
        return 'Link Expired register again'
    else:
        cursor=mydb.cursor(buffered=True)
        id1=data['faculty_id']
        cursor.execute('select count(*) from faculty where faculty_id=%s',[id1])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.close()
            flash('You are already registerterd!')
            return redirect(url_for('flogin'))
        else:
           
            cursor.execute('INSERT INTO faculty (faculty_id,username, password, email, phone_number, address,role,date_of_birth,gender,department,joining_date,blood_group,supervisor) VALUES (%s,%s,%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)',[data['faculty_id'],data['username'], data['password'], data['email'], data['phone_number'], data['address'],data['role'],data['Dob'],data['sex'],data['dept'],data['Doj'],data['bg'],data['supervisor']])
            mydb.commit()
            cursor.close()
            flash('Details registered!')
            return redirect(url_for('faculty_dashboard'))
@app.route('/forget',methods=['GET','POST'])
def forgot():
    if request.method=='POST':
        id1=request.form['id1']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from faculty where username=%s',[id1])
        count=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            cursor=mydb.cursor(buffered=True)

            cursor.execute('SELECT email  from faculty where username=%s',[id1])
            email=cursor.fetchone()[0]
            cursor.close()
            subject='Forget Password'
            confirm_link=url_for('reset',token=token(id1,salt=salt2),_external=True)
            body=f"Use this link to reset your password-\n\n{confirm_link}"
            sendmail(to=email,body=body,subject=subject)
            flash('Reset link sent check your email')
            return redirect(url_for('flogin'))
        else:
            flash('Invalid email id')
            return render_template('forgot.html')
    return render_template('forgot.html')


@app.route('/reset/<token>',methods=['GET','POST'])
def reset(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        id1=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Link Expired')
    else:
        if request.method=='POST':
            newpassword=request.form['npassword']
            confirmpassword=request.form['cpassword']
            if newpassword==confirmpassword:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update  faculty set password=%s where username=%s',[newpassword,id1])
                mydb.commit()
                flash('Reset Successful')
                return redirect(url_for('flogin'))
            else:
                flash('Passwords mismatched')
                return render_template('newpassword.html')
        return render_template('newpassword.html')

@app.route('/faculty_dashboard')
def faculty_dashboard():
    if session.get('faculty'):

        return render_template('faculty_dashboard.html')
    else:
        return redirect(url_for('flogin'))
@app.route('/flogout')
def flogout():
    if session.get('faculty'):
        session.pop('faculty')
        flash('Successfully loged out')
        return redirect(url_for('flogin'))
    else:
        return redirect(url_for('flogin'))
    
#============apply for leave
@app.route('/apply_leave',methods=['GET','POST'])
def apply_leave():
    if session.get('faculty'):
        if request.method=='POST':
            faculty_id = request.form['faculty_id']
            leave_type = request.form['leave_type']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            #status = 'pending'  # Assuming the status is always pending when a leave application is submitted
            cursor=mydb.cursor(buffered=True)
            cursor.execute('''INSERT INTO LeaveApplications (faculty_id, leave_type, start_date, end_date)VALUES (%s, %s, %s, %s)''', (faculty_id, leave_type, start_date, end_date))
            mydb.commit()
            cursor.close()
            flash("leave application successfully submitted")
            return redirect(url_for('faculty_dashboard'))  # Redirect to the faculty dashboard after submitting the leave application

            
        return render_template('leave_application.html')
    else:
        return redirect(url_for('flogin'))
#==================view the leave status
@app.route('/view_status',methods=['GET','POST'])
def view_status():
    if session.get('faculty'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from leaveapplications where faculty_id=%s',(session['faculty'],))
        view=cursor.fetchall()
        cursor.execute('SELECT start_date,DATE_ADD(start_date, INTERVAL allocated_leaves DAY) AS end_date FROM leaveapplications where faculty_id=%s',[session['faculty']])
        duration=cursor.fetchone()
        if request.method=='POST':
            id1 = request.form['leave_id']
            cursor.execute('delete from leaveapplications where leave_id=%s',[id1])
            mydb.commit()
            cursor.close()
            flash('leave application deleted successfully')
            return redirect(url_for('view_status'))
        return render_template('leave_status.html',view=view,duration=duration)
    else:
        return redirect(url_for('flogin'))
#========================= workload assignment
@app.route('/workload',methods=['GET','POST'])
def workload():
    if session.get('faculty'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from workload where faculty_id=%s',(session['faculty'],))
        view = cursor.fetchall()
        if request.method=='POST':
         
            workload_description=request.form['workload_description']
            dept=request.form['dept']
            cursor.execute('insert into workload (faculty_id,workload_description,dept) values (%s,%s,%s)',(session['faculty'],workload_description,dept))
            mydb.commit()
            cursor.close()
            flash('workload submitted')
            return redirect(url_for('workload'))
        return render_template('work_load.html',view=view)
    else:
        return redirect(url_for('flogin'))
#=============================================================================
#==================== Administrator login
@app.route('/administrator_login',methods=['GET','POST'])
def alogin():
  
    if request.method=='POST':
        email=request.form['email']
        code = request.form['code']
        email1="admin@codegnan.com"
        code1="admin@123"
        if email == email1: 
            if code == code1:
                session['admin']=code1
                return redirect('admindashboard')
        else:
            flash("unauthorized access")
            return redirect(url_for('alogin'))
    
    return render_template('administrator_login.html')
#=======================admin dashboard
@app.route('/admindashboard')
def admindashboard():
    if session.get('admin'):
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('alogin'))

#==view all faculty memebers
@app.route('/viewfaculty',methods=['GET','POST'])
def viewfaculty():
    if session.get('admin'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from faculty')
        view = cursor.fetchall()
        if request.method == 'POST':
            faculty_id=request.form['faculty_id']
            print(faculty_id)
            status= request.form['status']
            cursor.execute('update faculty set member_status=%s where faculty_id=%s',[status,faculty_id])
            mydb.commit()
            cursor.close()
            flash(f'faculty member {faculty_id} updated  successfully')
            return redirect(url_for('viewfaculty'))
        return render_template('view_faculty.html',view=view)
    else:
        return redirect(url_for('alogin'))

@app.route('/algout')
def alogout():
    if session.get('admin'):
        session.pop('admin')
        flash('successfully log out')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('alogin'))

#=== allocate leaves
@app.route('/allocate_leaves', methods=['GET', 'POST'])
def allocate_leaves():
   if session.get('admin'):
       cursor=mydb.cursor(buffered=True)
       cursor.execute('''
                    SELECT 
            faculty_id,
            SUM(DATEDIFF(end_date, start_date) + 1) AS leave_count
        FROM 
            leaveapplications
        GROUP BY 
            faculty_id;
        ''')
       faculty=cursor.fetchall()
       print(faculty)
       if request.method=='POST':
           faculty_id=request.form['id1']
           print(faculty_id)
           allocated_leaves=request.form['allocated_leaves']
           print(allocated_leaves)
           cursor=mydb.cursor(buffered=True)
           cursor.execute('update leaveapplications set allocated_leaves=%s where faculty_id =%s',[allocated_leaves,faculty_id])
           mydb.commit()
           cursor.close()
           flash(f'updated {faculty_id} allocated leaves')
           return redirect(url_for('admindashboard'))

       return render_template('allocate_leaves.html',faculties=faculty)
#=========leave applications
@app.route('/view_leaves',methods=['GET','POST'])
def viewleaves():
    if session.get('admin'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select f.faculty_id,f.username,f.role,f.member_status,l.leave_type,l.start_date,l.end_date,l.status,l.leave_id from faculty as f left join leaveapplications as l on f.faculty_id=l.faculty_id where f.faculty_id = l.faculty_id')
        view=cursor.fetchall()
        if request.method=='POST':
            leave_id=request.form['leave_id']
            status=request.form['status']
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select faculty_id from leaveapplications where leave_id=%s',[leave_id])
            faculty_id=cursor.fetchone()[0]
            cursor.execute('select email from faculty where faculty_id=%s',[faculty_id])
            email=cursor.fetchone()[0]

            cursor.execute('update leaveapplications set status=%s where leave_id =%s',[status,leave_id])
            mydb.commit()
            cursor.close()
            subject='Leave Status'
            body=f"Your leave status is {status}"
            sendmail(to=email,subject=subject,body=body)
            flash('status sent to faculty email')
            flash(f'status {leave_id} updated successfully')
            return redirect(url_for('viewleaves'))
        return render_template('view_leaves.html',view=view)
    else:
        return redirect(url_for('login'))
@app.route('/view_workload', methods=['GET', 'POST'])
def view_workload():
    if session.get('admin'):
        cursor = mydb.cursor(buffered=True)
        cursor.execute('''
            SELECT f.faculty_id, f.username, f.role, f.member_status, 
                   w.workload_description, w.submission_date, w.status, 
                   w.workload_id, f.department 
            FROM faculty AS f 
            LEFT JOIN workload AS w ON f.faculty_id = w.faculty_id
        ''')
        view = cursor.fetchall()

        cursor.execute('''
    SELECT f.faculty_id, f.department, 
           l.start_date,l.end_date,l.allocated_leaves FROM faculty AS f JOIN leaveapplications AS l ON f.faculty_id = l.faculty_id
''')

        data = cursor.fetchall()

        ids_without_conflict = set()

        for i in range(len(data)):
            id_i, start_i, end_i = data[i][0], data[i][2], data[i][3]
            conflict_found = False
            
            for j in range(len(data)):
                if i != j and data[i][1]==data[j][1]:  # Avoid comparing the same entry
                    start_j, end_j = data[j][2], data[j][3]
                    
                    # Check for conflict
                    if not ((end_i < start_j) or (start_i > end_j)):
                        # Conflict found, break the inner loop
                        conflict_found = True
                        break
            
            # If no conflict found for entry i, add pairs with i coming second
            if not conflict_found:
                for j in range(len(data)):
                    if i != j and data[i][1]==data[j][1]:
                        ids_without_conflict.add((data[j][0], id_i,data[i][1]))  # Add pairs with comparison entry first

        # Now let's add pairs with entry i coming first
        for entry in ids_without_conflict.copy():
            ids_without_conflict.add((entry[1], entry[0],entry[2]))

        #print(ids_without_conflict)

        if request.method == 'POST':
            work_id = request.form['work_id']
            status = request.form['status']
            response_date = datetime.now()
            cursor.execute('''
                UPDATE workload 
                SET status = %s, response_date = %s 
                WHERE workload_id = %s
            ''', [status, response_date, work_id])
            mydb.commit()
            flash("Workload status updated successfully")
            return redirect(url_for('view_workload'))

        cursor.close()  # Close the cursor after executing all queries
        return render_template('view_workload.html', view=view, data=data,data1=ids_without_conflict)
    else:
        return redirect(url_for('alogin'))

@app.route('/assignwork_load/<fid>',methods=['GET','POST'])
def assignworkload(fid):
    if session.get('admin'):
        if request.method=='POST':
            work_id=request.form['work_id']
            print(work_id)
            assigned_to=request.form['assign']
            leavecount=request.form['leavecount']
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into workload_assignment(from_faculty_id,to_faculty_id,workload_id) values(%s,%s,%s)',[fid,assigned_to,work_id])
            mydb.commit()

            cursor.execute('select workload_description from workload where workload_id=%s',[work_id])
            work=cursor.fetchone()[0]
            
            cursor.execute('SELECT start_date,DATE_ADD(start_date, INTERVAL allocated_leaves DAY) AS end_date FROM leaveapplications where faculty_id=%s',[fid])
            duration=cursor.fetchone()
            print(duration)
            cursor.execute('select email from faculty where faculty_id=%s',[assigned_to])
            email=cursor.fetchone()[0]
            
            cursor.close()
            
            flash(f"workload assigned to {assigned_to}  successfully")
            subject='Workload Assignment'
            body=f"Faculty {fid} workload ' {work} ' has been assigned to you from {duration[0]} to {duration[1]}"
            sendmail(to=email,subject=subject,body=body)
            flash('Workload sent to faculty email')
            return redirect(url_for('view_workload'))

        return redirect(url_for('view_workload'))
    return redirect(url_for('alogout'))
app.run(use_reloader=True,debug=True)

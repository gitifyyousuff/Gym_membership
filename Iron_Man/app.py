from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2  # pip install psycopg2
import psycopg2.extras
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import date
from flask_login import login_user, login_required, logout_user, current_user,LoginManager,UserMixin

# import datetime

app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"

# DB_HOST = "localhost"
# DB_NAME = "ironman"
# DB_USER = "postgres"
# DB_PASS = "Magnus@14"

DB_HOST = "ec2-54-146-82-179.compute-1.amazonaws.com"
DB_NAME = "dc54hvctibec5e"
DB_USER = "xwuydulcxwtikv"
DB_PASS = "0d50de23165145b5b9f759fcb8f886b4bfe3151e66665d26ec90213b239b099b"


conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASS, host=DB_HOST)

@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM members"
    cur.execute(s)  # Execute the SQL
    list_users = cur.fetchall()
    return render_template('index.html', list_users=list_users)


def numOfDays(date1, date2):
    return (date1-date2).days


@app.route('/member')
def member():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM members"
    cur.execute(s)  # Execute the SQL
    list_users = cur.fetchall()
    # YY-mm-dd
    today = date.today()
    date2 =  today          
    for i in list_users:
        length = len(i)
        date1 = (i[length-1])
        res = numOfDays(date1, date2)
        if(res < 0):
            i.append('Expired')
        else:
            i.append(res)

    # print(list_users) 
    return render_template('member.html', list_users=list_users)

@app.route('/add_members', methods=['POST'])
def add_members():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        member_id = request.form['member_id']
        member_name = request.form['member_name']
        mobile_number = request.form['mobile_number']
        j_date = request.form['j_date']
        s_date = request.form['s_date']
        plan = request.form['plan']
        date_format = '%Y-%m-%d'
        dtObj = datetime.strptime(s_date, date_format)
        #Expiry date calculations
        if(plan):
            if(plan == "1"):
                n = 30
                expiry_date = dtObj + relativedelta(days=n)
                print(expiry_date.date())
            elif(plan == "3"):
                n = 90
                expiry_date = dtObj + relativedelta(days=n)
                print(expiry_date.date())
            elif(plan == "6"):
                n = 180
                expiry_date = dtObj + relativedelta(days=n)
                print(expiry_date.date())
            elif(plan == "12"):
                n = 365
                expiry_date = dtObj + relativedelta(days=n)
                print(expiry_date.date())
            elif(plan == ""):
                flash('Please select Plan')
        else:
            flash('Please select Plan')

        cur.execute(
            "INSERT INTO members (member_id, member_name, mobile_number,joining_date,s_date,plan,expiry) VALUES (%s,%s,%s,%s,%s,%s,%s)", (member_id, member_name, mobile_number,j_date,s_date,plan,expiry_date))
        conn.commit()
        flash('Member Added successfully')
        return redirect(url_for('member'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_member(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('SELECT * FROM members WHERE id = {0}'.format(id))
    data = cur.fetchall()
    print(data)
    print(data[0])
    cur.close()
    return render_template('edit.html', member=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_member(id):
    if request.method == 'POST':
        member_id = request.form['member_id']
        member_name = request.form['member_name']
        mobile_number = request.form['mobile_number']
        j_date = request.form['j_date']
        s_date = request.form['s_date']
        plan = request.form['plan']
        date_format = '%Y-%m-%d'
        dtObj = datetime.strptime(s_date, date_format)
        #Expiry date calculations
        if(plan):
            if(plan == "1"):
                n = 30
                expiry_date = dtObj + relativedelta(days=n)
                print(expiry_date.date())
            elif(plan == "3"):
                n = 90
                expiry_date = dtObj + relativedelta(days=n)
                print(expiry_date.date())
            elif(plan == "6"):
                n = 180
                expiry_date = dtObj + relativedelta(days=n)
                print(expiry_date.date())
            elif(plan == "12"):
                n = 365
                expiry_date = dtObj + relativedelta(days=n)
                print(expiry_date.date())
            elif(plan == ""):
                flash('Please select Plan')
        else:
            flash('Please select Plan')

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE members
            SET member_id = %s,
                member_name = %s,
                mobile_number = %s,
                joining_date = %s,
                s_date = %s,
                plan = %s,
                expiry = %s
            WHERE id = %s
        """, (member_id, member_name, mobile_number,j_date,s_date,plan,expiry_date,id))
        flash('Member Updated Successfully')
        conn.commit()
        return redirect(url_for('member'))


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_member(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('DELETE FROM members WHERE id = {0}'.format(id))
    conn.commit()
    flash('Member Removed Successfully')
    return redirect(url_for('member'))


if __name__ == "__main__":
    app.run(debug=True)

# </string: id > </id > </id >

# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2  # pip install psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"

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


@app.route('/add_members', methods=['POST'])
def add_members():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        member_id = request.form['member_id']
        member_name = request.form['member_name']
        mobile_number = request.form['mobile_number']
        cur.execute(
            "INSERT INTO members (member_id, member_name, mobile_number) VALUES (%s,%s,%s)", (member_id, member_name, mobile_number))
        conn.commit()
        flash('Member Added successfully')
        return redirect(url_for('Index'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('SELECT * FROM members WHERE id = {0}'.format(id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', member=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_member(id):
    if request.method == 'POST':
        member_id = request.form['member_id']
        member_name = request.form['member_name']
        mobile_number = request.form['mobile_number']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE members
            SET member_id = %s,
                member_name = %s,
                mobile_number = %s
            WHERE id = %s
        """, (member_id, member_name, mobile_number, id))
        flash('Member Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_member(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('DELETE FROM members WHERE id = {0}'.format(id))
    conn.commit()
    flash('Member Removed Successfully')
    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)

# </string: id > </id > </id >

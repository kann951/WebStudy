from flask import Flask, render_template, request
import pymysql

db = pymysql.connect(
    user='root',
    passwd='fjk@$f3ifkjo',
    host='127.0.0.1',
    db='test',
    charset='utf8'
)
cursor = db.cursor(pymysql.cursors.DictCursor)

app = Flask(__name__)
logon_id = None


@app.route('/')
def home():

    return render_template('login.html', nickname=logon_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global logon_id
    if request.method == 'GET':
        logon_id = id
        return render_template('login.html', nickname=id)

    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']
        cursor.execute(f'SELECT * FROM user_list WHERE id = "{id}";')
        table = cursor.fetchone()
        if table is None:
            return render_template('login.html', message='does not exist.')

        print(table)
        if table['password'] == int(pw):

            logon_id = id
            return render_template('login.html', nickname=id)
        return render_template('login.html', message='password is wrong.', nickname=logon_id)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']

        cursor.execute(f'SELECT * FROM user_list WHERE id = "{id}"')
        result = cursor.fetchone()
        if result is not None:
            return render_template('signup.html', message='already exist.')

        cursor.execute(f'INSERT IGNORE INTO user_list (id, password) VALUES ("{id}", {pw})')
        db.commit()

        return render_template('login.html', message='registration complete.', nickname=logon_id)


@app.route('/change', methods=['GET', 'PUT'])
def change():
    if request.method == 'GET':
        return render_template('change.html')
    if request.method == 'PUT':
        changed_pw = request.form['pw']
        result = "UPDATE user_list SET password = '{}' where id = '{}'".format(changed_pw, logon_id)
        cursor.execute(result)
        db.commit()
        cursor.execute(f'SELECT * FROM user_list WHERE id = "{logon_id}";')
        table = cursor.fetchone()
        print(table)
        return render_template('login.html')


@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    if request.method == 'GET':
        return render_template('delete.html')
    if request.method == 'DELETE':
        result = "DELETE FROM user_list WHERE id = '{}')".format(logon_id)
        cursor.execute(result)
        db.commit()
        return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    global logon_id
    logon_id = None
    return render_template('login.html', nickname=logon_id)


def main():
    app.run('127.0.0.1', 80)


if __name__ == '__main__':
    main()



# id조회o
# 회원가입o
# id-password 일치 여부x
# 계정중복x
from flask import Flask, render_template, flash, request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from user import *

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register_user():
    if request.method == 'GET':
        flash("Please register")
        return render_template('register.html')

    username = request.form['username']
    password = request.form['password']
    try:
        User(username, generate_password_hash(password)).save_to_db()
    except:
        return jsonify({'error': 'An error occurred saving the user to the database'}), 500
        flash("An error occurred saving the user to the database")

    return render_template('index.html')


@app.route('/login', methods=['GET','POST'])
def login_user():
    try :
        if request.method == 'GET':
            return render_template('index.html')

        username = request.form['username']
        password = request.form['password']

        user = User.find_by_username(username)
        if user and check_password_hash(user.password, password):
            flash ("Logged in")
            return render_template('dashboard.html')        
        else :
            flash("User not found, please register")
            return render_template('register.html')
    except:
        return jsonify({'error': 'An error occurred'}), 500
        flash("An error occurred")


@app.route('/logout', methods=['POST'])
def logout_user():

    flash("LOGGED OUT")
    #we can render index page
    #return render_template('index.html')
    return jsonify({'message': 'Successfully logged out'}), 200

if __name__ == '__main__':
    app.run(debug=True)

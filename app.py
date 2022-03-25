from flask import Flask, render_template, url_for, request, session, redirect, flash, url_for, send_from_directory
from flask_pymongo import PyMongo
import os 

app = Flask(__name__)   
app.config['SECRET_KEY'] = 'testing'

app.config['MONGO_dbname'] = 'users'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/users'


mongo = PyMongo(app)



@app.route("/")
@app.route("/main")
def main():
    return render_template('index.html')

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        user = users.find_one({'username': request.form['username']})

        message = ''
        error = False

        if user:
            error = True
            message = 'User is already existed'
        else:
            users.insert_one({
                'username': request.form['username'],
                'password': request.form['password']
            })
            error = False
            message = 'Sign up successfully'

        return render_template("signup.html", message=message, error=error)

    return render_template('signup.html')

@app.route("/auth", methods=['POST', 'GET'])
def auth():
    if request.method == 'POST':
        users = mongo.db.users
        user = users.find_one({'username': request.form['username']})

        message = ''
        error = False

        if user:
            if user['password'] != request.form['password']:
                message = 'Password is not correct'
                error = True
            else:
                message = 'Login successfully'
                error = False
                return url_for(render_template('profile.html'))
        else:
            message = 'User not found'
            error = True
        
        return render_template("profile.html", message=message, error=error)

    return render_template('auth.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
    app.run()
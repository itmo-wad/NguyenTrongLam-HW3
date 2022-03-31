from flask import Flask, redirect, render_template, request, url_for
from flask_pymongo import PyMongo


app = Flask(__name__)   
app.config['SECRET_KEY'] = 'testing'

app.config['MONGO_dbname'] = 'demo'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/demo'

mongo = PyMongo(app)

cache = {}

@app.route("/")
@app.route("/main")
def main():
    if cache.get('user'):
        return render_template('index.html', error=cache.get('need_to_login'), username=cache.get('user').get('username'))
    return render_template('index.html', error=cache.get('need_to_login'))


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
                cache['user'] = user
                cache['need_to_login'] = False
                error = False
                return redirect('post')
        else:
            message = 'User not found'
            error = True
        
        return render_template("auth.html", message=message, error=error)

    return render_template('auth.html')


@app.route("/logout", methods=['POST'])
def logout():
    cache['user'] = None
    return redirect(url_for('index'))


@app.route('/create-post', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        if cache.get('user'):
            cache['title'] = request.form.get('title', '')
            cache['content'] = request.form.get('content', '')
            return redirect('post')

        cache['need_to_login'] = True
        return redirect(url_for('main'))
    return render_template("create-post.html")


@app.route("/profile")
def profile():
    return render_template("/profile.html")


@app.route("/post", methods=['GET'])
def blog():
    if not cache.get('user'):
        cache['need_to_login'] = True
    elif cache.get('title') and cache.get('content'):
        return render_template("/post.html", title=cache['title'], content=cache['content'])
    else:
        return redirect(url_for("create_post"))
    return redirect(url_for('main'))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
    app.run()
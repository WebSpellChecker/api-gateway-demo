from flask import Flask, request, render_template, redirect, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--customerid", help="Your cloud customerid.")
parser.add_argument("--local", action='store_true', help="Configure gateway to a local WebSpellChecker instance.")
parser.add_argument("--protocol", help="WebSpellChecker protocol (http/https). Default: http.", default='http')
parser.add_argument("--host", help="WebSpellChecker host. Default: localhost", default='localhost')
parser.add_argument("--port", help="WebSpellChecker port. Default: 80", default=80, type=int)
parser.add_argument("--virtual_dir", help="WebSpellChecker virtual directory. Default: wscservice.", default='wscservice')
args = parser.parse_args()

flask_host = '127.0.0.1'
flask_port = 5000

app = Flask(__name__)
app.config.update(
    SECRET_KEY="your_secret_key",
)
if args.local:
    from api_gateway_onprem import create_service_path_blueprint

    app.register_blueprint(create_service_path_blueprint(args.protocol, args.host, args.port, args.virtual_dir))
else:
    from api_gateway_cloud import create_service_path_blueprint

    app.register_blueprint(create_service_path_blueprint(args.customerid))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = {'username': 'password'}


class User(UserMixin):
    ...


@login_manager.user_loader
def user_loader(username: str):
    if username in users:
        user_model = User()
        user_model.id = username
        return user_model
    return None


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and password == users[username]:
            user_model = User()
            user_model.id = username
            login_user(user_model)
        else:
            return "Wrong credentials"

        return redirect(url_for('home'))

    return render_template('login.html', error=None)


@app.route('/logout')
@login_required
def logout():
    # Log out the current user
    logout_user()
    return redirect(url_for('home'))


@login_manager.unauthorized_handler
def unauthorized():
    return "Unauthorized", 401


def render_index_template(user=None):
    return render_template('index.html', local=args.local, host=flask_host, port=flask_port, user=user)


@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_index_template(current_user.id)
    else:
        return render_index_template(None)


if __name__ == '__main__':
    if args.local:
        print("Running demo for on-premise version.")
    else:
        print("Running demo for cloud version.")

    app.run(host=flask_host, port=flask_port, debug=True)

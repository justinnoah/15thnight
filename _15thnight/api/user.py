from flask import Blueprint, request
from flask.ext.login import login_user

from _15thnight.forms import LoginForm
from _15thnight.util import jsonify

user_api = Blueprint('user_api', __name__)

@user_api.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.get_by_email(request.form['email'].lower())
        password = request.form.get('password')
        if user is not None and user.check_password(password):
            # TODO: issue API key here instead of cookie
            session['logged_in'] = True
            login_user(user)
            return '', 200
        return jsonify(error='Invalid username/password.', _status_code=401)
    return jsonify(error='Invalid form data', _status_code=400)

@user_api.route('/logout', methods=['POST'])
def logout():
    # TODO: de-auth API key
    session.clear()
    return '', 200


@user_api.route('/reset_password', methods=['GET'])
def reset_password():
    # TODO
    pass
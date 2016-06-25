from flask import Blueprint
from flask.ext.login import (
    login_user, current_user, login_required, LoginManager 
)

from _15thnight.forms import AlertForm
from _15thnight.models import Alert, User
from _15thnight.util import required_access, jsonify

try:
    from config import HOST_NAME
except:
    from configdist import HOST_NAME


alert_api = Blueprint('alert_api', __name__)

@alert_api.route('/alert', methods=['GET'])
@required_access('advocate')
def get_alerts():
    """
    Gets list of an advocate's Alerts.
    """
    # TODO: pagination
    return jsonify(Alert.get_user_alerts(current_user))

@alert_api.route('/alert', methods=['POST'])
@required_access('advocate')
def create_alert():
    """
    Create an alert. Must be an advocate.
    """
    form = AlertForm()
    if form.validate_on_submit():
        send_out_alert(form)
    return jsonify(error='Invalid form.', _status_code=400)

@alert_api.route('/alert/<int:id>', methods=['PUT'])
#@required_access('advocate')
def update_alert(id):
    return 'Not Implemented', 501

@alert_api.route('/alert/<int:id>', methods=['DELETE'])
#@required_access('advocate')
def delete_alert(id):
    alert = Alert.get_user_alert(current_user, id)
    if alert:
        alert.delete()
        return ''
    return jsonify(error='No alert was found.', _status_code=404)

from flask import Blueprint, request
from flask.ext.login import (
    login_user, current_user, login_required, LoginManager
)

from _15thnight.core import respond_to_alert
from _15thnight.util import required_access


response_api = Blueprint('response_api', __name__)


@response_api.route('/response', methods=['GET'])
@required_access('provider')
def get_responses():
    """
    Gets a list of a provider's responses
    """
    return jsonify(Response.get_by_user(current_user))


@response_api.route('/response', methods=['POST'])
@required_access('provider')
def create_response():
    """
    Creates a response to an alert.

    POST params:
        - alert_id: alert identifier
        - message: response message
    """
    if 'alert_id' not in request.form or 'message' not in request.form:
        return jsonify(error='Invalid form', _status_code=400)

    alert = Alert.get(int(request.form['alert_id']))

    if not alert:
        return jsonify(error='Alert not found.', _status_code=404)

    respond_to_alert(current_user, request.form['message'], alert)

    return '', 200


@response_api.route('/response/:uuid', methods=['DELETE'])
@required_access('provider')
def delete_response():
    """
    Delete a response to an alert.
    """
    return 'Not Implemented', 501


@response_api.route('/response/:uuid', methods=['PUT'])
@required_access('provider')
def update_response():
    """
    Update a response to an alert.
    """
    return 'Not Implemented', 501

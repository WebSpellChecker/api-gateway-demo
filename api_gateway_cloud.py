from flask import Blueprint, request, Response
from flask_login import current_user
import requests
from urllib.parse import unquote


def create_service_path_blueprint(serviceid):
    service_path_blueprint = Blueprint('check', __name__)

    @service_path_blueprint.route('/check', methods=["POST"])
    def check():
        # Check if user is authorized
        if not current_user.is_authenticated:
            # If user is not authorized, return 401
            return Response("Unauthorized", status=401)

        headers = {'Referer': request.headers['Referer']}

        # Add serviceid to request data
        data = parse_form_data(request.data.decode())
        data['serviceid'] = serviceid
        # Send request to wsc cloud
        proxied_response = requests.post("https://svc.webspellchecker.net/api", data=data, headers=headers)

        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        response_headers = {
            k: v for k, v in proxied_response.raw.headers.items()
            if k.lower() not in excluded_headers
        }

        # Return wsc cloud's response
        return Response(proxied_response.text, status=proxied_response.status_code, headers=response_headers)

    def parse_form_data(raw_data):
        raw_data = unquote(raw_data)
        data = {}
        for pair in raw_data.split('&'):
            key, value = pair.split('=')
            data[key] = value

        return data

    return service_path_blueprint

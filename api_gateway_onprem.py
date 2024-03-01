from flask import Blueprint, request, Response
from flask_login import current_user, login_required
import requests


def create_service_path_blueprint(protocol, host, port, virtual_dir):
    service_path_blueprint = Blueprint('check', __name__)

    @service_path_blueprint.route('/check', methods=["POST"])
    def check():
        # Check if user is authorized
        if not current_user.is_authenticated:
            # If user is not authorized, return 401
            return Response("Unauthorized", status=401)

        headers = {'Referer': request.headers['Referer']}

        # Get data from request
        data = request.data.decode()
        # Send request to local appserver
        proxied_response = requests.post(protocol + "://" + host + ":" + str(port) + "/" + virtual_dir + "/api", data=data, headers=headers)

        # Filter response headers
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        response_headers = {
            k: v for k, v in proxied_response.raw.headers.items()
            if k.lower() not in excluded_headers
        }

        # Return wsc response
        return Response(proxied_response.text, status=proxied_response.status_code, headers=response_headers)

    @service_path_blueprint.route("/wscbundle/<path:path>", methods=["GET"])
    @login_required
    def wscbundle(path):
        # Save Referer header
        headers = {'Referer': request.headers['Referer']}
        # Make proxy request to a local appserver with specified path
        print(protocol + "://" + host + ":" + str(port) + "/" + virtual_dir + "/wscbundle/" + path)
        proxied_response = requests.get(protocol + "://" + host + ":" + str(port) + "/" + virtual_dir + "/wscbundle/" + path, headers=headers)

        # Filter response headers
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        response_headers = {
            k: v for k, v in proxied_response.raw.headers.items()
            if k.lower() not in excluded_headers
        }

        # Return wsc response
        return Response(proxied_response.content, status=proxied_response.status_code, headers=response_headers)

    return service_path_blueprint

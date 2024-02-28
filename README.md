# WebSpellChecker API Gateway demo

This repository contains an example of the API Gateway example built with Python Flask.
The API Gateway serves as a secured entry point for WebSpellChecker service and implements
session-based authorization for secure access.

Using this example you are able to implement API Gateway for WebSpellChecker (both cloud and on-premise versions) service on your side.

## Getting started

Follow the steps below to set up and run the API Gateway:

### Prerequisites

- Python 3.x
- Required dependencies (install using `pip install -r requirements.txt`)
- WebSpellChecker subscription (cloud subscription or on-premise version configured)

### Running demo for WebSpellChecker cloud version

To run demo for WebSpellChecker cloud version launch the application specifying your customer id:

```
python main.py --customerid <your_customer_id>
```

After launching the application should be running and available under http://127.0.0.1:5000/

### Running demo for WebSpellChecker on-premise version

To run demo for WebSpellChecker on-premise version launch the application specifying path to your WebSpellChecker service endpoint:

```
python main.py --local --protocol <http/https> --host <webspellchecker_host> --port <webspellchecker_port> --virtual_dir <webspellchecker_virtual_dir>
```

To list all available parameters use:

```
python main.py --help
```

**Note!** Make sure, that API Gateway is able to reach provided WebSpellChecker service endpoint.

After launching the application should be running and available under http://127.0.0.1:5000/

## Configure your own API Gateway

While this repository provides a simple demonstration of an API Gateway with session-based authorization,
it is essential to implement a robust and customized solution for production environments.
Below are steps to guide you in configuring your own API Gateway tailored to your specific requirements:

### Cloud version

To implement API Gateway for cloud version of WebSpellChecker using your existing authorization you need to create a
separate handler with a specific path, such as `/check`.
This handler can serve as the entry point for API Gateway-related requests in your production environment.
New handler should have next logic:

1. Check if request is authorized
2. Save `Referer` header and put it to a proxy request
3. Parse request body and add `customerid` parameter with your customerid
4. Send request to WebSpellChecker cloud endpoint: https://svc.webspellchecker.net/api
5. Return cloud's response

Then, configure `WEBSPELLCHECKER_CONFIG` with host, port and path to your API Gateway.

The example of such handler could be found in `api_gateway_cloud` file.

### On-premise version

As in cloud version, you need to create separate handler with specific path, like `/check` with next logic:

1. Check if request is authorized
2. Save `Referer` header and put it to a proxy request
3. Copy whole request body to a proxy request
4. Send request to your WebSpellChecker endpoint
5. Return the response

Also, handler for static files is needed. So define `/wscbundle/<path>` path handler with next logic:

1. Check if request is authorized
2. Send proxy request to your WebSpellChecker endpoint with provided `path` in the request.
3. Return the response

Then, configure `WEBSPELLCHECKER_CONFIG` with host, port and path to your API Gateway.

The example of such handler could be found in `api_gateway_onprem` file.

## Important notes

- To implement such approach to protect your Cloud subscription or on-premise endpoint you need to have
user authorization configured on your server side. This example implements Session-Based authorization
using Flask-Login module for demonstration purposes and should not be used in a production.
- When sending a proxy request `Referer` header and the whole request body from the original request should be preserved.
from logging.config import dictConfig
import sys
import logging
from typing import Any

from flask import Flask, jsonify, request

from .provider_data_loader import ProviderDataLoader

# Logging setup
# Reference: https://flask.palletsprojects.com/en/2.2.x/logging/
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

data_loader: ProviderDataLoader = ProviderDataLoader()

# Events & Setup
@app.before_first_request
def before_first_request_func():
    data_loader.load_data_into_memory()

# Setup routes
@app.route("/providers", methods=['GET'])
def providers():
    filters: dict[str, Any] = {}
    ordering: dict[str, Any] = {}

    QUERY_STRING_FILTER_PREFIX: str = 'filter_'
    QUERY_STRING_ORDER_PREFIX: str = 'order_'

    for arg in request.args:
        if arg.startswith(QUERY_STRING_FILTER_PREFIX):
            filter_key: str = arg.replace(QUERY_STRING_FILTER_PREFIX, '')
            filters[filter_key] = request.args[arg]

        elif arg.startswith(QUERY_STRING_ORDER_PREFIX):
            order_key: str = arg.replace(QUERY_STRING_ORDER_PREFIX, '')
            ordering[order_key] = int(request.args[arg])
    print('hey')
    print(filters)
    providers: list[Any] = data_loader.get_providers_with_options(
        filters=filters, ordering=ordering
    )

    result = {
        "count": len(providers),
        "list": providers
    }

    return jsonify(result)


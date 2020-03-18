from flask_restplus import Api, reqparse, inputs
from werkzeug.exceptions import HTTPException
import json
import datetime
import sentry_sdk
import math

api = Api(version='0.0.1', default='stock_api', title='STOCK API',
          description=' Stock Alert')


parser_auth = reqparse.RequestParser()
parser_auth.add_argument('Authorization', location='headers', required=True)

parser_paginate_auth = parser_auth.copy()
parser_paginate_auth.add_argument('page', type=int, location='args')
parser_paginate_auth.add_argument('page_size', type=int, location='args')

parser_event = parser_paginate_auth.copy()
parser_event.add_argument('month', type=str, location='args')
parser_event.add_argument('event_type', type=str, location='args')


@api.errorhandler
def default_error_handler(e):
    if isinstance(e, HTTPException):
        print(e.get_response())
        response = {'message': e.description}
        status_code = e.code
    else:
        sentry_sdk.capture_exception(e)
        response = {'message': 'Unhandled Exception'}
        status_code = 500

    return response, status_code


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


@api.representation('application/json')
def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    data_s = json.dumps(data, cls=DateTimeEncoder)
    data_d = json.loads(data_s)
    resp = Api().make_response(data_d, code, fallback_mediatype='application/json')
    resp.headers.extend(headers or {})
    return resp


def paginate(query, page, page_size):
    total_records = query.count()
    skip = (page - 1) * page_size
    total_pages = math.ceil(total_records / page_size)
    query = query.offset(skip).limit(page_size)
    return query, total_pages

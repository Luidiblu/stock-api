from stock_api.api import api, parser_auth, parser_suggestion, parser_wallet_name
from flask_restplus import Resource, reqparse
from werkzeug.exceptions import Forbidden
from stock_api.api.auth import AuthHelper
from stock_api.database.orm import *
from flask import request, Response
from stock_api.api.wallet.suggestion import stock_suggestions
from stock_api.api.wallet.wallet import create_wallet


ns_stock = api.namespace('stock', description='Operations related to stocks')
ns_wallet = api.namespace('wallet', description='Operations related to wallets')


@ns_stock.route('/<string:user_id>/suggestion')
class SuggestStock(Resource):
    @ns_stock.expect(parser_auth, parser_suggestion, validate=True)
    def get(self, user_id):
        args = parser_auth.parse_args(request)
        token = AuthHelper.read_token(args)
        suggestion = parser_suggestion.parse_args(request)

        clearance = f'api::stock::client::{user_id}::read'
        if not AuthHelper.user_is_cleared(token, clearance):
            raise Forbidden('User is not Authorized')

        return stock_suggestions(suggestion)


@ns_wallet.route('/<string:user_id>/wallet_name')
class CreateWallet(Resource):
    @ns_stock.expect(parser_auth, parser_wallet_name, validate=True)
    def get(self, user_id):
        args = parser_auth.parse_args(request)
        token = AuthHelper.read_token(args)
        wallet_name = parser_wallet_name.parse_args(request)

        clearance = f'api::stock::client::{user_id}::read'
        if not AuthHelper.user_is_cleared(token, clearance):
            raise Forbidden('User is not Authorized')

        return create_wallet(user_id, wallet_name)

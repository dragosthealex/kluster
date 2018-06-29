import json

from flask import Flask, request
from licenta.dao import DAO

from licenta.constants import TRACKER_PORT, TRACKER_HOST
from licenta.utils import _json_success

APP = Flask(__name__)
_DAO = DAO()


@APP.route('/providers', methods=['GET'])
def get_providers():
    # Called by client
    service_name = request.args.get('service_name')
    max_price = request.args.get('max_price')
    providers = _DAO.get_providers(service_name=service_name,
                                   max_price=max_price)
    return _json_success({
        provider.address: {
            'ip': provider.ip_address,
            'port': provider.port,
            'price': [service_assoc.price for service_assoc in provider.services
                      if service_assoc.service.name == service_name].pop(),
            'rating': provider.rating
        }
        for provider in providers})


@APP.route('/update-status', methods=['GET'])
def update_provider_status():
    # Called by provider
    address = request.args.get('address')
    is_online = request.args.get('status') == 'online'
    _DAO.update_status(address, is_online)
    return _json_success('Updated.')


@APP.route('/rating', methods=['GET'])
def update_peer_rating():
    address = request.args.get('address')
    rating = request.args.get('rating')
    rating = int(rating) if rating else 0
    _DAO.update_rating(address, rating)
    return _json_success('Updated.')


@APP.route('/register-peer', methods=['GET'])
def register_peer():
    _DAO.register_peer(address=request.args.get('address'),
                       ip_address=request.args.get('ip_address'),
                       port=int(request.args.get('port')),
                       services=json.loads(request.args.get('services')))


def rate_peer(address, rating):
    # Called by whatever
    pass


def main():
    APP.run(debug=True, host=TRACKER_HOST, port=TRACKER_PORT)


if __name__ == '__main__':
    main()

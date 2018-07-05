import json

import requests
from flask import Flask, request
from licenta.constants import PROVIDER_PORT, PROVIDER_HOST, PROVIDER_ADDRESS, \
    TRACKER_HOST, TRACKER_PORT

from licenta.utils import _json_success

APP = Flask('Provider')


@APP.route('/request', methods=['GET'])
def take_request():
    peer_address = request.args.get('address')
    service_name = request.args.get('service_name')

    print('Got a request from {} for {} service.'.format(
            peer_address, service_name
    ))

    # Check peers rating
    request_obj = requests.get('http://{}:{}/get-rating'
                               .format(TRACKER_HOST, TRACKER_PORT),
                               params={'address': peer_address})
    request_obj.raise_for_status()
    peer_rating = json.loads(request_obj.content)
    print('Rating for {} is {}. If it is lower than 2.5 not going to provide.'
          .format(peer_address, peer_rating))

    return _json_success('YES') if peer_rating > 2.5 else _json_success('NOPE')


@APP.route('/contribution', methods=['GET'])
def take_contribution():
    peer_address = request.args.get('address')
    amount = int(request.args.get('contribution'))
    service_name = request.args.get('service_name')

    print('Got {} contribution from {} for {} service.'.format(
            amount, peer_address, service_name
    ))
    # save latent contrib
    # w3py
    return _json_success('THANK')


def main():
    print('Running provider {}'.format(PROVIDER_ADDRESS))
    APP.run(debug=True, host=PROVIDER_HOST, port=PROVIDER_PORT)


if __name__ == '__main__':
    main()

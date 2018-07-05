from flask import Flask, request
from licenta.constants import PROVIDER_PORT, PROVIDER_HOST, PROVIDER_ADDRESS

from licenta.utils import _json_success

APP = Flask('Provider')


@APP.route('/request', methods=['GET'])
def take_request():
    peer_address = request.args.get('address')
    service_name = request.args.get('service_name')

    print('Got a request from {} for {} service.'.format(
            peer_address, service_name
    ))
    # check rating when get request
    return _json_success('YES')


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

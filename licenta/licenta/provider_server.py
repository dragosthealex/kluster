import csv
import datetime
import json

import requests
from flask import Flask, request
from licenta.constants import PROVIDER_PORT, PROVIDER_HOST, PROVIDER_ADDRESS, \
    TRACKER_HOST, TRACKER_PORT, PROVIDER_LATENT_CSV_PATH, CONTRACT_ADDRESS, \
    CONTRACT_ABI

from licenta.utils import _json_success
from web3 import Web3, TestRPCProvider, HTTPProvider
from web3.contract import ConciseContract

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

    # Save to file
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    with open(PROVIDER_LATENT_CSV_PATH, 'rw') as latent_csv:
        data = csv.reader(latent_csv, delimiter=',', quotechar='|')
        data.append([now, peer_address, amount, service_name])
        csv.writer(latent_csv, delimiter=',',
                   quotechar='|', quoting=csv.QUOTE_MINIMAL)

    # Try to send contrib
    try:
        _upload_latent()
    except:
        pass

    return _json_success('THANK')


def _upload_latent():
    w3 = Web3(HTTPProvider('https://ropsten.infura.io/'))
    w3.eth.enable_unaudited_features()
    contract_address = CONTRACT_ADDRESS
    abi = CONTRACT_ABI
    contract_instance = w3.eth.contract(address=contract_address, abi=abi,
                                        ContractFactoryClass=ConciseContract)

    with open(PROVIDER_LATENT_CSV_PATH, 'rw') as latent_csv:
        data = csv.reader(latent_csv, delimiter=',', quotechar='|')
    for row in data:
        address = row[1]
        value = row[2]
        contract_instance.registerLatent(address, value, v, r, s)


def main():
    print('Running provider {}'.format(PROVIDER_ADDRESS))
    APP.run(debug=True, host=PROVIDER_HOST, port=PROVIDER_PORT)


if __name__ == '__main__':
    main()

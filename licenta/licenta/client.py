import json
from argparse import ArgumentParser
import bitcoin as b

from licenta.constants import CLIENT_ADDRESS, PROVIDER_ADDRESS, \
    CLIENT_PRIVATE_KEY
from licenta.peer_node import PeerNode

from licenta.utils import validate_args


class Client(PeerNode):

    def list_providers(self, service_name=None, max_price=None):
        providers = self.request('/providers', args={
            'service_name': service_name,
            'max_price': max_price
        })
        for address, provider in providers.items():
            print('Token address: {}'.format(address))
            print('IP address: {}:{}'.format(provider['ip'],
                                             provider['port']))
            print('Price: {}'.format(provider['price']))
            print('------------------------------------')

    def send_contribution(self, ip, port, service_name, contribution):
        base_url = 'http://{}:{}'.format(ip, port)

        # pub = b.privtopub(CLIENT_PRIVATE_KEY)
        # pickledstring = json.dumps({pub, PROVIDER_ADDRESS,
        #                             contribution})
        # msghash = b.sha256(pickledstring)
        # v, r, s = b.ecdsa_raw_sign(msghash, CLIENT_PRIVATE_KEY)

        resp = self.request('/contribution', base_url, args={
            'service_name': service_name,
            'contribution': contribution,
            'address': self.address
        })
        print('Sent {} contribution to {} and got response: {}'.format(
                contribution, '{}:{}'.format(ip, port), resp
        ))

    def send_request(self, ip, port, service_name):
        base_url = 'http://{}:{}'.format(ip, port)
        resp = self.request('/request', base_url, args={
            'service_name': service_name,
            'address': self.address
        })
        print('Sent request to {} for service {} and got response: {}'.format(
                '{}:{}'.format(ip, port), service_name, resp
        ))


def main():
    parser = ArgumentParser(description='Client console interface.')
    parser.add_argument('action', type=str,
                        choices=['providers', 'send_contribution',
                                 'send_request'],
                        help='Either list providers or send contribution to '
                             'one. If "providers", you must specify service'
                             'and max price. If "contribution" must specify ip,'
                             ' port, service and contribution. If "request", '
                             'must specify ip, port, service_name.')
    parser.add_argument('--ip', type=str,
                        help='IP of peer to send contribution to.')
    parser.add_argument('--port', type=int, help='Port of peer to send '
                                                 'contribution to.')
    parser.add_argument('--contribution', type=int, help='Amount of '
                                                         'contribution.')
    parser.add_argument('--service', type=str, help='Name of the service you'
                                                    'want providers for.')
    parser.add_argument('--max_price', type=str, help='Max price you are '
                                                      'willing to pay.')
    args = parser.parse_args()
    client = Client(CLIENT_ADDRESS)
    if args.action == 'providers':
        if validate_args([args.service, args.max_price]):
            client.list_providers(args.service, int(args.max_price))
    elif args.action == 'send_contribution':
        if validate_args([args.ip, args.port, args.contribution, args.service]):
            client.send_contribution(args.ip, args.port, args.service,
                                     args.contribution)
    elif args.action == 'send_request':
        if validate_args([args.ip, args.port, args.service]):
            client.send_request(args.ip, args.port, args.service)


if __name__ == '__main__':
    main()

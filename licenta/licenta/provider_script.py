from argparse import ArgumentParser

from licenta.constants import PROVIDER_ADDRESS
from licenta.peer_node import PeerNode
from licenta.utils import validate_args


class Provider(PeerNode):

    def send_rating(self, address, rating):
        resp = self.request('/rating', args={
            'address': address,
            'rating': rating
        })
        print(resp)

    def send_status(self, is_online):
        resp = self.request('/update-status', args={
            'address': self.address,
            'status': 'online' if is_online else 'offline'
        })
        print(resp)


def main():
    parser = ArgumentParser(description='Provider console interface.')
    parser.add_argument('action', type=str,
                        choices=['rating', 'status_update'],
                        help='Either send a rating for a client or send status'
                             'update. If rating, need to set address of client'
                             'and rating -1, 0, 1. If status, need 0=offline or'
                             '1=online.')
    parser.add_argument('--address', type=str,
                        help='Address of peer to rate.')
    parser.add_argument('--rating', type=int, help='Rating for peer',
                        choices=[-1, 0, 1])
    parser.add_argument('--status', type=int, help='0 for offline, 1 for '
                                                   'online',
                        choices=[0, 1])
    args = parser.parse_args()
    provider = Provider(PROVIDER_ADDRESS)
    if args.action == 'rating':
        if validate_args([args.address, args.rating]):
            provider.send_rating(args.address, args.rating)
    elif args.action == 'status_update':
        if validate_args([args.status]):
            provider.send_status(args.status)


if __name__ == '__main__':
    main()

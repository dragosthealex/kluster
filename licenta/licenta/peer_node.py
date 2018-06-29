import json

import requests

from licenta.constants import TRACKER_PORT, TRACKER_HOST


class PeerNode:

    def __init__(self, address, tracker_host=TRACKER_HOST,
                 tracker_port=TRACKER_PORT):
        self.base_url = 'http://{}:{}'.format(tracker_host, tracker_port)
        self.address = address

    def request(self, route, base_url=None, args=None):
        args = args or {}
        base_url = base_url or self.base_url
        request = requests.get(base_url + route, params=args)
        request.raise_for_status()

        content = json.loads(request.content)
        if content['status'] == 'ERROR':
            print('ERROR requesting {}: {}'.format(route, content['message']))
        return content['message']

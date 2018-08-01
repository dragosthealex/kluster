import argparse
import random
import string

from licenta.constants import PROVIDER_ADDRESS, PROVIDER_HOST, PROVIDER_PORT, \
    Services, SERVICE_NAMES
from licenta.dao import DAO

if __name__ == '__main__':
    services = {SERVICE_NAMES[Services.MINECRAFT]: 10,
                SERVICE_NAMES[Services.ROCKET_LEAGUE]: 20}
    parser = argparse.ArgumentParser()
    parser.add_argument('--number', help='Number of peers to register',
                        type=int, default=10000)
    args = parser.parse_args()
    dao = DAO()
    for n in range(args.number):
        print(n)
        address = ''.join(random.choice(string.ascii_uppercase
                                        + string.digits) for _ in range(10))
        dao.register_peer(address=address, ip_address=PROVIDER_HOST,
                          port=PROVIDER_PORT, services=services)
        print('Added peer {} to db'.format(address))

from enum import Enum

TRACKER_PORT = 5001
TRACKER_HOST = 'localhost'

PROVIDER_PORT = 5003
PROVIDER_HOST = 'localhost'


CLIENT_ADDRESS = 'qwer'
PROVIDER_ADDRESS = 'asdf'


class Services(Enum):
    MINECRAFT = 0
    ROCKET_LEAGUE = 1


SERVICE_NAMES = {
    Services.MINECRAFT: 'minecraft',
    Services.ROCKET_LEAGUE: 'rocket_league'
}

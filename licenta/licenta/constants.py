from enum import Enum

TRACKER_PORT = 5001
TRACKER_HOST = 'localhost'


CLIENT_ADDRESS = 'qwer'
CLIENT_PUBLIC_KEY = '0xd949aaC3f8217dd69977f746a7Cc6D1d33bAF4c1'
CLIENT_PRIVATE_KEY = '0x46AbaF771ef7Dc0E10FDDb1A417fBE2b91B08Af3'


PROVIDER_PORT = 5003
PROVIDER_HOST = 'localhost'
PROVIDER_ADDRESS = 'asdf'
PROVIDER_LATENT_CSV_PATH = 'provider_latent_contrib.csv'

CONTRACT_ADDRESS = 'contract eth address here'
CONTRACT_ABI = 'binary here'


class Services(Enum):
    MINECRAFT = 0
    ROCKET_LEAGUE = 1


SERVICE_NAMES = {
    Services.MINECRAFT: 'minecraft',
    Services.ROCKET_LEAGUE: 'rocket_league'
}

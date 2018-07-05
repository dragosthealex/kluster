"""Data Access Object.

Provides methods to access the data in db
"""
from contextlib import contextmanager

from licenta.constants import SERVICE_NAMES, \
    Services, PROVIDER_HOST, PROVIDER_PORT, PROVIDER_ADDRESS, CLIENT_ADDRESS

from licenta.sql_models import SessionFactory, Peer, PeerServiceAssociation, \
    Service


class DAO:

    def __init__(self):
        self.session_maker = SessionFactory

    @contextmanager
    def session_getter(self):
        session = self.session_maker()
        try:
            yield session
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()

    def get_providers(self, service_name=None, max_price=None):
        with self.session_getter() as session:
            print(session.query)
            query = session.query(Peer).filter(Peer.is_online == 1)
            if service_name:
                query = query.filter(Peer.services.any(
                        PeerServiceAssociation.service.has(name=service_name)
                ))
            if max_price:
                query = query.filter(Peer.services.any(
                        PeerServiceAssociation.price <= max_price
                ))
            providers = query.order_by(Peer.rating.desc()).all()
            session.expunge_all()
        return providers

    def register_peer(self, address, ip_address, port, services):
        with self.session_getter() as session:
            peer = Peer(address=address,
                        ip_address=ip_address,
                        port=port,
                        rating=0)
            # Add services as provider
            for service_name, price in services.items():
                # Make sure service in db
                service = (session.query(Service)
                           .filter(Service.name == service_name)
                           .first())
                # If not, add it
                if not service:
                    service = Service(name=service_name)
                    session.add(service)

                service_assoc = PeerServiceAssociation(price=price,
                                                       service=service)
                peer.services.append(service_assoc)
            session.add(peer)

    def update_status(self, address, is_online):
        print('Updating is_online for {}: {}'.format(address, is_online))
        with self.session_getter() as session:
            provider = (session.query(Peer).filter(Peer.address == address)
                        .first())
            if not provider:
                raise ValueError('Invalid address.')
            provider.is_online = is_online

    def update_rating(self, address, rating):
        print('Updating rating for {}: {}'.format(address, rating))
        with self.session_getter() as session:
            provider = (session.query(Peer).filter(Peer.address == address)
                        .first())
            if not provider:
                raise ValueError('Invalid address.')

            provider.rating_count += 1
            if provider.rating_count == 1:
                provider.rating = rating
            else:
                provider.rating += ((rating - provider.rating)
                                    / provider.rating_count)

    def get_rating(self, address):
        print('Getting rating for {}'.format(address))
        with self.session_getter() as session:
            peer = (session.query(Peer).filter(Peer.address == address)
                      .first())
            if not peer:
                raise ValueError('Invalid address.')
            return peer.rating


if __name__ == '__main__':
    dao = DAO()
    services = {SERVICE_NAMES[Services.MINECRAFT]: 10,
                SERVICE_NAMES[Services.ROCKET_LEAGUE]: 20}
    dao.register_peer(address=PROVIDER_ADDRESS, ip_address=PROVIDER_HOST,
                      port=PROVIDER_PORT, services=services)
    dao.register_peer(address=CLIENT_ADDRESS, ip_address='localhost',
                      port='0.0.0.0', services={})
    providers = dao.get_providers(
            service_name=SERVICE_NAMES[Services.MINECRAFT],
            max_price=100
    )
    print(providers)

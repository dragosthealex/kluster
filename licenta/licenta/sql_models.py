from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, \
    Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

_KlusterBase = declarative_base()


class PeerServiceAssociation(_KlusterBase):
    __tablename__ = 'peer_service'

    service_id = Column(Integer, ForeignKey('service.id'), primary_key=True)
    peer_id = Column(Integer, ForeignKey('peer.id'), primary_key=True)
    price = Column(Integer, nullable=True, default=0)

    peer = relationship('Peer', back_populates='services', lazy='subquery')
    service = relationship('Service', back_populates='providers',
                           lazy='subquery')


class Peer(_KlusterBase):
    __tablename__ = 'peer'

    id = Column(Integer, primary_key=True)
    address = Column(String(255))
    ip_address = Column(String(15))
    port = Column(Integer)
    rating = Column(Integer, nullable=True, default=0)
    is_online = Column(Boolean, default=False)

    services = relationship('PeerServiceAssociation', back_populates='peer',
                            lazy='subquery')


class Service(_KlusterBase):
    __tablename__ = 'service'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    providers = relationship('PeerServiceAssociation', back_populates='service'
                             , lazy='subquery')


_ENGINE = create_engine('sqlite:///kluster.db')
_KlusterBase.metadata.create_all(_ENGINE)
SessionFactory = sessionmaker(bind=_ENGINE)

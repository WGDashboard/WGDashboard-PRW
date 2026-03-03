#!/bin/env python3

import sqlalchemy
import sqlalchemy.orm

Base = sqlalchemy.orm.declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)

    username = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    password = sqlalchemy.Column(sqlalchemy.String)

    role = sqlalchemy.Column(sqlalchemy.String, default='user')

    totp_enabled = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    totp_verified = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    totp_key = sqlalchemy.Column(sqlalchemy.String)

    email = sqlalchemy.Column(sqlalchemy.String)

class Apikeys(Base):
    __tablename__ = 'apikeys'

    key_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    key_data = sqlalchemy.Column(sqlalchemy.String)

    key_creation = sqlalchemy.Column(sqlalchemy.String)
    key_expiration = sqlalchemy.Column(sqlalchemy.String)

    def to_dict(self):
        return {
            'id': self.key_id,
            'key': self.key_data,
            'creation': self.key_creation,
            'expiration': self.key_expiration,
        }

class Wireguard(Base):
    __tablename__ = 'wireguard_interfaces'

    iface_status = sqlalchemy.Column(sqlalchemy.String)
    iface_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)

    iface_name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    iface_notes = sqlalchemy.Column(sqlalchemy.String)

    iface_privkey = sqlalchemy.Column(sqlalchemy.String, unique=True)
    iface_pubkey = sqlalchemy.Column(sqlalchemy.String, unique=True)
    iface_address = sqlalchemy.Column(sqlalchemy.String)
    iface_listen_port = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    iface_mtu = sqlalchemy.Column(sqlalchemy.Integer)

    iface_preup = sqlalchemy.Column(sqlalchemy.String)
    iface_predown = sqlalchemy.Column(sqlalchemy.String)
    iface_postup = sqlalchemy.Column(sqlalchemy.String)
    iface_predown = sqlalchemy.Column(sqlalchemy.String)

    iface_save_config = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    iface_total_rx = sqlalchemy.Column(sqlalchemy.Float)
    iface_total_tx = sqlalchemy.Column(sqlalchemy.Float)
    iface_total_data = sqlalchemy.Column(sqlalchemy.Float)

class Amnezia(Base):
    __tablename__ = 'amnezia_interfaces'

    iface_status = sqlalchemy.Column(sqlalchemy.String)
    iface_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)

    iface_name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    iface_notes = sqlalchemy.Column(sqlalchemy.String)

    iface_privkey = sqlalchemy.Column(sqlalchemy.String, unique=True)
    iface_pubkey = sqlalchemy.Column(sqlalchemy.String, unique=True)
    iface_address = sqlalchemy.Column(sqlalchemy.String)
    iface_listen_port = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    iface_mtu = sqlalchemy.Column(sqlalchemy.Integer)

    iface_preup = sqlalchemy.Column(sqlalchemy.String)
    iface_predown = sqlalchemy.Column(sqlalchemy.String)
    iface_postup = sqlalchemy.Column(sqlalchemy.String)
    iface_predown = sqlalchemy.Column(sqlalchemy.String)

    iface_jc = sqlalchemy.Column(sqlalchemy.Integer)
    iface_jmin = sqlalchemy.Column(sqlalchemy.Integer)
    iface_jmax = sqlalchemy.Column(sqlalchemy.Integer)

    iface_s1 = sqlalchemy.Column(sqlalchemy.Integer)
    iface_s2 = sqlalchemy.Column(sqlalchemy.Integer)
    iface_s3 = sqlalchemy.Column(sqlalchemy.Integer)
    iface_s4 = sqlalchemy.Column(sqlalchemy.Integer)

    iface_h1 = sqlalchemy.Column(sqlalchemy.String)
    iface_h2 = sqlalchemy.Column(sqlalchemy.String)
    iface_h3 = sqlalchemy.Column(sqlalchemy.String)
    iface_h4 = sqlalchemy.Column(sqlalchemy.String)

    iface_i1 = sqlalchemy.Column(sqlalchemy.String)
    iface_i2 = sqlalchemy.Column(sqlalchemy.String)
    iface_i3 = sqlalchemy.Column(sqlalchemy.String)
    iface_i4 = sqlalchemy.Column(sqlalchemy.String)
    iface_i5 = sqlalchemy.Column(sqlalchemy.String)

    iface_save_config = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    iface_total_rx = sqlalchemy.Column(sqlalchemy.Float)
    iface_total_tx = sqlalchemy.Column(sqlalchemy.Float)
    iface_total_data = sqlalchemy.Column(sqlalchemy.Float)

class Peers(Base):
    __tablename__ = 'interface_peers'

    peer_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)

    assigned_iface = sqlalchemy.Column(sqlalchemy.String)
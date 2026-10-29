#!/bin/env python3

from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str | None] = mapped_column(String, unique=True, index=True)
    password: Mapped[str | None] = mapped_column(String)
    role: Mapped[str | None] = mapped_column(String, default='user')
    totp_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    totp_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    totp_secret: Mapped[str | None] = mapped_column(String)
    email: Mapped[str | None] = mapped_column(String)

class Apikeys(Base):
    __tablename__ = 'apikeys'

    key_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    key_data: Mapped[str | None] = mapped_column(String)
    key_creation: Mapped[str | None] = mapped_column(String)
    key_expiration: Mapped[str | None] = mapped_column(String)

    def to_dict(self) -> dict[str, int | str | None]:
        return {
            'id': self.key_id,
            'key': self.key_data,
            'creation': self.key_creation,
            'expiration': self.key_expiration,
        }

class Wireguard(Base):
    __tablename__ = 'wireguard_interfaces'

    iface_status: Mapped[str | None] = mapped_column(String)
    iface_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    iface_name: Mapped[str | None] = mapped_column(String, unique=True)
    iface_notes: Mapped[str | None] = mapped_column(String)
    iface_privkey: Mapped[str | None] = mapped_column(String, unique=True)
    iface_pubkey: Mapped[str | None] = mapped_column(String, unique=True)
    iface_address: Mapped[str | None] = mapped_column(String)
    iface_listen_port: Mapped[int | None] = mapped_column(Integer, unique=True)
    iface_mtu: Mapped[int | None] = mapped_column(Integer)
    iface_preup: Mapped[str | None] = mapped_column(String)
    iface_predown: Mapped[str | None] = mapped_column(String)
    iface_postup: Mapped[str | None] = mapped_column(String)
    iface_postdown: Mapped[str | None] = mapped_column(String)
    iface_save_config: Mapped[bool] = mapped_column(Boolean, default=True)
    iface_total_rx: Mapped[float | None] = mapped_column(Float)
    iface_total_tx: Mapped[float | None] = mapped_column(Float)
    iface_total_data: Mapped[float | None] = mapped_column(Float)

class Amnezia(Base):
    __tablename__ = 'amnezia_interfaces'

    iface_status: Mapped[str | None] = mapped_column(String)
    iface_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    iface_name: Mapped[str | None] = mapped_column(String, unique=True)
    iface_notes: Mapped[str | None] = mapped_column(String)
    iface_privkey: Mapped[str | None] = mapped_column(String, unique=True)
    iface_pubkey: Mapped[str | None] = mapped_column(String, unique=True)
    iface_address: Mapped[str | None] = mapped_column(String)
    iface_listen_port: Mapped[int | None] = mapped_column(Integer, unique=True)
    iface_mtu: Mapped[int | None] = mapped_column(Integer)
    iface_preup: Mapped[str | None] = mapped_column(String)
    iface_predown: Mapped[str | None] = mapped_column(String)
    iface_postup: Mapped[str | None] = mapped_column(String)
    iface_postdown: Mapped[str | None] = mapped_column(String)
    iface_jc: Mapped[int | None] = mapped_column(Integer)
    iface_jmin: Mapped[int | None] = mapped_column(Integer)
    iface_jmax: Mapped[int | None] = mapped_column(Integer)
    iface_s1: Mapped[int | None] = mapped_column(Integer)
    iface_s2: Mapped[int | None] = mapped_column(Integer)
    iface_s3: Mapped[int | None] = mapped_column(Integer)
    iface_s4: Mapped[int | None] = mapped_column(Integer)
    iface_h1: Mapped[str | None] = mapped_column(String)
    iface_h2: Mapped[str | None] = mapped_column(String)
    iface_h3: Mapped[str | None] = mapped_column(String)
    iface_h4: Mapped[str | None] = mapped_column(String)
    iface_i1: Mapped[str | None] = mapped_column(String)
    iface_i2: Mapped[str | None] = mapped_column(String)
    iface_i3: Mapped[str | None] = mapped_column(String)
    iface_i4: Mapped[str | None] = mapped_column(String)
    iface_i5: Mapped[str | None] = mapped_column(String)
    iface_save_config: Mapped[bool] = mapped_column(Boolean, default=True)
    iface_total_rx: Mapped[float | None] = mapped_column(Float)
    iface_total_tx: Mapped[float | None] = mapped_column(Float)
    iface_total_data: Mapped[float | None] = mapped_column(Float)

class Peers(Base):
    __tablename__ = 'interface_peers'

    peer_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    assigned_iface: Mapped[str | None] = mapped_column(String)
    peer_public_key: Mapped[str | None] = mapped_column(String)
    peer_private_key: Mapped[str | None] = mapped_column(String)
    peer_preshared_key: Mapped[str | None] = mapped_column(String)
    peer_name: Mapped[str | None] = mapped_column(String)
    peer_allowed_ips: Mapped[str | None] = mapped_column(String)
    peer_endpoint_allowed_ips: Mapped[str | None] = mapped_column(String)
    peer_dns: Mapped[str | None] = mapped_column(String)
    peer_mtu: Mapped[int | None] = mapped_column(Integer)
    peer_keep_alive: Mapped[int | None] = mapped_column(Integer)
    peer_remote_endpoint: Mapped[str | None] = mapped_column(String)
    peer_notes: Mapped[str | None] = mapped_column(String)
    peer_status: Mapped[str | None] = mapped_column(String)
    peer_latest_handshake: Mapped[str | None] = mapped_column(String)
    peer_endpoint: Mapped[str | None] = mapped_column(String)
    peer_total_rx: Mapped[float | None] = mapped_column(Float)
    peer_total_tx: Mapped[float | None] = mapped_column(Float)
    peer_cumulative_rx: Mapped[float | None] = mapped_column(Float)
    peer_cumulative_tx: Mapped[float | None] = mapped_column(Float)
    peer_group_id: Mapped[int | None] = mapped_column(Integer)
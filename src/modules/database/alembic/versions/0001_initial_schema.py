"""Create the initial WGDashboard schema.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-10-28
"""

from typing import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _interface_columns(include_amnezia: bool) -> list[sa.Column]:
    '''Build columns shared by the WireGuard interface tables.'''
    columns = [
        sa.Column("iface_status", sa.String(), nullable=True),
        sa.Column("iface_id", sa.Integer(), nullable=False),
        sa.Column("iface_name", sa.String(), nullable=True),
        sa.Column("iface_notes", sa.String(), nullable=True),
        sa.Column("iface_privkey", sa.String(), nullable=True),
        sa.Column("iface_pubkey", sa.String(), nullable=True),
        sa.Column("iface_address", sa.String(), nullable=True),
        sa.Column("iface_listen_port", sa.Integer(), nullable=True),
        sa.Column("iface_mtu", sa.Integer(), nullable=True),
        sa.Column("iface_preup", sa.String(), nullable=True),
        sa.Column("iface_predown", sa.String(), nullable=True),
        sa.Column("iface_postup", sa.String(), nullable=True),
        sa.Column("iface_postdown", sa.String(), nullable=True),
    ]

    if include_amnezia:
        columns.extend(
            [
                sa.Column("iface_jc", sa.Integer(), nullable=True),
                sa.Column("iface_jmin", sa.Integer(), nullable=True),
                sa.Column("iface_jmax", sa.Integer(), nullable=True),
                sa.Column("iface_s1", sa.Integer(), nullable=True),
                sa.Column("iface_s2", sa.Integer(), nullable=True),
                sa.Column("iface_s3", sa.Integer(), nullable=True),
                sa.Column("iface_s4", sa.Integer(), nullable=True),
                sa.Column("iface_h1", sa.String(), nullable=True),
                sa.Column("iface_h2", sa.String(), nullable=True),
                sa.Column("iface_h3", sa.String(), nullable=True),
                sa.Column("iface_h4", sa.String(), nullable=True),
                sa.Column("iface_i1", sa.String(), nullable=True),
                sa.Column("iface_i2", sa.String(), nullable=True),
                sa.Column("iface_i3", sa.String(), nullable=True),
                sa.Column("iface_i4", sa.String(), nullable=True),
                sa.Column("iface_i5", sa.String(), nullable=True),
            ]
        )

    columns.extend(
        [
            sa.Column("iface_save_config", sa.Boolean(), nullable=False),
            sa.Column("iface_total_rx", sa.Float(), nullable=True),
            sa.Column("iface_total_tx", sa.Float(), nullable=True),
            sa.Column("iface_total_data", sa.Float(), nullable=True),
            sa.PrimaryKeyConstraint("iface_id"),
            sa.UniqueConstraint("iface_name"),
            sa.UniqueConstraint("iface_privkey"),
            sa.UniqueConstraint("iface_pubkey"),
            sa.UniqueConstraint("iface_listen_port"),
        ]
    )
    return columns


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column("role", sa.String(), nullable=True),
        sa.Column("totp_enabled", sa.Boolean(), nullable=False),
        sa.Column("totp_verified", sa.Boolean(), nullable=False),
        sa.Column("totp_secret", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_users_user_id", "users", ["user_id"], unique=False)
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "apikeys",
        sa.Column("key_id", sa.Integer(), nullable=False),
        sa.Column("key_data", sa.String(), nullable=True),
        sa.Column("key_creation", sa.String(), nullable=True),
        sa.Column("key_expiration", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("key_id"),
    )
    op.create_index("ix_apikeys_key_id", "apikeys", ["key_id"], unique=False)

    op.create_table("wireguard_interfaces", *_interface_columns(include_amnezia=False))
    op.create_index("ix_wireguard_interfaces_iface_id", "wireguard_interfaces", ["iface_id"], unique=False)

    op.create_table("amnezia_interfaces", *_interface_columns(include_amnezia=True))
    op.create_index("ix_amnezia_interfaces_iface_id", "amnezia_interfaces", ["iface_id"], unique=False)

    op.create_table(
        "interface_peers",
        sa.Column("peer_id", sa.Integer(), nullable=False),
        sa.Column("assigned_iface", sa.String(), nullable=True),
        sa.Column("peer_public_key", sa.String(), nullable=True),
        sa.Column("peer_private_key", sa.String(), nullable=True),
        sa.Column("peer_preshared_key", sa.String(), nullable=True),
        sa.Column("peer_name", sa.String(), nullable=True),
        sa.Column("peer_allowed_ips", sa.String(), nullable=True),
        sa.Column("peer_endpoint_allowed_ips", sa.String(), nullable=True),
        sa.Column("peer_dns", sa.String(), nullable=True),
        sa.Column("peer_mtu", sa.Integer(), nullable=True),
        sa.Column("peer_keep_alive", sa.Integer(), nullable=True),
        sa.Column("peer_remote_endpoint", sa.String(), nullable=True),
        sa.Column("peer_notes", sa.String(), nullable=True),
        sa.Column("peer_status", sa.String(), nullable=True),
        sa.Column("peer_latest_handshake", sa.String(), nullable=True),
        sa.Column("peer_endpoint", sa.String(), nullable=True),
        sa.Column("peer_total_rx", sa.Float(), nullable=True),
        sa.Column("peer_total_tx", sa.Float(), nullable=True),
        sa.Column("peer_cumulative_rx", sa.Float(), nullable=True),
        sa.Column("peer_cumulative_tx", sa.Float(), nullable=True),
        sa.Column("peer_group_id", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("peer_id"),
    )
    op.create_index("ix_interface_peers_peer_id", "interface_peers", ["peer_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_interface_peers_peer_id", table_name="interface_peers")
    op.drop_table("interface_peers")
    op.drop_index("ix_amnezia_interfaces_iface_id", table_name="amnezia_interfaces")
    op.drop_table("amnezia_interfaces")
    op.drop_index("ix_wireguard_interfaces_iface_id", table_name="wireguard_interfaces")
    op.drop_table("wireguard_interfaces")
    op.drop_index("ix_apikeys_key_id", table_name="apikeys")
    op.drop_table("apikeys")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_user_id", table_name="users")
    op.drop_table("users")

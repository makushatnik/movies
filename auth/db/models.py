import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import or_
from sqlalchemy.dialects.postgresql import UUID
from db import db


def create_partition(target, connection, **kw) -> None:
    """ creating partitions in user_sign_in """
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_sign_in_smart"
        PARTITION OF "users_sign_in" FOR VALUES IN ('smart')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_sign_in_mobile"
        PARTITION OF "users_sign_in" FOR VALUES IN ('mobile')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_sign_in_web"
        PARTITION OF "users_sign_in" FOR VALUES IN ('web')"""
    )


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.login}>'

    @classmethod
    def get_user_by_universal_login(cls, login: Optional[str] = None,
                                    email: Optional[str] = None):
        return cls.query.filter(or_(cls.login == login, cls.email == email)).first()


class SocialAccount(db.Model):
    __tablename__ = 'social_account'
    __table_args__ = (db.UniqueConstraint('social_id', 'social_name', name='social_pk'))

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(User, backref=db.backref('social_accounts', lazy=True))
    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>'


class UserSignIn(db.Model):
    __tablename__ = 'users_sign_in'
    __table_args__ = {
        'postgresql_partition_by': 'LIST (user_device_type)',
        'listeners': [('after_create', create_partition)],
    }

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    logined_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_agent = db.Column(db.Text)
    user_device_type = db.Column(db.Text)

    def __repr__(self):
        return f'<UserSignIn {self.user_id}:{self.logined_at}>'

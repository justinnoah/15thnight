"""Data Models."""
from datetime import datetime, timedelta

from sqlalchemy import (
    Column, DateTime, Enum, ForeignKey, Integer, String, Table, Text, and_,
    desc
)
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from _15thnight.database import Model


class User(Model):
    """
    User Model.

    Required parameters:
        - email, password, phone_number
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    phone_number = Column(String(20), nullable=False)
    role = Column(Enum('admin', 'advocate', 'provider'), default='advocate')
    categories = relationship(
        "Category", secondary="user_categories", backref="users")

    def __init__(self, email, password, phone_number, categories, role):
        self.email = email.lower()
        self.set_password(password)
        self.phone_number = phone_number
        self.role = role
        self.categories = categories

    def check_password(self, password):
        """Check a user's password (includes salt)."""
        return check_password_hash(self.password, password)

    def provider_capabilities(self):
        categories = []
        for category in self.categories:
            categories.append(category.name)

        return ", ".join(categories)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_advocate(self):
        return self.role == 'advocate'

    @property
    def is_provider(self):
        return self.role == 'provider'

    @property
    def is_authenticated(self):
        """Authenticaition check."""
        return True

    @property
    def is_active(self):
        """Active check."""
        return True

    @property
    def is_anonymous(self):
        """Anonimity check."""
        return False

    def get_id(self):
        """Get the User id in unicode or ascii."""
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    @classmethod
    def get_users(cls):
        return cls.query.order_by(desc(cls.created_at)).all()

    @classmethod
    def users_in_categories(cls, categories):
        """Return a list of users in the passed in categories."""
        users = cls.query.join(cls.categories) \
            .filter(Category.id.in_(categories)) \
            .distinct()

        return users

    def get_alerts(self):
        return Alert.query.filter(
            Alert.user == self).order_by(desc(Alert.created_at)).all()

    @classmethod
    def get_by_email(cls, email):
        """Return user based on email."""
        return cls.query.filter(cls.email == email).first()

    def set_password(self, password):
        """Using pbkdf2:sha512, hash 'password'."""
        self.password = generate_password_hash(
            password=password,
            method='pbkdf2:sha512',
            salt_length=128
        )

    def __repr__(self):
        """Return <User: %(email)."""
        return '<User %s>' % (self.email)


class Alert(Model):
    """Alert Model for alertering users."""

    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    description = Column(String(200), nullable=False)
    gender = Column(Enum(
        'male', 'female', 'unspecified'), nullable=False, default='unspecified'
    )
    age = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='alerts')
    categories = relationship(
        "Category", secondary="alert_categories", backref="alerts")

    def get_needs(self):
        categories = []
        for category in self.categories:
            categories.append(category.name)

        return ", ".join(categories)

    @classmethod
    def get_active_alerts_for_provider(cls, user):
        time_to_filter_from = datetime.now() - timedelta(days=2)
        alerts_past_two_days = cls.query\
            .filter(cls.created_at > time_to_filter_from)\
            .order_by(desc(cls.created_at)) \
            .all()
        responded_alerts = map(
            lambda respond: respond.alert_id,
            Response.query.filter(
                Response.user_id == user.id,
                Response.created_at > time_to_filter_from
            )
        )

        for alert in alerts_past_two_days:
            if alert.id in responded_alerts:
                alerts_past_two_days.remove(alert)

        return alerts_past_two_days

    @classmethod
    def get_user_alerts(cls, user):
        return cls.query.filter(cls.user == user).all()

    @classmethod
    def get_user_alert(cls, user, id):
        return cls.query.filter(cls.user == user & cls.id == id).first()

    @classmethod
    def get_alerts(cls):
        return cls.query.order_by(desc(Alert.created_at)).all()

    def get_user_response(self, user):
        response = Response.get_by_user_and_alert(user, self)
        if response:
            return response
        return False


class Category(Model):
    """Category/type of provided help representation."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    description = Column(Text)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @classmethod
    def get_by_ids(cls, id_list):
        return cls.query.filter(cls.id.in_(id_list)).all()

    @classmethod
    def get_by_name(cls, name):
        named = cls.query.filter(cls.name == name).first()
        return named


class Response(Model):
    """Response model."""

    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'))
    user = relationship('User', backref='responses')
    created_at = Column(DateTime, default=datetime.utcnow)
    alert_id = Column(ForeignKey('alerts.id'))
    alert = relationship('Alert', backref='responses')
    message = Column(Text, nullable=True, default='')

    @classmethod
    def get_by_user_and_alert(cls, user, alert):
        return cls.query.filter(
            cls.user == user).filter(cls.alert == alert).all()


class SlackMessage(Model):
    """Record of messages sent to slack."""

    __tablename__ = 'slack_messages'
    id = Column(Integer, primary_key=True)
    alert_id = Column(Integer, ForeignKey('alerts.id'), nullable=False)
    channel = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)

    def get_valid_message(cls, alert_id, channel):
        """Check that the alert_id comes from an IM that was sent."""

        valid = SlackMessage.query.filter(and_(
            SlackMessage.alert_id == alert_id,
            SlackMessage.channel == channel
        )).first()
        return valid


user_categories = Table(
    "user_categories", Model.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("category_id", Integer, ForeignKey("categories.id"))
)

alert_categories = Table(
    "alert_categories", Model.metadata,
    Column("alert_id", Integer, ForeignKey("alerts.id")),
    Column("category_id", Integer, ForeignKey("categories.id"))
)

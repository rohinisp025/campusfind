from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def utc_now():
    return datetime.now(timezone.utc)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    department = db.Column(db.String(100), default='Computer Applications')
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='student', nullable=False)  # 'student' or 'admin'
    avatar = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationships
    items = db.relationship('Item', backref='reporter', lazy='dynamic', cascade='all, delete-orphan')
    claims = db.relationship('Claim', backref='claimant', lazy='dynamic', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'student_id': self.student_id,
            'department': self.department,
            'phone': self.phone,
            'role': self.role,
            'avatar': self.avatar,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, index=True)
    type = db.Column(db.String(20), nullable=False, index=True)  # 'lost' or 'found'
    category = db.Column(db.String(50), nullable=False, index=True)  # 'Electronics', 'ID & Cards', 'Keys', etc.
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(150), nullable=False, index=True)  # 'Library', 'Canteen', 'Lab 3', etc.
    date_lost_or_found = db.Column(db.String(50), nullable=False)  # ISO date string YYYY-MM-DD
    primary_color = db.Column(db.String(50), nullable=True)
    brand = db.Column(db.String(50), nullable=True)
    photo_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(30), default='open', nullable=False, index=True)  # 'open', 'claimed', 'resolved', 'closed'
    contact_email = db.Column(db.String(120), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    claims = db.relationship('Claim', backref='item', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, include_reporter=True):
        data = {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'category': self.category,
            'description': self.description,
            'location': self.location,
            'date_lost_or_found': self.date_lost_or_found,
            'primary_color': self.primary_color,
            'brand': self.brand,
            'photo_url': self.photo_url,
            'status': self.status,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'claims_count': self.claims.count()
        }
        if include_reporter and self.reporter:
            data['reporter'] = {
                'id': self.reporter.id,
                'name': self.reporter.name,
                'email': self.reporter.email,
                'student_id': self.reporter.student_id,
                'department': self.reporter.department
            }
        return data


class Claim(db.Model):
    __tablename__ = 'claims'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id', ondelete='CASCADE'), nullable=False)
    claimant_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    proof_description = db.Column(db.Text, nullable=False)
    secret_identifier = db.Column(db.Text, nullable=True)
    proof_image_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='pending', nullable=False)  # 'pending', 'approved', 'rejected'
    admin_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    messages = db.relationship('ClaimMessage', backref='claim', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, include_details=True):
        data = {
            'id': self.id,
            'item_id': self.item_id,
            'claimant_id': self.claimant_id,
            'proof_description': self.proof_description,
            'secret_identifier': self.secret_identifier,
            'proof_image_url': self.proof_image_url,
            'status': self.status,
            'admin_notes': self.admin_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_details:
            if self.claimant:
                data['claimant'] = {
                    'id': self.claimant.id,
                    'name': self.claimant.name,
                    'email': self.claimant.email,
                    'student_id': self.claimant.student_id,
                    'department': self.claimant.department,
                    'phone': self.claimant.phone
                }
            if self.item:
                data['item'] = {
                    'id': self.item.id,
                    'title': self.item.title,
                    'type': self.item.type,
                    'category': self.item.category,
                    'location': self.item.location,
                    'photo_url': self.item.photo_url,
                    'status': self.item.status,
                    'reporter_id': self.item.user_id,
                    'reporter_name': self.item.reporter.name if self.item.reporter else 'Unknown'
                }
        return data


class ClaimMessage(db.Model):
    __tablename__ = 'claim_messages'

    id = db.Column(db.Integer, primary_key=True)
    claim_id = db.Column(db.Integer, db.ForeignKey('claims.id', ondelete='CASCADE'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    # Sender relationship
    sender = db.relationship('User', foreign_keys=[sender_id])

    def to_dict(self):
        return {
            'id': self.id,
            'claim_id': self.claim_id,
            'sender_id': self.sender_id,
            'sender_name': self.sender.name if self.sender else 'User',
            'sender_role': self.sender.role if self.sender else 'student',
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), default='info')  # 'claim', 'approval', 'item', 'admin'
    link = db.Column(db.String(200), nullable=True)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'link': self.link,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """User model for authentication and roles"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'buyer', 'supplier', 'admin'
    profile_image = db.Column(db.String(255), nullable=True)  # Path to profile image
    company_name = db.Column(db.String(150), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    machines = db.relationship('Machine', backref='supplier', lazy=True)
    enquiries = db.relationship('Enquiry', foreign_keys='Enquiry.buyer_id', backref='buyer', lazy=True)
    
    def __repr__(self):
        return f'<User {self.name} ({self.role})>'

class Machine(db.Model):
    """Machine model for supplier listings"""
    __tablename__ = 'machines'
    
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    use_case = db.Column(db.String(200), nullable=False)
    price_range = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Multiple image URLs
    image_front = db.Column(db.String(500))
    image_side = db.Column(db.String(500))
    image_working = db.Column(db.String(500))
    image_closeup = db.Column(db.String(500))
    
    # Additional specification fields
    production_capacity = db.Column(db.String(100))
    automation_level = db.Column(db.String(50))
    power_requirement = db.Column(db.String(100))
    machine_dimensions = db.Column(db.String(100))
    raw_material = db.Column(db.String(200))
    operator_skill = db.Column(db.String(100))
    warranty_info = db.Column(db.String(200))
    
    # Business fit information
    ideal_industry = db.Column(db.String(200))
    business_size_fit = db.Column(db.String(100))
    installation_support = db.Column(db.String(10))  # yes/no
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    enquiries = db.relationship('Enquiry', backref='machine', lazy=True)
    
    def __repr__(self):
        return f'<Machine {self.name}>'
    
    @property
    def image_url(self):
        """Return the primary image URL for backward compatibility"""
        return self.image_front or self.image_side or self.image_working or self.image_closeup
    
    @property
    def all_images(self):
        """Return all available images as a list"""
        images = []
        if self.image_front:
            images.append({'url': self.image_front, 'type': 'Front View'})
        if self.image_side:
            images.append({'url': self.image_side, 'type': 'Side View'})
        if self.image_working:
            images.append({'url': self.image_working, 'type': 'Working View'})
        if self.image_closeup:
            images.append({'url': self.image_closeup, 'type': 'Close-up View'})
        return images

class Enquiry(db.Model):
    """Enquiry model for buyer-supplier interactions"""
    __tablename__ = 'enquiries'
    
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    budget = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    production_need = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'responded', 'closed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Enquiry for Machine {self.machine_id} by Buyer {self.buyer_id}>'

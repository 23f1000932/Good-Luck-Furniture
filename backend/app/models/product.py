from datetime import datetime, timezone
from ..extensions import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False, index=True)
    short_description = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=True)

    # Taxonomy
    collection_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True, index=True)
    product_type = db.Column(db.String(100), nullable=True)

    # Attributes
    material = db.Column(db.String(200), nullable=True)
    finish = db.Column(db.String(200), nullable=True)
    color = db.Column(db.String(100), nullable=True)
    dimensions = db.Column(db.String(300), nullable=True)

    # Pricing
    price = db.Column(db.Numeric(10, 2), nullable=True)
    price_visibility = db.Column(
        db.String(30),
        nullable=False,
        default='contact_for_price'
    )  # visible | contact_for_price | hidden

    # Status
    is_featured = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    display_order = db.Column(db.Integer, nullable=False, default=0)

    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationship
    images = db.relationship(
        'ProductImage',
        backref='product',
        lazy='joined',
        cascade='all, delete-orphan',
        order_by='ProductImage.display_order'
    )

    @property
    def primary_image(self):
        """Return the primary image or the first image."""
        for img in self.images:
            if img.is_primary:
                return img
        return self.images[0] if self.images else None

    def to_dict(self, include_images=True):
        data = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'short_description': self.short_description,
            'description': self.description,
            'collection_id': self.collection_id,
            'collection': self.collection.to_dict() if self.collection else None,
            'product_type': self.product_type,
            'material': self.material,
            'finish': self.finish,
            'color': self.color,
            'dimensions': self.dimensions,
            'price': float(self.price) if self.price is not None else None,
            'price_visibility': self.price_visibility,
            'is_featured': self.is_featured,
            'is_active': self.is_active,
            'display_order': self.display_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_images:
            data['images'] = [img.to_dict() for img in self.images]
            primary = self.primary_image
            data['primary_image'] = primary.to_dict() if primary else None
        return data

    def __repr__(self):
        return f'<Product {self.name}>'

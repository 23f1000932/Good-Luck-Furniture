from datetime import datetime, timezone
from ..extensions import db


class ProductImage(db.Model):
    __tablename__ = 'product_images'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    image_url = db.Column(db.String(1000), nullable=False)
    storage_path = db.Column(db.String(1000), nullable=True)
    alt_text = db.Column(db.String(300), nullable=True)
    display_order = db.Column(db.Integer, nullable=False, default=0)
    is_primary = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'image_url': self.image_url,
            'storage_path': self.storage_path,
            'alt_text': self.alt_text,
            'display_order': self.display_order,
            'is_primary': self.is_primary,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<ProductImage {self.id} product={self.product_id}>'

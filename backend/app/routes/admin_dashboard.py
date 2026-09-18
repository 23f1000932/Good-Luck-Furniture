from flask import Blueprint
from ..extensions import db
from ..models.product import Product
from ..models.category import Category
from ..utils.responses import success_response
from ..utils.decorators import require_admin

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)


@admin_dashboard_bp.route('/dashboard', methods=['GET'])
@require_admin
def dashboard_stats():
    """Admin: dashboard overview statistics."""
    total_products = Product.query.count()
    active_products = Product.query.filter_by(is_active=True).count()
    inactive_products = total_products - active_products
    featured_products = Product.query.filter_by(is_featured=True, is_active=True).count()
    total_categories = Category.query.count()
    active_categories = Category.query.filter_by(is_active=True).count()

    recent_products = (
        Product.query
        .order_by(Product.created_at.desc())
        .limit(5)
        .all()
    )

    return success_response({
        'stats': {
            'total_products': total_products,
            'active_products': active_products,
            'inactive_products': inactive_products,
            'featured_products': featured_products,
            'total_categories': total_categories,
            'active_categories': active_categories,
        },
        'recent_products': [p.to_dict() for p in recent_products],
    })

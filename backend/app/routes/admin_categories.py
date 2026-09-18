from flask import Blueprint, request
from ..extensions import db
from ..models.category import Category
from ..utils.responses import success_response, error_response
from ..utils.decorators import require_admin
from ..utils.validators import validate_required_fields
from ..utils.slugify import unique_slug

admin_categories_bp = Blueprint('admin_categories', __name__)


@admin_categories_bp.route('/categories', methods=['GET'])
@require_admin
def list_categories():
    """Admin: list all categories."""
    categories = Category.query.order_by(Category.display_order, Category.name).all()
    return success_response([c.to_dict(include_product_count=True) for c in categories])


@admin_categories_bp.route('/categories', methods=['POST'])
@require_admin
def create_category():
    """Admin: create a category."""
    data = request.get_json()
    if not data:
        return error_response('BAD_REQUEST', 'Request body required', 400)

    missing = validate_required_fields(data, ['name'])
    if missing:
        return error_response('VALIDATION_ERROR', f'Required fields: {", ".join(missing)}', 400)

    slug = unique_slug(data['name'], Category)

    category = Category(
        name=data['name'].strip(),
        slug=slug,
        description=data.get('description', ''),
        image_url=data.get('image_url', ''),
        display_order=int(data.get('display_order', 0)),
        is_active=bool(data.get('is_active', True)),
    )
    db.session.add(category)
    db.session.commit()
    return success_response(category.to_dict(), 'Category created', 201)


@admin_categories_bp.route('/categories/<int:category_id>', methods=['PUT'])
@require_admin
def update_category(category_id):
    """Admin: update a category."""
    category = Category.query.get(category_id)
    if not category:
        return error_response('NOT_FOUND', 'Category not found', 404)

    data = request.get_json()
    if not data:
        return error_response('BAD_REQUEST', 'Request body required', 400)

    if 'name' in data and data['name'].strip() != category.name:
        category.slug = unique_slug(data['name'], Category, existing_id=category_id)
        category.name = data['name'].strip()

    for field in ['description', 'image_url', 'display_order', 'is_active']:
        if field in data:
            setattr(category, field, data[field])

    db.session.commit()
    return success_response(category.to_dict(), 'Category updated')


@admin_categories_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@require_admin
def delete_category(category_id):
    """Admin: delete a category (only if no products are using it)."""
    category = Category.query.get(category_id)
    if not category:
        return error_response('NOT_FOUND', 'Category not found', 404)

    product_count = category.products.count()
    if product_count > 0:
        return error_response(
            'CONSTRAINT_ERROR',
            f'Cannot delete: {product_count} product(s) belong to this category. '
            'Reassign or remove them first.',
            409
        )

    db.session.delete(category)
    db.session.commit()
    return success_response(message='Category deleted')

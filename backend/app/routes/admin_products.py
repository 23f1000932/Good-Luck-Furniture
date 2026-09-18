from flask import Blueprint, request
from ..extensions import db
from ..models.product import Product
from ..models.product_image import ProductImage
from ..models.category import Category
from ..utils.responses import success_response, error_response, paginated_response
from ..utils.decorators import require_admin
from ..utils.validators import (
    validate_required_fields, validate_price_visibility,
    validate_image_file
)
from ..utils.slugify import unique_slug
from ..services.image_service import save_image, delete_image

admin_products_bp = Blueprint('admin_products', __name__)


# ─────────────────────────────────────────────
# Product CRUD
# ─────────────────────────────────────────────

@admin_products_bp.route('/products', methods=['GET'])
@require_admin
def list_products():
    """Admin: list all products with pagination."""
    page = max(int(request.args.get('page', 1)), 1)
    per_page = min(int(request.args.get('per_page', 20)), 100)
    search = request.args.get('search', '').strip()
    status = request.args.get('status', '')  # active | inactive | all

    query = Product.query

    if search:
        like = f'%{search}%'
        query = query.filter(
            (Product.name.ilike(like)) |
            (Product.product_type.ilike(like))
        )

    if status == 'active':
        query = query.filter_by(is_active=True)
    elif status == 'inactive':
        query = query.filter_by(is_active=False)

    query = query.order_by(Product.updated_at.desc())
    total = query.count()
    products = query.offset((page - 1) * per_page).limit(per_page).all()

    return paginated_response(
        items=[p.to_dict() for p in products],
        total=total,
        page=page,
        per_page=per_page
    )


@admin_products_bp.route('/products', methods=['POST'])
@require_admin
def create_product():
    """Admin: create a new product."""
    data = request.get_json()
    if not data:
        return error_response('BAD_REQUEST', 'Request body required', 400)

    missing = validate_required_fields(data, ['name'])
    if missing:
        return error_response('VALIDATION_ERROR', f'Required fields missing: {", ".join(missing)}', 400)

    # Validate price_visibility
    pv = data.get('price_visibility', 'contact_for_price')
    valid_pv, pv_error = validate_price_visibility(pv)
    if not valid_pv:
        return error_response('VALIDATION_ERROR', pv_error, 400)

    slug = unique_slug(data['name'], Product)

    product = Product(
        name=data['name'].strip(),
        slug=slug,
        short_description=data.get('short_description', ''),
        description=data.get('description', ''),
        collection_id=data.get('collection_id'),
        product_type=data.get('product_type', ''),
        material=data.get('material', ''),
        finish=data.get('finish', ''),
        color=data.get('color', ''),
        dimensions=data.get('dimensions', ''),
        price=data.get('price'),
        price_visibility=pv,
        is_featured=bool(data.get('is_featured', False)),
        is_active=bool(data.get('is_active', True)),
        display_order=int(data.get('display_order', 0)),
    )

    db.session.add(product)
    db.session.commit()
    return success_response(product.to_dict(), 'Product created', 201)


@admin_products_bp.route('/products/<int:product_id>', methods=['GET'])
@require_admin
def get_product(product_id):
    """Admin: get a single product."""
    product = Product.query.get(product_id)
    if not product:
        return error_response('NOT_FOUND', 'Product not found', 404)
    return success_response(product.to_dict())


@admin_products_bp.route('/products/<int:product_id>', methods=['PUT'])
@require_admin
def update_product(product_id):
    """Admin: update a product."""
    product = Product.query.get(product_id)
    if not product:
        return error_response('NOT_FOUND', 'Product not found', 404)

    data = request.get_json()
    if not data:
        return error_response('BAD_REQUEST', 'Request body required', 400)

    # Regenerate slug only if name changed
    if 'name' in data and data['name'].strip() != product.name:
        product.slug = unique_slug(data['name'], Product, existing_id=product_id)
        product.name = data['name'].strip()

    if 'price_visibility' in data:
        valid_pv, pv_error = validate_price_visibility(data['price_visibility'])
        if not valid_pv:
            return error_response('VALIDATION_ERROR', pv_error, 400)
        product.price_visibility = data['price_visibility']

    fields = [
        'short_description', 'description', 'collection_id', 'product_type',
        'material', 'finish', 'color', 'dimensions', 'price',
        'is_featured', 'is_active', 'display_order'
    ]
    for field in fields:
        if field in data:
            setattr(product, field, data[field])

    db.session.commit()
    return success_response(product.to_dict(), 'Product updated')


@admin_products_bp.route('/products/<int:product_id>', methods=['DELETE'])
@require_admin
def delete_product(product_id):
    """Admin: delete a product and its images."""
    product = Product.query.get(product_id)
    if not product:
        return error_response('NOT_FOUND', 'Product not found', 404)

    # Delete image files
    for image in product.images:
        if image.storage_path:
            delete_image(image.storage_path)

    db.session.delete(product)
    db.session.commit()
    return success_response(message='Product deleted')


# ─────────────────────────────────────────────
# Image management
# ─────────────────────────────────────────────

@admin_products_bp.route('/products/<int:product_id>/images', methods=['POST'])
@require_admin
def upload_images(product_id):
    """Admin: upload one or more images for a product."""
    product = Product.query.get(product_id)
    if not product:
        return error_response('NOT_FOUND', 'Product not found', 404)

    files = request.files.getlist('images')
    if not files:
        return error_response('BAD_REQUEST', 'No images provided', 400)

    # Determine next display_order
    existing_max = db.session.query(
        db.func.max(ProductImage.display_order)
    ).filter_by(product_id=product_id).scalar() or -1

    uploaded = []
    errors = []

    for idx, file in enumerate(files):
        is_valid, err = validate_image_file(file)
        if not is_valid:
            errors.append({'filename': file.filename, 'error': err})
            continue

        try:
            image_url, storage_path = save_image(file, product_id)
            is_first = (not product.images and not uploaded)
            image = ProductImage(
                product_id=product_id,
                image_url=image_url,
                storage_path=storage_path,
                alt_text=request.form.get('alt_text', product.name),
                display_order=existing_max + idx + 1,
                is_primary=is_first,
            )
            db.session.add(image)
            uploaded.append(image)
        except Exception as e:
            errors.append({'filename': file.filename, 'error': str(e)})

    db.session.commit()

    response_data = {
        'uploaded': [img.to_dict() for img in uploaded],
        'errors': errors,
    }
    status = 201 if uploaded else 400
    return success_response(response_data, f'{len(uploaded)} image(s) uploaded', status)


@admin_products_bp.route('/products/<int:product_id>/images/<int:image_id>', methods=['DELETE'])
@require_admin
def delete_product_image(product_id, image_id):
    """Admin: delete a product image."""
    image = ProductImage.query.filter_by(id=image_id, product_id=product_id).first()
    if not image:
        return error_response('NOT_FOUND', 'Image not found', 404)

    was_primary = image.is_primary

    if image.storage_path:
        delete_image(image.storage_path)

    db.session.delete(image)
    db.session.flush()

    # Reassign primary if needed
    if was_primary:
        remaining = ProductImage.query.filter_by(product_id=product_id).order_by(
            ProductImage.display_order
        ).first()
        if remaining:
            remaining.is_primary = True

    db.session.commit()
    return success_response(message='Image deleted')


@admin_products_bp.route('/products/<int:product_id>/images/reorder', methods=['PUT'])
@require_admin
def reorder_images(product_id):
    """
    Admin: reorder images.
    Body: { "order": [{ "id": 1, "display_order": 0 }, ...] }
    """
    product = Product.query.get(product_id)
    if not product:
        return error_response('NOT_FOUND', 'Product not found', 404)

    data = request.get_json()
    order_list = data.get('order', [])

    for item in order_list:
        image = ProductImage.query.filter_by(id=item['id'], product_id=product_id).first()
        if image:
            image.display_order = item.get('display_order', 0)
            if item.get('is_primary'):
                # Unset all primaries first
                ProductImage.query.filter_by(product_id=product_id).update({'is_primary': False})
                image.is_primary = True

    db.session.commit()
    updated = ProductImage.query.filter_by(product_id=product_id).order_by(
        ProductImage.display_order
    ).all()
    return success_response([img.to_dict() for img in updated], 'Images reordered')


@admin_products_bp.route('/products/<int:product_id>/images/<int:image_id>/primary', methods=['PUT'])
@require_admin
def set_primary_image(product_id, image_id):
    """Admin: set an image as primary."""
    product = Product.query.get(product_id)
    if not product:
        return error_response('NOT_FOUND', 'Product not found', 404)

    ProductImage.query.filter_by(product_id=product_id).update({'is_primary': False})
    image = ProductImage.query.filter_by(id=image_id, product_id=product_id).first()
    if not image:
        return error_response('NOT_FOUND', 'Image not found', 404)

    image.is_primary = True
    db.session.commit()
    return success_response(image.to_dict(), 'Primary image set')

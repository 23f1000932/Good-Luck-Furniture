from flask import Blueprint, request
from ..models.product import Product
from ..models.category import Category
from ..models.product_image import ProductImage
from ..utils.responses import success_response, error_response, paginated_response

public_bp = Blueprint('public', __name__)


@public_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all active categories."""
    categories = (
        Category.query
        .filter_by(is_active=True)
        .order_by(Category.display_order, Category.name)
        .all()
    )
    return success_response([c.to_dict(include_product_count=True) for c in categories])


@public_bp.route('/categories/<slug>', methods=['GET'])
def get_category(slug):
    """Get a single category by slug."""
    category = Category.query.filter_by(slug=slug, is_active=True).first()
    if not category:
        return error_response('NOT_FOUND', 'Category not found', 404)
    return success_response(category.to_dict(include_product_count=True))


@public_bp.route('/featured-products', methods=['GET'])
def get_featured_products():
    """Get featured products for homepage."""
    limit = min(int(request.args.get('limit', 8)), 20)
    products = (
        Product.query
        .filter_by(is_active=True, is_featured=True)
        .order_by(Product.display_order, Product.updated_at.desc())
        .limit(limit)
        .all()
    )
    return success_response([p.to_dict() for p in products])


@public_bp.route('/products', methods=['GET'])
def get_products():
    """
    Get paginated products with optional filtering and search.
    Query params: search, collection, product_type, page, per_page, sort
    """
    # Pagination
    page = max(int(request.args.get('page', 1)), 1)
    per_page = min(int(request.args.get('per_page', 12)), 48)

    # Filters
    search = request.args.get('search', '').strip()
    collection_slug = request.args.get('collection', '').strip()
    product_type = request.args.get('product_type', '').strip()
    sort = request.args.get('sort', 'newest')  # newest | oldest | name_asc | name_desc

    query = Product.query.filter_by(is_active=True)

    if search:
        like = f'%{search}%'
        query = query.filter(
            (Product.name.ilike(like)) |
            (Product.short_description.ilike(like)) |
            (Product.product_type.ilike(like)) |
            (Product.material.ilike(like))
        )

    if collection_slug:
        category = Category.query.filter_by(slug=collection_slug, is_active=True).first()
        if category:
            query = query.filter_by(collection_id=category.id)

    if product_type:
        query = query.filter(Product.product_type.ilike(product_type))

    # Sorting
    if sort == 'newest':
        query = query.order_by(Product.created_at.desc())
    elif sort == 'oldest':
        query = query.order_by(Product.created_at.asc())
    elif sort == 'name_asc':
        query = query.order_by(Product.name.asc())
    elif sort == 'name_desc':
        query = query.order_by(Product.name.desc())
    else:
        query = query.order_by(Product.display_order, Product.created_at.desc())

    total = query.count()
    products = query.offset((page - 1) * per_page).limit(per_page).all()

    return paginated_response(
        items=[p.to_dict() for p in products],
        total=total,
        page=page,
        per_page=per_page
    )


@public_bp.route('/products/<slug>', methods=['GET'])
def get_product(slug):
    """Get a single product by slug."""
    product = Product.query.filter_by(slug=slug, is_active=True).first()
    if not product:
        return error_response('NOT_FOUND', 'Product not found', 404)
    return success_response(product.to_dict())


@public_bp.route('/product-types', methods=['GET'])
def get_product_types():
    """Get all distinct product types for filter UI."""
    from ..extensions import db
    types = db.session.query(Product.product_type).filter(
        Product.is_active == True,
        Product.product_type != None,
        Product.product_type != ''
    ).distinct().order_by(Product.product_type).all()
    return success_response([t[0] for t in types if t[0]])

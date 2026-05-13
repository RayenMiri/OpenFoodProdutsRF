from flask import Blueprint, jsonify, request
from sqlalchemy import func, select
from extensions import db
from models.product import Product

products_bp = Blueprint("products", __name__)


@products_bp.get("/api/products/search")
def search_products():
    q = request.args.get("q", "").strip()

    # Safe int parsing for pagination parameters with fallback to defaults
    try:
        page = max(int(request.args.get("page", 1)), 1)
    except (ValueError, TypeError):
        page = 1

    try:
        page_size = min(int(request.args.get("page_size", 20)), 100)
    except (ValueError, TypeError):
        page_size = 20

    # DB stores grades in lowercase; normalize user input for case-insensitive matching
    grade = request.args.get("grade", "").strip().lower()
    category = request.args.get("category", "").strip()
    country = request.args.get("country", "").strip()

    filters = []

    if q:
        tsquery = func.plainto_tsquery("english", q)
        tsvector = func.to_tsvector(
            "english",
            func.coalesce(Product.product_name, "") + " " + func.coalesce(Product.brands, ""),
        )
        filters.append(tsvector.op("@@")(tsquery))

    if grade:
        filters.append(Product.nutrition_grade_fr == grade)
    if category:
        filters.append(Product.categories.ilike(f"%{category}%"))
    if country:
        filters.append(Product.countries.ilike(f"%{country}%"))

    count_stmt = select(func.count()).select_from(Product)
    data_stmt = select(Product)
    for f in filters:
        count_stmt = count_stmt.where(f)
        data_stmt = data_stmt.where(f)

    total = db.session.execute(count_stmt).scalar()
    items = db.session.execute(
        data_stmt.offset((page - 1) * page_size).limit(page_size)
    ).scalars().all()

    return jsonify(
        total=total,
        page=page,
        page_size=page_size,
        items=[p.to_summary() for p in items],
    )


@products_bp.get("/api/products/<barcode>")
def get_product(barcode):
    product = db.session.get(Product, barcode)
    if not product:
        return jsonify(error="Product not found", barcode=barcode), 404
    return jsonify(product.to_detail())

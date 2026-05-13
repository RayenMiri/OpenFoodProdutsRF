import pytest
from models.product import Product


@pytest.fixture(autouse=True)
def seed(db):
    db.session.add(Product(
        barcode="TEST000000001",
        product_name="Nutella",
        brands="Ferrero",
        categories="Spreads, Sweet spreads",
        countries="France",
        ingredients_text="Sugar, Palm oil, Hazelnuts",
        allergens="en:gluten, en:milk",
        nutrition_grade_fr="e",
        nutrition_score_fr_100g=26.0,
        image_url="https://example.com/nutella.jpg",
        image_small_url="https://example.com/nutella_small.jpg",
        url="https://world.openfoodfacts.org/product/3017620422003",
    ))
    db.session.commit()
    yield
    db.session.query(Product).filter(Product.barcode == "TEST000000001").delete()
    db.session.commit()


def test_get_product_returns_full_detail(client):
    resp = client.get("/api/products/TEST000000001")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["barcode"] == "TEST000000001"
    assert data["product_name"] == "Nutella"
    assert data["brands"] == "Ferrero"


def test_get_product_allergen_list_is_parsed(client):
    resp = client.get("/api/products/TEST000000001")
    data = resp.get_json()
    assert data["allergen_list"] == ["en:gluten", "en:milk"]


def test_get_product_ingredient_count(client):
    resp = client.get("/api/products/TEST000000001")
    data = resp.get_json()
    assert data["ingredient_count"] == 3


def test_get_product_not_found(client):
    resp = client.get("/api/products/9999999999999")
    assert resp.status_code == 404
    data = resp.get_json()
    assert "error" in data
    assert data["barcode"] == "9999999999999"

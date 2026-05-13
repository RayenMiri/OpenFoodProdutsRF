import pytest
from models.product import Product


@pytest.fixture(autouse=True)
def seed(db):
    db.session.add_all([
        Product(
            barcode="0000000000001",
            product_name="Nutella",
            brands="Ferrero",
            categories="Spreads",
            countries="France",
            nutrition_grade_fr="e",
            nutrition_score_fr_100g=26.0,
        ),
        Product(
            barcode="0000000000002",
            product_name="Greek Yogurt",
            brands="Danone",
            categories="Dairy",
            countries="United Kingdom",
            nutrition_grade_fr="b",
            nutrition_score_fr_100g=-2.0,
        ),
    ])
    db.session.commit()
    yield
    db.session.query(Product).delete()
    db.session.commit()


def test_search_returns_all_when_empty_query(client):
    resp = client.get("/api/products/search")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] >= 2
    assert len(data["items"]) >= 2


def test_search_filters_by_grade(client):
    resp = client.get("/api/products/search?grade=e&q=Nutella")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] >= 1
    barcodes = [item["barcode"] for item in data["items"]]
    assert "0000000000001" in barcodes


def test_search_filters_by_category(client):
    resp = client.get("/api/products/search?category=Dairy&q=Greek+Yogurt")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] >= 1
    barcodes = [item["barcode"] for item in data["items"]]
    assert "0000000000002" in barcodes


def test_search_filters_by_country(client):
    resp = client.get("/api/products/search?country=France&q=Nutella")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] >= 1
    barcodes = [item["barcode"] for item in data["items"]]
    assert "0000000000001" in barcodes


def test_search_full_text_match(client):
    resp = client.get("/api/products/search?q=Nutella")
    assert resp.status_code == 200
    data = resp.get_json()
    barcodes = [item["barcode"] for item in data["items"]]
    assert "0000000000001" in barcodes


def test_search_pagination(client):
    resp = client.get("/api/products/search?page=1&page_size=1")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] >= 2
    assert len(data["items"]) == 1
    assert data["page"] == 1
    assert data["page_size"] == 1


def test_search_response_shape(client):
    resp = client.get("/api/products/search?q=Nutella")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "items" in data
    if data["items"]:
        item = data["items"][0]
        for key in ("barcode", "product_name", "brands", "nutrition_grade_fr",
                    "image_small_url", "categories"):
            assert key in item

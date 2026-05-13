from extensions import db


class Product(db.Model):
    __tablename__ = "products"

    barcode = db.Column(db.String(20), primary_key=True)
    product_name = db.Column(db.Text)
    brands = db.Column(db.Text)
    categories = db.Column(db.Text)
    countries = db.Column(db.Text)
    ingredients_text = db.Column(db.Text)
    allergens = db.Column(db.Text)
    traces = db.Column(db.Text)
    labels = db.Column(db.Text)
    nutrition_grade_fr = db.Column(db.String(1))
    nutrition_score_fr_100g = db.Column(db.Float)
    image_url = db.Column(db.Text)
    image_small_url = db.Column(db.Text)
    url = db.Column(db.Text)

    def to_summary(self):
        return {
            "barcode": self.barcode,
            "product_name": self.product_name,
            "brands": self.brands,
            "nutrition_grade_fr": self.nutrition_grade_fr,
            "image_small_url": self.image_small_url,
            "categories": self.categories,
        }

    def to_detail(self):
        allergen_list = [
            a.strip()
            for a in (self.allergens or "").split(",")
            if a.strip()
        ]
        ingredient_count = len([
            i for i in (self.ingredients_text or "").split(",")
            if i.strip()
        ])
        return {
            "barcode": self.barcode,
            "product_name": self.product_name,
            "brands": self.brands,
            "categories": self.categories,
            "countries": self.countries,
            "ingredients_text": self.ingredients_text,
            "allergens": self.allergens,
            "allergen_list": allergen_list,
            "ingredient_count": ingredient_count,
            "traces": self.traces,
            "labels": self.labels,
            "nutrition_grade_fr": self.nutrition_grade_fr,
            "nutrition_score_fr_100g": self.nutrition_score_fr_100g,
            "image_url": self.image_url,
            "image_small_url": self.image_small_url,
            "url": self.url,
        }

# backend/commands.py
import click
import pandas as pd
from extensions import db
from models.product import Product


def register_commands(app):
    @app.cli.command("import-tsv")
    @click.argument("path", default="data/en.openfoodfacts.org.products.tsv")
    def import_tsv(path):
        """Import OFF TSV dump into the products table. Skips if already populated."""
        if db.session.execute(db.select(Product)).first() is not None:
            click.echo("Products table already populated. Skipping import.")
            return

        col_map = {
            "code": "barcode",
            "product_name": "product_name",
            "brands": "brands",
            "categories": "categories",
            "countries": "countries",
            "ingredients_text": "ingredients_text",
            "allergens": "allergens",
            "traces": "traces",
            "labels": "labels",
            "nutrition_grade_fr": "nutrition_grade_fr",
            "nutrition-score-fr_100g": "nutrition_score_fr_100g",
            "image_url": "image_url",
            "image_small_url": "image_small_url",
            "url": "url",
        }

        total_imported = 0
        chunk_size = 10_000

        for chunk in pd.read_csv(
            path, sep="\t", dtype=str, chunksize=chunk_size, low_memory=False
        ):
            available = {k: v for k, v in col_map.items() if k in chunk.columns}
            chunk = chunk[list(available.keys())].rename(columns=available)

            chunk = chunk.dropna(subset=["barcode"])
            chunk = chunk[chunk["barcode"].str.strip() != ""]
            chunk = chunk[chunk["barcode"].str.len() <= 20]

            chunk["nutrition_score_fr_100g"] = pd.to_numeric(
                chunk.get("nutrition_score_fr_100g"), errors="coerce"
            )

            if "nutrition_grade_fr" in chunk.columns:
                chunk["nutrition_grade_fr"] = chunk["nutrition_grade_fr"].str[:1]

            records = chunk.where(pd.notna(chunk), None).to_dict(orient="records")
            db.session.bulk_insert_mappings(Product, records)
            db.session.commit()
            total_imported += len(records)
            click.echo(f"Imported {total_imported} products...")

        click.echo(f"Done. Total: {total_imported} products.")

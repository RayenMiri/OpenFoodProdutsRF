from flask import Flask, jsonify, request
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.get("/api/health")
    def health_check():
        return jsonify(status="ok", service="off-dashboard-api")

    @app.get("/api/products/search")
    def search_products():
        query = request.args.get("q", "").strip()
        page = max(int(request.args.get("page", 1)), 1)
        return jsonify(query=query, page=page, total=0, items=[])

    @app.get("/api/products/<barcode>")
    def get_product(barcode):
        return jsonify(barcode=barcode, found=False, product=None)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
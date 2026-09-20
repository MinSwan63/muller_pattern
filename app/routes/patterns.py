from flask import Blueprint, render_template, request, jsonify, session
from app.calculations import get_pattern, list_patterns
from app.services.measurement_service import normalize_measurements, denormalize_results
from app.models import Client, Calculation
from app import db

patterns_bp = Blueprint("patterns", __name__)


@patterns_bp.route("/")
def index():
    return render_template("patterns.html", patterns=list_patterns())


@patterns_bp.route("/<code>", methods=["GET", "POST"])
def calculate(code):
    pattern = get_pattern(code)
    if not pattern:
        return render_template("errors/404.html"), 404

    clients = Client.query.order_by(Client.name).all()
    errors = []
    results = []
    form_data = {}
    selected_client_id = None
    saved_calc_id = None

    if request.method == "POST":
        action = request.form.get("action", "calculate")
        unit = session.get("unit", "cm")
        selected_client_id = request.form.get("client_id") or None

        for field in pattern.measurements:
            form_data[field.key] = request.form.get(field.key, "").strip()

        errors = pattern.validate(form_data)

        if not errors:
            try:
                normalized = normalize_measurements(form_data, unit)
                raw_results = pattern.calculate(normalized)
                results = denormalize_results(raw_results, unit)

                if action == "save":
                    if not selected_client_id:
                        errors.append("برای ذخیره محاسبه، ابتدا یک مشتری انتخاب کنید.")
                    else:
                        calc = Calculation(
                            client_id=int(selected_client_id),
                            pattern=pattern.code,
                            unit=unit,
                        )
                        calc.measurements = {
                            k: float(v) for k, v in form_data.items() if v
                        }
                        calc.results = {
                            r.name: {
                                "value": r.value,
                                "unit": r.unit,
                                "description": r.description,
                            }
                            for r in results
                        }
                        db.session.add(calc)
                        db.session.commit()
                        saved_calc_id = calc.id
                        session["flash_success"] = "محاسبه با موفقیت ذخیره شد."
            except Exception as e:
                errors.append("خطایی در انجام محاسبه رخ داد. لطفاً دوباره تلاش کنید.")
                print("Calculation error:", e)

    return render_template(
        "calculate.html",
        pattern=pattern,
        clients=clients,
        errors=errors,
        results=results,
        form_data=form_data,
        selected_client_id=selected_client_id,
        saved_calc_id=saved_calc_id,
    )


@patterns_bp.route("/<code>/client-measurements/<int:client_id>")
def client_measurements(code, client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify(client.latest_measurements())

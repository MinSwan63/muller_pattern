from flask import Blueprint, render_template, request, session, redirect, url_for

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["theme"] = request.form.get("theme", "light")
        session["unit"] = request.form.get("unit", "cm")
        session["flash_success"] = "تنظیمات ذخیره شد."
        return redirect(url_for("settings.index"))

    return render_template(
        "settings.html",
        theme=session.get("theme", "light"),
        unit=session.get("unit", "cm"),
    )

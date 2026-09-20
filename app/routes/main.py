from flask import Blueprint, render_template
from app.calculations import list_patterns

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("home.html", patterns=list_patterns())


@main_bp.route("/about")
def about():
    return render_template("about.html")

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models import Client
from app import db

clients_bp = Blueprint("clients", __name__)


@clients_bp.route("/")
def index():
    clients = Client.query.order_by(Client.created_at.desc()).all()
    return render_template("clients.html", clients=clients)


@clients_bp.route("/create", methods=["POST"])
def create():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    notes = request.form.get("notes", "").strip()

    if not name:
        return jsonify({"error": "نام مشتری الزامی است."}), 400

    client = Client(name=name, phone=phone or None, notes=notes or None)
    db.session.add(client)
    db.session.commit()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"success": True, "client": client.to_dict()})

    return redirect(url_for("clients.index"))


@clients_bp.route("/<int:client_id>")
def detail(client_id):
    client = Client.query.get_or_404(client_id)
    return render_template("client_detail.html", client=client)


@clients_bp.route("/<int:client_id>/edit", methods=["POST"])
def edit(client_id):
    client = Client.query.get_or_404(client_id)
    client.name = request.form.get("name", "").strip() or client.name
    client.phone = request.form.get("phone", "").strip() or None
    client.notes = request.form.get("notes", "").strip() or None
    db.session.commit()
    return redirect(url_for("clients.detail", client_id=client.id))


@clients_bp.route("/<int:client_id>/delete", methods=["POST"])
def delete(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for("clients.index"))

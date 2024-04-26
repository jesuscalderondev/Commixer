from flask import Blueprint, render_template, redirect, jsonify, request, url_for
from flask import session as cookies

from database import *
from functions import passwordVerify, requiredSession, jwt_required

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.route("/login", methods=["GET"])
def login():
    return render_template("index.html")


@admin.route("/dashboard")
#@requiredSession
def dashboard():
    return render_template("dashboard.html")

@admin.route("/addProduct", methods = ['GET', 'POST'])
def addProduct():
    if request.method == "POST":
        data = request.get_json()
    return render_template("addProduct.html")
from flask import Blueprint, render_template, flash, request, redirect, url_for
from app import db

bp = Blueprint("facultad", __name__)

@bp.route("/facultad")
def indexFacultad():
    return render_template('administracion/facultad/index.html')
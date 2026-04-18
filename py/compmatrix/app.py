from flask import Flask, render_template, request
from sqlalchemy import create_engine, func, and_
from sqlalchemy.orm import sessionmaker, aliased
from .models import *

engine = create_engine("sqlite:///../../data.db")
Session = sessionmaker(bind=engine)

app = Flask(__name__)

@app.route("/")
def index():
    session = Session()
    sdks = session.query(SDK).all()
    return render_template(
        "index.html",
        available_sdks=sdks,
    )

@app.route("/matrix")
def matrix():
    session = Session()

    selected = request.args.getlist("selected_sdks")
    selected_sdk_ids = list(map(int, selected)) if selected else []

    sdks = session.query(SDK).all()
    selected_sdks = [sdk for sdk in sdks if sdk.id in selected_sdk_ids]

    matrix = {}
    norm = {}

    if selected_sdk_ids:
        matrix = compute_matrix(session, selected_sdk_ids)
        norm = normalize_matrix(matrix, selected_sdk_ids)

    return render_template(
        "matrix.html",
        available_sdks=sdks,
        selected=selected_sdks,
        matrix=matrix,
        norm=norm
    )

def compute_matrix(session, sdk_ids):
    a1 = aliased(AppSDK)
    a2 = aliased(AppSDK)

    rows = (
        session.query(
            a1.sdk_id.label("sdk_a"),
            a2.sdk_id.label("sdk_b"),
            func.count().label("count")
        )
        .filter(
            a1.app_id == a2.app_id,
            a1.installed == True,
            a2.installed == True,
            a1.sdk_id.in_(sdk_ids),
            a2.sdk_id.in_(sdk_ids),
        )
        .group_by(a1.sdk_id, a2.sdk_id)
        .all()
    )

    matrix = {(r.sdk_a, r.sdk_b): r.count for r in rows}
    return matrix

def normalize_matrix(matrix, sdk_ids):
    norm = {}
    for i in sdk_ids:
        row_sum = sum(matrix.get((i, j), 0) for j in sdk_ids)
        for j in sdk_ids:
            v = matrix.get((i, j), 0)
            norm[(i, j)] = v / row_sum if row_sum else 0
    return norm

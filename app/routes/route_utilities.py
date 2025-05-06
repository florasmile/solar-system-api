from flask import abort, make_response
from ..db import db


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        invalid = {"message": f"{cls.__name__} id {model_id} is invalid."}
        abort(make_response(invalid, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        not_found = {"message": f"{cls.__name__} id {model_id} not found."}
        abort(make_response(not_found, 404))
    return model


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError:
        response = {"message": f"missing {cls.__name__} information."}
        abort(make_response(response, 400))
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

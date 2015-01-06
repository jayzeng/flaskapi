from flask import jsonify, request
from . import api
from .. import db
from flask_cors import cross_origin
from ..models import Developer

@api.route('/signup/developer', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
def signup_developer():
    """
        @TOOD perform validations
    """
    json_req = request.get_json()['developer']

    new_developer = Developer(**json_req)

    db.session.add(new_developer)
    db.session.commit()

    return jsonify(developer=new_developer.serialize())

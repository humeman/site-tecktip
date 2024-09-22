from quart import Blueprint, request
import api
from api.data import Tip, Image, Submission

import time
import uuid

auth_blueprint = Blueprint("auth_page", __name__)

@auth_blueprint.route("/admin/auth", methods = ["GET"])
async def test_key():
    try:
        key = await api.main.authenticate(request)
    except api.main.AuthenticationFailure as e:
        return e.error_tuple
    
    return {
        "success": True
    }
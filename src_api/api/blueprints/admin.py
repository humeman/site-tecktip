from quart import Blueprint, request
import api
from api.data import Tip, Image, Submission

import time
import uuid

admin_blueprint = Blueprint("admin_page", __name__)

@admin_blueprint.route("/auth", methods = ["GET"])
async def test_key():
    
    err = await api.main.authenticate(request)
    
    if err: 
        return err
    
    return {
        "success": True
    }
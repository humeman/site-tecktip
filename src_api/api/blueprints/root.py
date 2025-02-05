from quart import Blueprint, request
import api
from api.data import Tip, Image, Submission

import time
import uuid
import os
import base64

root_blueprint = Blueprint("root_page", __name__)
rate_limits = {}

banned_words = [base64.b64decode(x).decode().strip() for x in ["ZnVjawo=", "c2hpdAo=", "Yml0Y2gK", "cmVwZW50Cg==", "YXNzCg=="]]
    

image_url = os.getenv("IMAGE_URL")
if image_url is None:
    raise RuntimeError("The IMAGE_URL env var must be set for the root blueprint to work.")

@root_blueprint.route("/", methods = ["GET"])
async def random_tip():
    tip = await api.main.db.random(Tip)
    if tip is None:
        return {
            "success": False,
            "reason": "no tips :("
        }, 404

    if request.content_type == "application/json":
        return tip.as_dict()
    
    else:
        return tip.tip

@root_blueprint.route("/nice", methods = ["GET"])
async def random_nice_tip():
    tip = None
    while tip is None:
        tip = await api.main.db.random(Tip)
        if tip is None:
            return {
                "success": False,
                "reason": "no tips :("
            }, 404
        
        for banned_word in banned_words:
            if banned_word.lower() in tip.tip.lower():
                tip = None

    if request.content_type == "application/json":
        return tip.as_dict()
    
    else:
        return tip.tip

@root_blueprint.route("/img", methods = ["GET"])
async def random_image():
    img = await api.main.db.random(Image)
    if img is None:
        return {
            "success": False,
            "reason": "no images :("
        }, 404

    if request.content_type == "application/json":
        return {
            **img.as_dict(),
            "url": f"{image_url}/{img.file}"
        }
    
    else:
        return f"{image_url}/{img.file}"

@root_blueprint.route("/submit", methods = ["POST"])
async def submit_tip():
    args = await request.json
    
    if args is None:
        return {
            "success": False,
            "reason": "no args passed"
        }, 400
    
    tip = args.get("tip")
    if type(tip) != str:
        return {
            "success": False,
            "reason": "tip must be a str"
        }, 400
    
    tip = tip.strip()
    if len(tip) > 128 or len(tip) < 3:
        return {
            "success": False,
            "reason": "tip must be between 3 and 128 characters"
        }, 400
    
    name = args.get("name")
    if type(name) != str:
        return {
            "success": False,
            "reason": "name must be a str"
        }, 400
    
    name = name.strip()
    if len(name) > 20 or len(name) < 3:
        return {
            "success": False,
            "reason": "name must be between 3 and 20 characters"
        }, 400
    
    addr = str(request.remote_addr)
    limit = rate_limits.get(addr)
    if limit is not None and limit >= time.time() - 60:
        return {
            "success": False,
            "reason": "tips can only be submitted once every 60 seconds"
        }, 429
    
    rate_limits[addr] = time.time()

    _id = str(uuid.uuid4())
    await api.main.db.upsert(
        Submission(
            id = _id,
            created = time.time(),
            ip = addr,
            by = name,
            tip = tip
        )
    )

    return {
        "success": True,
        "id": _id
    }


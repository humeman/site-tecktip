from quart import Blueprint, request
from .. import db
from ..io.database import Tip, Image, Submission

import time
import uuid

root_page = Blueprint("root_page", __name__)
rate_limits = {}

@root_page.route("/", methods = ["GET"])
async def random_tip():
    tip = await db.random(Tip)
    if request.content_type == "application/json":
        return tip.as_dict()
    
    else:
        return tip.tip

@root_page.route("/img", methods = ["GET"])
async def random_image():
    return (await db.random(Image)).file

@root_page.route("/submit", methods = ["POST"])
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
    
    name = args.get("by")
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
    await db.upsert(
        Submission(
            id = _id,
            at = time.time(),
            ip = addr,
            by = name,
            tip = tip
        )
    )

    return {
        "success": True,
        "id": _id
    }


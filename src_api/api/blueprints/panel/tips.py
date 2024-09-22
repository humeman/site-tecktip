from quart import Blueprint, request
import api
from api.data import Tip, Image, Submission

import time
import uuid

tips_blueprint = Blueprint("tips_page", __name__)

def validate_tip(tip: str):
    if type(tip) != str:
        raise ValueError("tip must be a str")
    
    tip = tip.strip()
    if len(tip) > 128 or len(tip) < 3:
        raise ValueError("tip must be between 3 and 128 characters")

def validate_name(name: str):
    if type(name) != str:
        raise ValueError("by must be a str")
    
    name = name.strip()
    if len(name) > 20 or len(name) < 3:
        raise ValueError("by must be between 3 and 20 characters")

def json_to_tip(data: str) -> api.data.Tip:
    tip = data.get("tip")
    validate_tip(tip)
    
    name = data.get("by")
    validate_name(name)
    
    return api.data.Tip(
        id = uuid.uuid4(),
        by = name,
        tip = tip,
        created = int(time.time())
    )

@tips_blueprint.route("/admin/tips", methods = ["GET"])
async def list_tips(page: int = 0):
    try:
        key = await api.main.authenticate(request)
    except api.main.AuthenticationFailure as e:
        return e.error_tuple
    
    page_str = request.args.get("page")
    if page_str is None:
        page = 0
    else:
        try:
            page = int(page_str)
        
        except Exception as e:
            return {
                "success": False,
                "reason": "page must be an int"
            }, 400
    
    
    tips = [x.as_dict() for x in await api.main.db.list_paginated(api.data.Tip, api.data.Tip.created, page)]
    
    return {
        "success": True,
        "data": {
            "page": page,
            "tips": tips
        }
    }
    
@tips_blueprint.route("/admin/tips/<tip_id>", methods = ["GET"])
async def get_tip(tip_id: str):
    try:
        key = await api.main.authenticate(request)
    except api.main.AuthenticationFailure as e:
        return e.error_tuple
    
    tip = await api.main.db.get(api.data.Tip, api.data.Tip.id == tip_id)
    
    if tip is None:
        return {
            "success": False,
            "reason": f"No tip with ID '{tip_id}'"
        }, 400
    
    return {
        "success": True,
        "data": {
            "tip": tip.as_dict()
        }
    }
    
@tips_blueprint.route("/admin/tips", methods = ["POST"])
async def new_tip():
    try:
        key = await api.main.authenticate(request)
    except api.main.AuthenticationFailure as e:
        return e.error_tuple
        
    data = await request.json
    if data is None:
        return {
            "success": False,
            "reason": "This route requires a JSON body"
        }, 400
    
    try:
        tip = json_to_tip(data)
        
    except ValueError as e:
        return {
            "success": False,
            "reason": e.args[0]
        }, 400

    await api.main.db.upsert(tip)
    await api.main.audit(key, f"created tip {tip.id}\ntip: {tip.tip}\nby: {tip.by}")
    
    return {
        "success": True,
        "data": {
            "tip": tip.as_dict()
        }
    }
    
@tips_blueprint.route("/admin/tips/<tip_id>", methods = ["PUT"])
async def edit_tip(tip_id: str):
    try:
        key = await api.main.authenticate(request)
    except api.main.AuthenticationFailure as e:
        return e.error_tuple
    
    tip = await api.main.db.get(api.data.Tip, api.data.Tip.id == tip_id)
    
    if tip is None:
        return {
            "success": False,
            "reason": f"No tip with ID '{tip_id}'"
        }, 400
        
    data = await request.json
    if data is None:
        return {
            "success": False,
            "reason": "This route requires a JSON body"
        }, 400
    
    tip_before = None
    by_before = None
    try:
        if "tip" in data:
            validate_tip(data["tip"])
            tip_before = tip.tip
            tip.tip = data["tip"]
            
        if "by" in data:
            validate_name(data["by"])
            by_before = tip.by
            tip.by = data["by"]
            
    except ValueError as e:
        return {
            "success": False,
            "reason": e.args[0]
        }, 400
        
    await api.main.db.upsert(tip)
    await api.main.audit(key, f"edited tip {tip.id}\ntip before: {tip_before or 'not modified'}\nby before: {by_before or 'not modified'}\ntip now: {tip.tip}\nby now: {tip.by}")
    
    return {
        "success": True,
        "data": {
            "tip": tip.as_dict()
        }
    }
    
@tips_blueprint.route("/admin/tips/<tip_id>", methods = ["DELETE"])
async def delete_tip(tip_id: str):
    try:
        key = await api.main.authenticate(request)
    except api.main.AuthenticationFailure as e:
        return e.error_tuple
    
    tip = await api.main.db.get(api.data.Tip, api.data.Tip.id == tip_id)
    
    if tip is None:
        return {
            "success": False,
            "reason": f"No tip with ID '{tip_id}'"
        }, 400
    
    await api.main.db.delete(tip)
    await api.main.audit(key, f"deleted tip {tip.id}\ntip: {tip.tip}\nby: {tip.by}")
    
    return {
        "success": True,
        "data": {
            "tip": tip.as_dict()
        }
    }
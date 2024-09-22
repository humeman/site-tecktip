from quart import Blueprint, request
import sqlalchemy
import api
from api.data import Tip, Image, Submission

import time
import uuid

audit_blueprint = Blueprint("audit_page", __name__)

@audit_blueprint.route("/admin/audit", methods = ["GET"])
async def list_audit(page: int = 0):
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
    
    audits = [
        {
            "id": x[0].id,
            "user_alias": f"deleted account {x[0].user_id}" if x[1] is None else x[1].alias,
            "created": x[0].created,
            "action": x[0].action
        } for x in (await api.main.db.arbitrary(
            sqlalchemy.select(api.data.AuditLog, api.data.Key).join(api.data.Key, api.data.Key.id == api.data.AuditLog.user_id, isouter = True).order_by(api.data.AuditLog.created.desc()).offset(page * 50).limit(50))
        ).all()
    ]
    
    return {
        "success": True,
        "data": {
            "page": page,
            "audits": audits
        }
    }
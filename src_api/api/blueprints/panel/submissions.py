from quart import Blueprint, request
import api
from api.data import Tip, Image, Submission
from .tips import validate_name, validate_tip

import time
import uuid

submissions_blueprint = Blueprint("submissions_page", __name__)

@submissions_blueprint.route("/admin/submissions", methods = ["GET"])
async def list_submissions(page: int = 0):
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
    
    
    submissions = [x.as_dict() for x in await api.main.db.list_paginated(api.data.Submission, api.data.Submission.created, page)]
    
    return {
        "success": True,
        "data": {
            "page": page,
            "submissions": submissions
        }
    }
    
@submissions_blueprint.route("/admin/submissions/<submission_id>", methods = ["GET"])
async def get_submission(submission_id: str):
    try:
        key = await api.main.authenticate(request)
    except api.main.AuthenticationFailure as e:
        return e.error_tuple
    
    submission = await api.main.db.get(api.data.Submission, api.data.Submission.id == submission_id)
    
    if submission is None:
        return {
            "success": False,
            "reason": f"No submission with ID '{submission_id}'"
        }, 400
    
    return {
        "success": True,
        "data": {
            "submission": submission.as_dict()
        }
    }
    
@submissions_blueprint.route("/admin/submissions/<submission_id>", methods = ["PUT"])
async def confirm_submission(submission_id: str):
    try:
        key = await api.main.authenticate(request)
    except api.main.AuthenticationFailure as e:
        return e.error_tuple
    
    submission = await api.main.db.get(api.data.Submission, api.data.Submission.id == submission_id)
    
    if submission is None:
        return {
            "success": False,
            "reason": f"No submission with ID '{submission_id}'"
        }, 400
        
    tip = submission.tip
    by = submission.by
    
    data = await request.json
    overrode_tip = None
    overrode_by = None
    if data is not None:
        if "tip" in data:
            overrode_tip = tip
            tip = data["tip"]
            
        if "by" in data:
            overrode_by = by
            by = data["by"]
    
    try:
        validate_tip(tip)
        validate_name(by)
            
    except ValueError as e:
        return {
            "success": False,
            "reason": e.args[0]
        }, 400
        
    tip = api.data.Tip(
        id = uuid.uuid4(),
        tip = tip,
        by = by,
        created = submission.created
    )
        
    await api.main.db.upsert(tip)
    await api.main.db.delete(submission)
    await api.main.audit(key, f"confirmed submission {submission_id}\ntip: {tip}\nby: {by}\nip: {submission.ip}\noverrode tip: {overrode_tip or 'no'}\noverrode by: {overrode_by or 'no'}")
    
    return {
        "success": True,
        "data": {
            "tip": tip.as_dict()
        }
    }
    
@submissions_blueprint.route("/admin/submissions/<submission_id>", methods = ["DELETE"])
async def delete_submission(submission_id: str):
    try:
        key = await api.main.authenticate(request)
    except api.main.AuthenticationFailure as e:
        return e.error_tuple
    
    submission = await api.main.db.get(api.data.Submission, api.data.Submission.id == submission_id)
    
    if submission is None:
        return {
            "success": False,
            "reason": f"No submission with ID '{submission_id}'"
        }, 400
    
    await api.main.db.delete(submission)
    await api.main.audit(key, f"deleted submission {submission_id}\ntip: {submission.tip}\nby: {submission.by}\nip: {submission.ip}")
    
    return {
        "success": True,
        "data": {
            "submission": submission.as_dict()
        }
    }
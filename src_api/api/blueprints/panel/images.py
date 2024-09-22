from quart import Blueprint, request
import api
from api.data import Tip, Image, Submission

import time
import aiofiles
import magic
import uuid
import os

images_blueprint = Blueprint("images_page", __name__)
allowable_mime_types = {
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/gif": "gif"
}
path_prefix = os.getenv("IMAGE_FOLDER")
if path_prefix is None:
    raise RuntimeError("The IMAGE_FOLDER env var must be set for the images blueprint to work.")
image_url = os.getenv("IMAGE_URL")
if image_url is None:
    raise RuntimeError("The IMAGE_URL env var must be set for the images blueprint to work.")

@images_blueprint.route("/admin/images", methods = ["GET"])
async def list_images(page: int = 0):
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
    
    
    images = [
        {
            **x.as_dict(),
            "url": f"{image_url}/{x.file}"
        } for x in await api.main.db.list_paginated(api.data.Image, api.data.Image.created, page)
    ]
    
    return {
        "success": True,
        "data": {
            "page": page,
            "images": images
        }
    }
    
@images_blueprint.route("/admin/images/<image_id>", methods = ["GET"])
async def get_image(image_id: str):
    try:
        key = await api.main.authenticate(request)
    except api.main.AuthenticationFailure as e:
        return e.error_tuple
    
    image = await api.main.db.get(api.data.Image, api.data.Image.id == image_id)
    
    if image is None:
        return {
            "success": False,
            "reason": f"No image with ID '{image_id}'"
        }, 400
    
    return {
        "success": True,
        "data": {
            "image": {
                **image.as_dict(),
                "url": f"{image_url}/{image.file}"
            }
        }
    }
    
@images_blueprint.route("/admin/images", methods = ["POST"])
async def new_image():
    try:
        key = await api.main.authenticate(request)
    except api.main.AuthenticationFailure as e:
        return e.error_tuple
    
    files = await request.files
    if "file" not in files:
        return {
            "success": False,
            "reason": "Expected a file under 'file'"
        }, 400
    
    file = files["file"]
    if file.filename.strip() == "":
        return {
            "success": False,
            "reason": "File was not provided"
        }, 400
        
    # Try to identify MIME type
    mimetype = magic.from_buffer(file.read(2048), mime = True)
    
    if mimetype not in allowable_mime_types:
        return {
            "success": False,
            "reason": "Only PNG, JPEG, or GIF images are allowed"
        }, 400
    
    imgid = uuid.uuid4()
    filename = f"{imgid}.{allowable_mime_types[mimetype]}"
    file.seek(0)
    await file.save(f"{path_prefix}/{filename}")
    
    # Write out to db
    image = api.data.Image(
        id = imgid,
        created = int(time.time()),
        file = filename
    )
    await api.main.db.upsert(image)
    await api.main.audit(key, f"created image {imgid} linking to {filename}")
    
    return {
        "success": True, 
        "data": {
            "image": {
                **image.as_dict(),
                "url": f"{image_url}/{image.file}"
            }
        }
    }
    
@images_blueprint.route("/admin/images/<image_id>", methods = ["DELETE"])
async def delete_image(image_id: str):
    try:
        key = await api.main.authenticate(request)
    except api.main.AuthenticationFailure as e:
        return e.error_tuple
    
    image = await api.main.db.get(api.data.Image, api.data.Image.id == image_id)
    
    if image is None:
        return {
            "success": False,
            "reason": f"No image with ID '{image_id}'"
        }, 400
    
    await api.main.db.delete(image)
    await api.main.audit(key, f"deleted image {image_id} which linked to {image.file}")
    
    return {
        "success": True,
        "data": {
            "image": {
                **image.as_dict(),
                "url": f"{image_url}/{image.file}"
            }
        }
    }
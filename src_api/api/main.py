import time
import api
import hypercorn
from quart import Quart
import hypercorn
from quart_cors import cors
import os
import traceback

config = None
app = None
db = None

auth_rate_limits = {}

async def authenticate(request):
    addr = str(request.remote_addr)
    limit = auth_rate_limits.get(addr)
    if limit is not None and limit >= time.time() - 5:
        return {
            "success": False,
            "reason": "You are being rate limited due to an authentication failure."
        }, 429
    
    key = request.headers.get("Authorization")
    
    if not key:
        auth_rate_limits[addr] = time.time()
        return {
            "success": False,
            "error": "You must be authenticated to use this method."
        }
    
    try:
        res = await db.get(api.data.Key, api.data.Key.val == key)
        
    except Exception as e:
        traceback.print_exc()
        auth_rate_limits[addr] = time.time()
        return {
            "success": False,
            "error": "Could not authenticate you."
        }
    
    if key is None:
        auth_rate_limits[addr] = time.time()
        return {
            "success": False,
            "error": "Could not authenticate you."
        }

async def start():
    global config
    config = hypercorn.config.Config.from_toml("config.toml")
    config.certfile = os.getenv("HYPERCORN_CERTFILE")
    config.keyfile = os.getenv("HYPERCORN_KEYFILE")
    config.bind = f"0.0.0.0:{os.getenv('PORT')}"
    global app
    app = Quart(__name__)
    app = cors(app, allow_origin = "*")
    global db
    db = api.data.Database()

    app.register_blueprint(api.blueprints.root_blueprint)
    app.register_blueprint(api.blueprints.admin_blueprint)
    
    async with db:
        await hypercorn.asyncio.serve(app, config)
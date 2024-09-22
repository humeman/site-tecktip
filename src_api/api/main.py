import time
import uuid
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

class AuthenticationFailure(RuntimeError):
    def __init__(self, res_data, res_status):
        super().__init__(self)
        self.error_tuple = res_data, res_status

async def authenticate(request) -> api.data.Key:
    addr = str(request.remote_addr)
    limit = auth_rate_limits.get(addr)
    if limit is not None and limit >= time.time() - 15:
       raise AuthenticationFailure({
            "success": False,
            "reason": "You are being rate limited due to an authentication failure."
        }, 429)
    
    key = request.headers.get("Authorization")
    
    if not key:
        auth_rate_limits[addr] = time.time()
        raise AuthenticationFailure({
            "success": False,
            "reason": "You must be authenticated to use this method."
        }, 400)
    
    try:
        res_key = await db.get(api.data.Key, api.data.Key.val == key)
        
    except Exception as e:
        traceback.print_exc()
        auth_rate_limits[addr] = time.time()
        raise AuthenticationFailure({
            "success": False,
            "reason": "Could not authenticate you."
        }, 401)
    
    if res_key is None:
        auth_rate_limits[addr] = time.time()
        raise AuthenticationFailure({
            "success": False,
            "reason": "Could not authenticate you."
        }, 401)
        
    return res_key

async def audit(key: api.data.Key, action: str):
    audit = api.data.AuditLog(
        id = uuid.uuid4(),
        user_id = key.id,
        created = int(time.time()),
        action = action
    )
    await db.upsert(audit)

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
    app.register_blueprint(api.blueprints.auth_blueprint)
    app.register_blueprint(api.blueprints.tips_blueprint)
    app.register_blueprint(api.blueprints.submissions_blueprint)
    app.register_blueprint(api.blueprints.images_blueprint)
    app.register_blueprint(api.blueprints.audit_blueprint)
    
    async with db:
        await hypercorn.asyncio.serve(app, config)
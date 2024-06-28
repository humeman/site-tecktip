import api
import hypercorn
from quart import Quart
import hypercorn
from quart_cors import cors

config = None
app = None
db = None


async def start():
    config = hypercorn.config.Config.from_toml("config.toml")
    app = Quart(__name__)
    app = cors(app, allow_origin = "*")
    db = api.data.Database()

    app.register_blueprint(api.blueprints.root_blueprint)
    
    async with db:
        await hypercorn.asyncio.serve(api.app, api.config)
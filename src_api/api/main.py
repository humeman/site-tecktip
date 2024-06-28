import api
import hypercorn
from quart import Quart
import hypercorn
from quart_cors import cors

config = None
app = None
db = None


async def start():
    global config
    config = hypercorn.config.Config.from_toml("config.toml")
    global app
    app = Quart(__name__)
    app = cors(app, allow_origin = "*")
    global db
    db = api.data.Database()

    app.register_blueprint(api.blueprints.root_blueprint)
    
    async with db:
        await hypercorn.asyncio.serve(app, config)
from quart import Quart
import hypercorn
from quart_cors import cors

from .io.database import Database


config = hypercorn.config.Config.from_toml("config.toml")
app = Quart(__name__)
app = cors(app, allow_origin = "*")
db = Database()

async def main():
    async with db:
        await hypercorn.asyncio.serve(app, config)

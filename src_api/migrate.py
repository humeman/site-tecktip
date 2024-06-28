import json
from api.data import Database, Tip, Image, LegacyKey

db = Database()

with open("tips.json", "r") as f:
    old_db = json.loads(f.read())

async def main():
    async with db:
        for tip in old_db["tips"].values():
            await db.upsert(Tip(id = tip["uuid"], tip = tip["tip"], by = tip["by"], created = tip["created"]))
        
        for key in old_db["keys"]:
            await db.upsert(LegacyKey(val = key))

        for image_id, image in old_db["images"].items():
            await db.upsert(Image(id = image_id, created = image["created"], file = image["file"]))

import asyncio
asyncio.new_event_loop().run_until_complete(main())
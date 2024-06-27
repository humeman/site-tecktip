from quart import Quart, request
import werkzeug
import asyncio
import hypercorn
import aiofiles
import json
import copy
import random
from quart_cors import cors
import time
import uuid
import aiofiles
import aiohttp
import traceback

config = hypercorn.config.Config.from_toml("config.toml")

settings = {
    "allow_origin": "*"
}

app = Quart(__name__)
app = cors(app, **settings)

db = {}

# Important things
async def load():
    async with aiofiles.open("tips.json", "r") as f:
        global db
        db = json.loads(await f.read())

async def write():
    async with aiofiles.open("tips.json", "w") as f:
        await f.write(json.dumps(db, indent = 4))

asyncio.get_event_loop().run_until_complete(load())

# Verify all things exist
default_db = {
    "tips": [],
    "keys": [
        "c264e756-3b85-462f-a38c-986357f32626",
        "7c9bfb2b-aa1a-4f10-80e9-a0fd533133c3", # not me
        "fb2ddcc0-8fdc-4587-94fe-0c27e918a1da" # JIMMY!
    ]
}

write_ = False
for key, default_value in default_db.items():
    if key not in db:
        db[key] = copy.copy(default_value)
        write_ = True

if write:
    asyncio.get_event_loop().run_until_complete(write())

@app.route("/", methods = ["GET"])
async def random_tip():
    if len(db["tips"]) == 0:
        return "error: no tips... is life even worth living anymore?"

    return db["tips"][random.choice(db["tip_ids"])]["tip"]

@app.route("/img", methods = ["GET"])
async def random_img():
    if len(db["images"]) == 0:
        return "https://tecktip.today/images/5c7179ad-ff59-4608-b817-b7778cf38efb.png"

    return db["images"][random.choice(db["image_ids"])]["file"]

async def authorize(
        args
    ):

    print(args)

    if type(args) not in [werkzeug.datastructures.ImmutableMultiDict, dict]:
        return {
            "success": False,
            "reason": "invald args"
        }

    #if request.remote_addr not in ["::1", "localhost", "127.0.0.1", "63.151.26.52", "199.188.116.50"]:
    #    return {
    #        "success": False,
    #        "reason": "invalid IP"
    #    }

    if not args.get("key"):
        return {
            "success": False,
            "reason": "no API key"
        }

    if args.get("key") not in db["keys"]:
        return {
            "success": False,
            "reason": "bad API key"
        }

    return False

@app.route("/new", methods = ["PUT"])
async def new_tip():
    args = await request.json

    err = await authorize(args)

    if err:
        return err

    tip = args.get("tip")

    if type(tip) != str:
        return {
            "success": False,
            "reason": "tip not a string"
        }

    if len(tip) > 128:
        return {
            "success": False,
            "reason": "tip too long (128 char max)"
        }

    by = args.get("by")

    if type(by) != str:
        return {
            "success": False,
            "reason": "by is not a string"
        }

    if len(by) > 20 or len(by) < 3:
        return {
            "success": False,
            "reason": "by must be between 3 and 20 characters"
        }

    uid = str(uuid.uuid4())

    db["tips"][uid] = {
        "tip": tip,
        "by": by,
        "created": int(time.time()),
        "uuid": uid
    }
    db["tip_ids"].append(uid)

    await write()

    return {
        "success": True,
        "uuid": uid
    }

@app.route("/edit", methods = ["PUT"])
async def edit_tip():
    args = await request.json

    err = await authorize(args)

    if err:
        return err

    uid = args.get("uuid")

    if type(uid) != str:
        return {
            "success": False,
            "reason": "uuid is not a str"
        }

    if uid not in db["tips"]:
        return {
            "success": False,
            "reason": "uuid doesn't exist"
        }

    changes = {}

    if "tip" in args:
        tip = args.get("tip")

        if type(tip) != str:
            return {
                "success": False,
                "reason": "tip not a string"
            }

        if len(tip) > 128:
            return {
                "success": False,
                "reason": "tip too long (128 char max)"
            }

        changes["tip"] = tip

    if "by" in args:
        by = args.get("by")

        if type(by) != str:
            return {
                "success": False,
                "reason": "by is not a string"
            }

        if len(by) > 20 or len(by) < 3:
            return {
                "success": False,
                "reason": "by must be between 3 and 20 characters"
            }
        
        changes["by"] = by

    db["tips"][uid].update(
        changes
    )

    await write()

    return {
        "success": True,
        "uuid": uid,
        "tip": db["tips"][uid]
    }

@app.route("/kill", methods = ["PUT"])
async def kill_tip():
    args = await request.json

    err = await authorize(args)

    if err:
        return err

    uid = args.get("uuid")

    if type(uid) != str:
        return {
            "success": False,
            "reason": "uuid is not a str"
        }

    if uid not in db["tips"]:
        return {
            "success": False,
            "reason": "uuid doesn't exist"
        }

    del db["tip_ids"][db["tip_ids"].index(uid)]
    del db["tips"][uid]

    await write()

    return {
        "success": True,
        "uuid": uid
    }

@app.route("/get", methods = ["GET"])
async def get_tip():
    args = request.args

    err = await authorize(args)

    if err:
        return err

    uid = args.get("uuid")

    if type(uid) != str:
        return {
            "success": False,
            "reason": "uuid is not a str"
        }

    if uid not in db["tips"]:
        return {
            "success": False,
            "reason": "uuid doesn't exist"
        }

    return {
        "success": True,
        "uuid": uid,
        "tip": db["tips"][uid]
    }

@app.route("/list", methods = ["GET"])
async def list_tip():
    args = request.args

    err = await authorize(args)

    if err:
        return err

    return {
        "success": True,
        "tips": db["tips"]
    }

@app.route("/pending", methods = ["GET"])
async def pending():
    args = request.args

    err = await authorize(args)

    if err:
        return err

    return {
        "success": True,
        "pending": db["submissions"]
    }

@app.route("/del_pending", methods = ["PUT"])
async def del_pending():
    args = await request.json

    err = await authorize(args)

    if err:
        return err

    uid = args.get("uuid")
    
    if type(uid) != str:
        return {
            "success": False,
            "reason": "uid must be a string"
        }

    if uid not in db["submissions"]:
        return {
            "success": False,
            "reason": "uid does not exist"
        }

    del db["submissions"][uid]

    await write()

    return {
        "success": True,
        "uuid": uid
    }

@app.route("/test_login", methods = ["PUT"])
async def test_login():
    args = await request.json

    err = await authorize(args)

    if err:
        return err

    return {
        "success": True
    }


@app.route("/pub/submit", methods = ["PUT"])
async def submit_tip():
    args = await request.json

    if args is None:
        return {
            "success": False,
            "reason": "no args passed"
        }


    tip = args.get("tip")

    if type(tip) != str:
        return {
            "success": False,
            "reason": "tip must be a str"
        }

    if len(tip) > 128 or len(tip) < 3:
        return {
            "success": False,
            "reason": "tip must be between 3 and 128 characters"
        }

    name = args.get("by")
    if type(name) != str:
        return {
            "success": False,
            "reason": "author must be a str"
        }

    if len(name) > 20 or len(tip) < 3:
        return {
            "success": False,
            "reason": "author must be between 3 and 20 characters"
        }

    # check ratelimit
    addr = str(request.remote_addr)
    if addr in db["ratelimits"]:
        if db["ratelimits"][addr] >= time.time() - 60:
            return {
                "success": False,
                "reason": "tips can only be submitted every 60 seconds"
            }

    db["ratelimits"][addr] = int(time.time())

    uid = str(uuid.uuid4())

    db["submissions"][uid] = {
        "tip": tip,
        "at": int(time.time()),
        "ip": addr,
        "by": name,
        "uuid": uid
    }

    return {
        "success": True,
        "uuid": uid
    }

@app.route("/img/list", methods = ["GET"])
async def list_img():
    args = request.args

    err = await authorize(args)

    if err:
        return err

    return {
        "success": True,
        "images": db["images"]
    }

@app.route("/img/add", methods = ["PUT"])
async def add_img():
    args = await request.json

    err = await authorize(args)

    if err:
        return err

    # Get image URL
    url = args.get("url")

    if type(url) != str:
        return {
            "success": False,
            "reason": "url is not a str"
        }

    # Generate a UUID
    uid = str(uuid.uuid4())

    # Grab extension from URL
    try:
        ext = url.split("&")[0].rsplit(".", 1)[-1].lower()

    except:
        return {
            "success": False,
            "reason": "no image extension found"
        }

    if ext not in ["png", "jpg", "jpeg", "gif"]:
        return {
            "success": False,
            "reason": f"extension '{ext}' invalid: need png, jpg, jpeg, gif"
        }

    # Queue for download
    asyncio.get_event_loop().create_task(
        wrap_download(
            uid,
            download_img(url, uid, ext)
        )
    )

    return {
        "success": True,
        "uuid": uid
    }

async def wrap_download(uid, coro):
    task = asyncio.get_event_loop().create_task(coro)

    # Check for 10s timeout
    await asyncio.sleep(10)

    if not task.done():
        db["img_status"][uid] = {
            "success": False,
            "reason": "timeout reached"
        }

        await write()

        try:
            await task.cancel()

        except:
            print("failed to cancel dl task")


async def download_img(url, uid, ext):
    try:
        async with aiohttp.ClientSession(
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11"
                }
            ) as session:

            async with session.get(url) as resp:
                if resp.status == 200:
                    if write:
                        filename = f"/home/camden/sites/tecktip.today/site/static/images/{uid}.{ext}"

                        async with aiofiles.open(filename, mode = "wb") as f:
                            await f.write(await resp.read())

                        # Save to DB
                        db["images"][uid] = {
                            "file": f"{uid}.{ext}",
                            "created": int(time.time())
                        }

                        db["image_ids"].append(uid)

                        db["img_status"][uid] = {
                            "success": True,
                            "name": f"{uid}.{ext}",
                            "uuid": uid
                        }

                        await write()

                else:
                    db["img_status"][uid] = {
                        "success": False,
                        "reason": f"non-200 status code: {resp.status}"
                    }

                    await write()

    except Exception as e:
        db["img_status"][uid] = {
            "success": False,
            "reason": f"exception: {type(e)}"
        }

        await write()

        traceback.print_exc()

@app.route("/img/kill", methods = ["PUT"])
async def kill_img():
    args = await request.json

    err = await authorize(args)

    if err:
        return err

    # Get image URL
    uid = args.get("uuid")

    if type(uid) != str:
        return {
            "success": False,
            "reason": "uuid is not a str"
        }

    # Delete from API
    # No need to purge files for now, we got lots of storage over here
    if uid not in db["images"]:
        return {
            "success": False,
            "reason": "uuid not in image list"
        }

    del db["images"][uid]
    del db["image_ids"][db["image_ids"].index(uid)]

    await write()

    return {
        "success": True,
        "uuid": uid
    }

@app.route("/img/check", methods = ["GET"])
async def check_img():
    args = request.args

    err = await authorize(args)

    if err:
        return err

    # Get image URL
    uid = args.get("uuid")

    if type(uid) != str:
        return {
            "success": False,
            "reason": "uid is not a str"
        }

    if uid not in db["img_status"]:
        return {
            "success": False,
            "waiting": True,
            "reason": "uid not in status list"
        }
    
    return db["img_status"][uid]

async def main():
    await hypercorn.asyncio.serve(app, config)

asyncio.get_event_loop().run_until_complete(main())

import json
import time
import aiofiles
from quart import Blueprint, request
import api
from api.data import Tip

import os
import openai

teckgpt_blueprint = Blueprint("teckgpt_page", __name__)

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise RuntimeError("The OPENAI_API_KEY env var must be set for the teckgpt blueprint to work.")
model = os.getenv("OPENAI_MODEL") or "gpt-4o"


openai_client = openai.AsyncOpenAI(
    api_key = api_key
)

default_instructions = """
Note that correct grammar is NOT to be used, and most words should be badly misspelled. 
Add characters like {}[],.<>/? in random places, within words or as punctuation. 
If you wish, tips don't have to make sense, and they can sometimes loosely contain an illogical technology joke.
Be sure to begin your message with a helpful greeting, for example "teck tip today!!!!" or "teck!!!,"
"""

prompt = """
Your goal is to write "teck tips". 
Whenever someone asks for a teck tip, respond using the format described below. 
%instructions%
Tips must be no longer than 128 characters.
Respond with only one teck tip per message from the user.
Do not duplicate tips you have seen previously.
Do not use any offensive language.
"""


rate_limits = {}

@teckgpt_blueprint.route("/admin/teckgpt", methods = ["GET"])
async def generate_tip():
    try:
        key = await api.main.authenticate(request)
    except api.main.AuthenticationFailure as e:
        return e.error_tuple
    
    addr = str(request.remote_addr)
    limit = rate_limits.get(addr)
    if limit is not None and limit >= time.time() - 5:
       return {
            "success": False,
            "reason": "You are being rate limited. TeckGPT is a technological marvel and also quite expensive, so you can only request a tip every 5 seconds."
        }, 429
       
    rate_limits[addr] = time.time()
    user_prompt = request.args.get("prompt")
    if user_prompt is not None and len(user_prompt) > 3:
        if len(user_prompt) > 1000:
            return {
                "success": False,
                "reason": "TeckGPT has refused your request because your demands are far too lengthy. Please fix this."
            }, 400
            
        messages = [
            {"role": "system", "content": prompt.replace("%instructions%", user_prompt)},
            {"role": "user", "content": "teck tip please"}
        ]
        
    else:
        messages = [
            {"role": "system", "content": prompt.replace("%instructions%", default_instructions)},
            {"role": "user", "content": "teck tip please"},
            {"role": "assistant", "content": (await api.main.db.random(Tip)).tip},
            {"role": "user", "content": "teck tip please"},
            {"role": "assistant", "content": (await api.main.db.random(Tip)).tip},
            {"role": "user", "content": "teck tip please"}
        ]
    
    response = await openai_client.chat.completions.create(
        model = model,
        messages = messages
    )
    
    return {
        "success": True,
        "data": {
            "tip": response.choices[0].message.content
        }
    }
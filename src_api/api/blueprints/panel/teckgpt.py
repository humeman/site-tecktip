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

prompt = """
Your goal is to write "teck tips". 
Whenever someone asks for a teck tip, respond using the format described below. 
Note that correct grammar is NOT to be used, and most words should be badly misspelled. 
Add characters like {}[],.<>/? in random places, within words or as punctuation. 
If you wish, tips don't have to make sense, and they can sometimes loosely contain an illogical technology joke.
Be sure to begin your message with a helpful greeting, for example "teck tip today!!!!" or "teck!!!,"
Tips must be no longer than 128 characters.
Respond with only one teck tip per message from the user.

Here are what tips can look like (where each tip is delimited by a newline). Don't directly copy tips, but make your own in a similar style.
Tech for now. did you have known that the majority of computer problem can be solved by simply turning the computler off?
tech tup tomorrow!!!!!!!< < !<,
tteck tip! tomorrow. evvevry every talk about chip shortage.. bro just ggo buy bag of chip at sotre i ddont underst hahaghg
teck,,, wat is that? raid0... sonds like vrius// dont you thin?
mery techmas.. ,your gift is 
teck tip today: if u maek game using unity... you will (ERROR: due to too many teck tips, we are now bankrupt. this tec
tech tip Today !!! you've Been lied to.. The Gaphics are missing because I consumed them all.,...,, I Hunger for TEch,,,,
tip
tech tuop today !!!!!!! <. 2,m3m justp[ put COmputer in my brain,,, i think in Tech
tech tip!!!! ! did you know that in 2013 there will be coputer the size of House . don't believe me? 
tech!!!!!!1 when the motherbord exlplodes it is usually not good
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
    
    response = await openai_client.chat.completions.create(
        model = model,
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "teck tip please"},
            {"role": "assistant", "content": (await api.main.db.random(Tip)).tip},
            {"role": "user", "content": "teck tip please"}
        ]
    )
    
    return {
        "success": True,
        "data": {
            "tip": response.choices[0].message.content
        }
    }
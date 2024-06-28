import api
import asyncio

if __name__ == "__main__":
    asyncio.new_event_loop().run_until_complete(api.main.start())
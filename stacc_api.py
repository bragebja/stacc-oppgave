import aiohttp
import asyncio

STACC_API_URL = "https://code-challenge.stacc.dev/api"

# Use STACC PEP API to lookup a single person by name
async def pep(name : str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{STACC_API_URL}/pep?name={name}") as response:

                return {"status" : 1, "description" : "success", "response" : await response.json()}
    except:
        return {"status" : 0, "description" : "Something went wrong", "response" : {}}


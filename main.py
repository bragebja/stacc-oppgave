from fastapi import FastAPI
from stacc_api import pep
from database import decrement_api_calls, get_remaining_api_calls, create_api_token

app = FastAPI()

@app.get("/api/pep")
async def router_pep(name : str, token : str):
    # Check if a token has more api calls. Decrement if it has.
    has_more_api_calls = await decrement_api_calls(token)
    if has_more_api_calls:
        pep_response = await pep(name)
        return pep_response
    else:
        return {"status" : 0, "description" : "Key has no remaining api calls or does not exist", "response" : {}}

@app.get("/api/remaining_api_calls")
async def router_remaining_api_calls(token :str):
    response = await get_remaining_api_calls(token)
    return response

@app.post("/api/api_token")
async def router_create_api_token():
    # Create a random api token with 100 api calls
    how_many_api_calls = 100
    response = await create_api_token(how_many_api_calls)
    return response



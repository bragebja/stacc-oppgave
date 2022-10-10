from fastapi import FastAPI
from stacc_api import pep
from database import decrement_api_calls

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
import asyncio
import aiomysql

## DB CONFIGS
HOST = "database-2.c2z77t0mvtlc.us-east-1.rds.amazonaws.com"
PORT = 3306
USER = "admin"
DB = "stacc_db"
PASSWORD = "MYSQL12345" # Should not be part of codebase ideally.

# Tries to decrease the remaining available api calls for a given token, if its greater than 0
# Returns True if success, or False if its not greather than 0 or if token does not exist
async def decrement_api_calls(token : str) -> bool:
    try:
        rows_affected = 0
        ## Connect to DB
        pool = await aiomysql.create_pool(host=HOST, port=PORT,
                                        user=USER, password=PASSWORD,
                                        db=DB, autocommit=True)
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Decrease remaining_api_calls by 1 that belongs to the token if it exists
                query = "UPDATE api_token SET remaining_api_calls = (remaining_api_calls - 1) WHERE token = %s AND remaining_api_calls > 0"
                rows_affected = await cur.execute(query, (token))

        pool.close()
        await pool.wait_closed()
        return count > 0
    # Return false if something unexpected happens, such as failing to connect, etc.
    except Exception as e:
        return False
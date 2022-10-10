import asyncio
import aiomysql
import pymysql
import secrets

## DB CONFIGS
HOST = "database-1eu.cobpbett9lnf.eu-west-2.rds.amazonaws.com" # Only available from AWS EC2 compute instance
#HOST = "database-2.c2z77t0mvtlc.us-east-1.rds.amazonaws.com"  # Publicly available
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

        return rows_affected > 0
    # Return false if something unexpected happens, such as failing to connect, etc.
    except Exception as e:
        return False
    finally:
        pool.close()
        await pool.wait_closed()


# Get how many more api / pep calls a token have remaining.
# Returns a dictionary with the format:
# {"status" : 1, "description" : "Success", "remaining_api_calls" : b9b09ebdf29f464s82e23269c535acbd}
# or alternatively {"status" : 0, "description" : "Token does not exist"} 
async def get_remaining_api_calls(token : str) -> dict:
    try:
        ## Connect to DB
        pool = await aiomysql.create_pool(host=HOST, port=PORT,
                                        user=USER, password=PASSWORD,
                                        db=DB, autocommit=True)
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get how many more api calls the token can do
                query = "SELECT remaining_api_calls FROM api_token WHERE token = %s"
                rows_affected = await cur.execute(query, (token))
                if not rows_affected:
                    print("Not affected")
                    return {"status" : 0, "description" : "Token does not exist"}
                else:
                    remaining_api_calls = await cur.fetchone()
                    return {"status" : 1, "description" : "Success", "remaining_api_calls" : remaining_api_calls[0]}

    # If something unexpected happens, such as failing to connect, etc.
    except Exception as e:
        print(e)
        return {"status" : 0, "description" : "Something went wrong"}
    finally:
        pool.close()
        await pool.wait_closed()

# Creates a random token that has "how_many_calls" available api calls.
# It creates a record in the sql db and returns the random token if it was a success
# Example: {"status" : 1, "description" : "Success", "token" : b9b09ebdf29f464s82e23269c535acbd}
# Example if not success: {"status" : 0, "description" : "Something went wrong"}
async def create_api_token(how_many_calls : int) -> dict:
    # Create secret token of 16 bytes / 128 bits.
    token = secrets.token_hex(16)
    try:
        ## Connect to DB
        pool = await aiomysql.create_pool(host=HOST, port=PORT,
                                        user=USER, password=PASSWORD,
                                        db=DB, autocommit=True)
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Create api token consisting of a token and how many remaining calls it can do
                query = "INSERT INTO api_token (token, remaining_api_calls) VALUES (%s, %s)"
                await cur.execute(query, (token, how_many_calls))
                return {"status" : 1, "description" : "Success", "token" : token}

    # If something unexpected happens, such as failing to connect, duplicate entry, etc.
    except pymysql.err.IntegrityError:
        return {"status" : 0, "description" : "Token already exists"}
    except Exception:
        return {"status" : 0, "description" : "Something went wrong"}
    finally:
        pool.close()
        await pool.wait_closed()

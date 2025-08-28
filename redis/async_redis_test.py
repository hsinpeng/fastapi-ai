import asyncio, argparse
import redis.asyncio as redis

async def main():
    print(f"Redis Async Test...")

    # Create parser
    parse = argparse.ArgumentParser(
        description="This is my parser"
    )
    # Add argument(s) to parser
    parse.add_argument("-o", dest="run_option", default=0, type=int)
    # Parsing arguments
    args = parse.parse_args()
    # get values
    run_option:int = args.run_option

    # check if use connection pool
    if run_option > 2:
        try:
            pool = redis.ConnectionPool(
                host='localhost',
                port=6379,
                db=0,
                decode_responses=False #True
            )
            print("✅ Redis connection pool created successfully.")
        except redis.exceptions.ConnectionError as e:
            print(f"❌ Could not connect to Redis: {e}")
            # Exit if connection fails, as the rest of the script won't work.
            exit()

    match run_option:
        case 0:
            print("Hello from Redis-Async-Test! Please check how to use me by the '-h' argument.")

        case 1:
            print("----- Async Call -----")
            try:
                # Establish an asynchronous connection to Redis.
                # It's recommended to create a connection pool for production.
                r = redis.Redis(host='localhost', port=6379, db=0)

                # 1. Set a value for a key asynchronously
                await r.set('async_key', 'Hello from redis.asyncio!')
                print("Set 'async_key' to 'Hello from redis.asyncio!'")

                # 2. Get the value of the key
                # The result is a bytes object, so we decode it.
                value = await r.get('async_key')
                if value:
                    print(f"Got the value for 'async_key': {value.decode('utf-8')}")

                # 3. Check if a key exists
                key_exists = await r.exists('async_key')
                print(f"Does 'async_key' exist? {bool(key_exists)}")

                # 4. Delete the key
                await r.delete('async_key')
                print("Deleted 'async_key'")

                # 5. Check again if the key exists
                key_exists_after_delete = await r.exists('async_key')
                print(f"Does 'async_key' exist after deletion? {bool(key_exists_after_delete)}")
                
                # Close the connection
                await r.aclose()
                print("\nConnection to Redis is now closed.")

            except ValueError as ve:
                return str(ve)
        
        case 2:
            print("----- Async Comtext Manager -----")
            try:
                # The async Redis client can be used as a context manager.
                # It will automatically handle connecting and disconnecting.
                async with redis.Redis(host='localhost', port=6379, db=0) as r:
                    # 1. Set a value for a key
                    await r.set('context_key', 'Hello from a context manager!')
                    print("Set 'context_key' to 'Hello from a context manager!'")

                    # 2. Get the value of the key
                    value = await r.get('context_key')
                    if value:
                        print(f"Got the value for 'context_key': {value.decode('utf-8')}")

                    # 3. Check if a key exists
                    key_exists = await r.exists('context_key')
                    print(f"Does 'context_key' exist? {bool(key_exists)}")

                # The connection is automatically closed here, as we've exited the 'async with' block.
                print("\nConnection to Redis is now closed.")

                # You can no longer perform operations on `r`
                # The following line would raise an error if not commented out:
                # await r.get('context_key') 
            except ValueError as ve:
                return str(ve)
        
        case 3:
            print("----- Async Call with Connection Pool -----")
            # 1. Explicitly get an async connection from the pool.
            r = redis.Redis(connection_pool=pool)
            print("\nUsing an async connection from the pool (explicitly managed)...")
            try:
                # 1. Set a value for a key asynchronously
                await r.set('async_key', 'Hello from redis.asyncio!')
                print("Set 'async_key' to 'Hello from redis.asyncio!'")

                # 2. Get the value of the key
                # The result is a bytes object, so we decode it.
                value = await r.get('async_key')
                if value:
                    print(f"Got the value for 'async_key': {value.decode('utf-8')}")

                # 3. Check if a key exists
                key_exists = await r.exists('async_key')
                print(f"Does 'async_key' exist? {bool(key_exists)}")

                # 4. Delete the key
                await r.delete('async_key')
                print("Deleted 'async_key'")

                # 5. Check again if the key exists
                key_exists_after_delete = await r.exists('async_key')
                print(f"Does 'async_key' exist after deletion? {bool(key_exists_after_delete)}")

            except ValueError as ve:
                return str(ve)
            
            finally:
                # IMPORTANT: Always close the connection to return it to the pool.
                # This is a critical step to avoid connection leaks in async mode.
                await r.aclose()
                print("  - Async connection explicitly released back to the pool.")
        
        case 4:
            print("----- Async Comtext Manager with Connection Pool -----")
            try:
                # The async Redis client can be used as a context manager.
                # It will automatically handle connecting and disconnecting.
                async with redis.Redis(connection_pool=pool) as r:
                    # 1. Set a value for a key
                    await r.set('context_key', 'Hello from a context manager!')
                    print("Set 'context_key' to 'Hello from a context manager!'")

                    # 2. Get the value of the key
                    value = await r.get('context_key')
                    if value:
                        print(f"Got the value for 'context_key': {value.decode('utf-8')}")

                    # 3. Check if a key exists
                    key_exists = await r.exists('context_key')
                    print(f"Does 'context_key' exist? {bool(key_exists)}")

                # The connection is automatically released back to the pool here.
                print("Async Redis connection pool disconnected.")
                # You can no longer perform operations on `r`
                # The following line would raise an error if not commented out:
                # await r.get('context_key') 
            except ValueError as ve:
                return str(ve)
            
        case _:
            print(f"Error: wrong run_option({run_option})!")

if __name__ == "__main__":
    asyncio.run(main())
import sys, argparse
import redis

def main():
    print(f"Redis Sync Test...")

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
            print("Hello from Redis-Sync-Test! Please check how to use me by the '-h' argument.")

        case 1:
            print("----- Sync Call -----")
            try:
                # Connect to Redis
                # The default host is 'localhost' and the default port is 6379
                # If your Redis server is running on a different machine or port, adjust these
                r = redis.Redis(host='localhost', port=6379, db=0)

                # 1. Set a value for a key
                r.set('mykey', 'Hello, Redis!')
                print("Set 'mykey' to 'Hello, Redis!'")

                # 2. Get the value of the key: The result is a bytes object, so we need to decode it to a string
                value = r.get('mykey')
                if value:
                    print(f"Got the value for 'mykey': {value.decode('utf-8')}")

                # 3. Check if a key exists
                key_exists = r.exists('mykey')
                print(f"Does 'mykey' exist? {bool(key_exists)}")

                # 4. Delete the key
                r.delete('mykey')
                print("Deleted 'mykey'")

                # 5. Check again if the key exists
                key_exists_after_delete = r.exists('mykey')
                print(f"Does 'mykey' exist after deletion? {bool(key_exists_after_delete)}")

                # Close the connection
                r.close()
                print("\nConnection to Redis is now closed.")

            except ValueError as ve:
                return str(ve)
            
        case 2:
            print("----- Sync Comtext Manager -----")
            try:
                # The synchronous Redis client can be used as a context manager.
                # It will automatically handle connecting and disconnecting.
                with redis.Redis(host='localhost', port=6379, db=0) as r:
                    # 1. Set a value for a key
                    r.set('sync_context_key', 'Hello from a sync context manager!')
                    print("Set 'sync_context_key' to 'Hello from a sync context manager!'")

                    # 2. Get the value of the key
                    # The result is a bytes object, so we need to decode it.
                    value = r.get('sync_context_key')
                    if value:
                        print(f"Got the value for 'sync_context_key': {value.decode('utf-8')}")

                    # 3. Check if a key exists
                    key_exists = r.exists('sync_context_key')
                    print(f"Does 'sync_context_key' exist? {bool(key_exists)}")

                # The connection is automatically closed here, as we've exited the 'with' block.
                print("\nConnection to Redis is now closed.")

            except ValueError as ve:
                return str(ve)
            
        case 3:
            print("----- Sync Call with Connection Pool -----")
            # Explicitly get a connection from the pool.
            r = redis.Redis(connection_pool=pool)
            print("\nUsing a connection from the pool (explicitly managed)...")
            try:
                # 1. Set a value for a key
                r.set('mykey', 'Hello, Redis!')
                print("Set 'mykey' to 'Hello, Redis!'")

                # 2. Get the value of the key: The result is a bytes object, so we need to decode it to a string
                value = r.get('mykey')
                if value:
                    print(f"Got the value for 'mykey': {value.decode('utf-8')}")

                # 3. Check if a key exists
                key_exists = r.exists('mykey')
                print(f"Does 'mykey' exist? {bool(key_exists)}")

                # 4. Delete the key
                r.delete('mykey')
                print("Deleted 'mykey'")

                # 5. Check again if the key exists
                key_exists_after_delete = r.exists('mykey')
                print(f"Does 'mykey' exist after deletion? {bool(key_exists_after_delete)}")

            except ValueError as ve:
                return str(ve)
            
            finally:
                # IMPORTANT: Always return the connection to the pool.
                # This is a critical step to avoid connection leaks.
                if r:
                    r.connection_pool.release(r.connection)
                    print("  - Connection explicitly released back to the pool.")

        case 4:
            print("----- Sync Comtext Manager with Connection Pool -----")
            try:
                # The 'with' statement is the key here. It automatically:
                # 1. Calls __enter__ on the Redis object to get a connection from the pool.
                # 2. Assigns the connection to the variable 'r'.
                # 3. Executes the code inside the block.
                # 4. Calls __exit__ on the Redis object to release the connection back to the pool.
                #    This happens even if an error occurs inside the block.
                with redis.Redis(connection_pool=pool) as r:
                    # 1. Set a value for a key
                    r.set('sync_context_key', 'Hello from a sync context manager!')
                    print("Set 'sync_context_key' to 'Hello from a sync context manager!'")

                    # 2. Get the value of the key
                    # The result is a bytes object, so we need to decode it.
                    value = r.get('sync_context_key')
                    if value:
                        print(f"Got the value for 'sync_context_key': {value.decode('utf-8')}")

                    # 3. Check if a key exists
                    key_exists = r.exists('sync_context_key')
                    print(f"Does 'sync_context_key' exist? {bool(key_exists)}")

                # The connection has been automatically returned to the pool here,
                # and the Redis object 'r' is no longer available.
                print("  - Connection has been released back to the pool.")

            except ValueError as ve:
                return str(ve)
        
        case _:
            print(f"Error: wrong run_option({run_option})!")


if __name__ == "__main__":
    sys.exit(main())
import os
import argparse
from dotenv import load_dotenv
from setting.util import parse_boolean
import uvicorn

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the server in different modes.")
    # 將 parser.add_argument 的部分，分成不同的 group
    app_mode = parser.add_argument_group(title="App Mode", description="Run the server in different modes.")
    app_mode.add_argument("--prod", action="store_true", help="Run the server in production mode.")
    app_mode.add_argument("--test", action="store_true", help="Run the server in test mode.")
    app_mode.add_argument("--dev", action="store_true", help="Run the server in development mode.")
 
    # 新增 run_mode
    run_mode = parser.add_argument_group(title="Run Mode", description="Run the server in Async or Sync mode. Default is Async.")
    run_mode.add_argument("--sync", action="store_true", help="Run the server in Sync mode.")

   # 新增 db_type
    db_type =  parser.add_argument_group(title="Database Type", description="Run the server in different database type.")
    db_type.add_argument("--db", help="Run the server in database type.",choices=["mysql","postgresql"], default="postgresql")

    # Read settings and parsing to environment variables...
    args = parser.parse_args()
    if args.prod:
        load_dotenv("setting/.env.prod")
    elif args.test:
        load_dotenv("setting/.env.test")
    else:
        load_dotenv("setting/.env.dev") # default
        
    if args.sync:
        os.environ["RUN_MODE"] = "SYNC"
    else:
        os.environ["RUN_MODE"] = "ASYNC"

    # export DB_TYPE 環境變數
    os.environ["DB_TYPE"] = args.db        

    app_name: str = "main:app"
    host_name: str = "0.0.0.0"
    port_num: int = int(os.getenv("PORT")) 
    if_reload: bool = parse_boolean(os.getenv("RELOAD"))
    
    print(f"Uvicron starting:(app_name={app_name}, host_name={host_name}, port_num={port_num}, if_reload={if_reload})...")
    uvicorn.run(app_name, host=host_name, port=port_num, reload=if_reload)
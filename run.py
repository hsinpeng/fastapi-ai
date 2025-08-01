import os
import argparse
from dotenv import load_dotenv
from setting.util import parse_boolean
import uvicorn

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the server in different modes.")
    parser.add_argument("--prod", action="store_true", help="Run the server in production mode.")
    parser.add_argument("--test", action="store_true", help="Run the server in test mode.")
    parser.add_argument("--dev", action="store_true", help="Run the server in development mode.")
    
    args = parser.parse_args()
    if args.prod:
        load_dotenv("setting/.env.prod")
    elif args.test:
        load_dotenv("setting/.env.test")
    else:
        load_dotenv("setting/.env.dev")

    app_name: str = "main:app"
    host_name: str = "0.0.0.0"
    port_num: int = int(os.getenv("PORT")) 
    if_reload: bool = parse_boolean(os.getenv("RELOAD"))
    
    print(f"Uvicron starting... ({app_name},{host_name},{port_num},{if_reload})")
    uvicorn.run(app_name, host=host_name, port=port_num, reload=if_reload)
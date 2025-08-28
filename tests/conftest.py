# conftest.py是pytest中一個特殊的檔案，可以在測試中使用一些共用的設定
import os 
from dotenv import load_dotenv
import pytest_asyncio
import pytest
import asyncio
from httpx import AsyncClient

# parser加上需要的arguments，就可以透過pytest --help看到arguments
def pytest_addoption(parser):
    parser.addoption("--prod",action="store_true", help="Run the server in production mode.")
    parser.addoption("--test",action="store_true", help="Run the server in test mode.")
    parser.addoption("--dev",action="store_true", help="Run the server in development mode.")
    parser.addoption("--sync",action="store_true", help="Run the server in Sync mode.")
    parser.addoption("--db", help="Run the server in database type.",choices=["mysql","postgresql"], default="postgresql")



# 在pytest中，如果pytest_asyncio.fixture的scope是 session，還需要在conftest.py加以下設定
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


# fixture可以在測試中共用一些資源: 因為是async function，所以需用pytest_asyncio來建立fixture
# pytest的fixture有這幾種scope:
# 1. function: 每個測試都會執行一次
# 2. class: 每個測試類別都會執行一次
# 3. module: 每個測試 module 都會執行一次
# 4. session: 整個測試會執行一次
@pytest_asyncio.fixture(scope="session")
async def dependencies(request):
    args = request.config

    if args.getoption("prod"):
        load_dotenv("../setting/.env.prod")
    elif args.getoption("test"):
        load_dotenv("../setting/.env.test")
    else:
        load_dotenv("../setting/.env.dev")

    if args.getoption("sync"):
            os.environ["RUN_MODE"] = "SYNC"
    else:
        os.environ["RUN_MODE"] = "ASYNC"

    os.environ["DB_TYPE"] = args.getoption("db")
    print("DB_TYPE",os.getenv("DB_TYPE"))


@pytest_asyncio.fixture(scope="module")
async def async_client(dependencies) -> AsyncClient:
    from .app import app
    async with AsyncClient(app=app,base_url="http://test") as client:
        yield client
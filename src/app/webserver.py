import os

from authlib.integrations.requests_client import OAuth2Session
from dotenv import load_dotenv
from fastapi import FastAPI, Response, Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
import streamsync.serve
import uvicorn

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
ISSUER_DOMAIN = os.getenv('ISSUER_DOMAIN')
MODE = os.getenv('MODE', 'edit') # run or edit
SCOPE = "openid email profile"
REDIRECT_URI = os.getenv('REDIRECT_URI')
ALLOW_EMAILS = os.getenv('ALLOW_EMAILS', "").split(' ')
ALLOW_DOMAINS = os.getenv('ALLOW_DOMAINS', "").split(' ')


auth0 = OAuth2Session(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scope=SCOPE.split(" "),
    redirect_uri=REDIRECT_URI,
    authorization_endpoint=f'https://{ISSUER_DOMAIN}/authorize',
    token_endpoint=f'https://{ISSUER_DOMAIN}/oauth/token',
)

app_path = "." # . for current working directory


root_asgi_app = FastAPI(lifespan=streamsync.serve.lifespan)

@root_asgi_app.get("/")
async def init():
    return Response("""
    <h1>Welcome to the App</h1>
    """)


@root_asgi_app.middleware("http")
async def valid_authentication(request: Request, call_next):
    """
    """
    if 'username' in request.session or request.url.path in ['/callback', '/401']:
        return await call_next(request)
    else:
        url = auth0.create_authorization_url(f'https://{ISSUER_DOMAIN}/authorize')
        response = RedirectResponse(url=url[0])
        return response

@root_asgi_app.get('/callback')
def callback(request: Request):
    token = auth0.fetch_token(token_endpoint='https://{ISSUER_DOMAIN}/oauth/token', authorization_response=str(request.url))
    resp = auth0.get(f'https://{ISSUER_DOMAIN}/userinfo')
    userinfo = resp.json()
    email: str = userinfo['email']
    domain = email.split("@")[1]
    if email in ALLOW_EMAILS or domain in ALLOW_DOMAINS:
        session = request.session
        session['username'] = email
        response = RedirectResponse(url='/app1')
        return response
    else:
        response = RedirectResponse(url='/401')
        return response

@root_asgi_app.get('/logout')
def logout(request: Request):
    session = request.session
    del session['username']
    return Response("""
        <h1>Disconnected</h1>
    """)

@root_asgi_app.get('/401')
def callback(request: Request):
    return Response("""
        <h1>Invalid username</h1>
    """)

sub_asgi_app_1 = streamsync.serve.get_asgi_app(".", MODE)
root_asgi_app.mount("/app1", sub_asgi_app_1)

root_asgi_app.add_middleware(SessionMiddleware, secret_key="xxxxxxxxxx-xxxx")


uvicorn.run(root_asgi_app,
    host="0.0.0.0",
    port=5000,
    log_level="warning",
    ws_max_size=streamsync.serve.MAX_WEBSOCKET_MESSAGE_SIZE)

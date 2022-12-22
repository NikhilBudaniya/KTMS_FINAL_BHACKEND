from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from ..models.vendor import VendorModel, SessionModel
from ..database import get_db
import requests
import json
 

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

config = Config(".env")
oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/auth')
async def auth(request: Request, db: Session=Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)

        user=db.query(VendorModel).filter(VendorModel.email==token.get('userinfo')['email']).first()
        if user is None:
            userinfo = token.get('userinfo')
            newUser = VendorModel()
            newUser.name = userinfo['name']
            newUser.email = userinfo['email']
            db.add(newUser)
            db.commit()
        loginSession = SessionModel()
        loginSession.sessionId = token.get('access_token')
        loginSession.email = token.get('userinfo')['email']
        db.add(loginSession)
        db.commit()
        response = RedirectResponse(url="http://localhost:3000/authredirect/vendor?token="+str(token.get('access_token')))
        return response
    except ValueError:
        raise HTTPException(status_code=498, detail=ValueError)

@router.get('/getuser')
async def auth(request: Request, db: Session=Depends(get_db)):
    token = request.headers["Authorization"]
    userResponse = db.query(SessionModel).filter(SessionModel.sessionId==token).first()
    email = userResponse.email
    if email:
        userInfo =db.query(VendorModel).filter(VendorModel.email==email).first()
        response = {
            "user": {
                'name':userInfo.name,
                'email':userInfo.email
            }
        }
        return JSONResponse(status_code=200, content=response) 
    else:
        raise HTTPException(status_code=498, detail={'msg': 'Invalid Token'})
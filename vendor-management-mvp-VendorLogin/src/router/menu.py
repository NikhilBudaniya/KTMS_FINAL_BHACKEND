from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from ..models.vendor import MenuModel
from ..database import get_db
from ..schemas.vendor import VendorSchema, MenuSchema
import requests
import json
 

router = APIRouter(
    prefix="/menu",
    tags=["menu"]
)

@router.get('/get-menu-for-vendor')
async def getMenuforVendor(email:str, db: Session=Depends(get_db)):
    menu = db.query(MenuModel).filter(MenuModel.user_id==email).all()
    return menu

@router.post('/create-menu-for-vendor')
def createMenuforVendor(menu:MenuSchema, db: Session=Depends(get_db)):
    new_menu = MenuModel()
    new_menu.user_id=menu.user_id
    new_menu.breakfast=menu.breakfast
    new_menu.lunch=menu.lunch
    new_menu.dinner=menu.dinner
    new_menu.date=menu.date
    db.add(new_menu)
    db.commit()
    return new_menu

@router.get('/get-menu-for-day')
async def getMenuforDay(request: Request, db: Session=Depends(get_db)):
    # menuList = db.query(MenuModel).filter(MenuModel.date==request.body.date).all()
    # print(menuList)
    # return JSONResponse(status_code=200, content={'msg':'menu send sucessfully'})
    return {"Response":"Yes"}
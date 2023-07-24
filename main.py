from fastapi import FastAPI, status, HTTPException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

import schemas

Base = declarative_base()

from models import Menu, engine
from models import SubMenu
from models import Dish

app = FastAPI()


@app.get("/api/v1/menus")
async def read_menu_list():
    session = Session(bind=engine, expire_on_commit=False)
    menu_list_db = session.query(Menu).all()
    session.close()
    response = []
    for i in menu_list_db:
        response.append({
            "id": str(i.id),
            "title": i.title,
            "description": i.description,
            "submenus_count": len(session.query(SubMenu).all()),
            "dishes_count": 0
        })
        dishes_count = 0
        for submenu in session.query(SubMenu).where(SubMenu.menu_id == i.id).all():
            dishes_count += len(session.query(Dish).where(Dish.submenu_id == submenu.id).all())
        response[-1]["dishes_count"] = dishes_count
    return response


@app.get("/api/v1/menus/{menu_id}/submenus")
async def read_submenu_list(menu_id: int):
    session = Session(bind=engine, expire_on_commit=False)
    submenu_list_db = session.query(SubMenu).filter(SubMenu.menu_id == menu_id).all()
    session.close()
    response = []
    for i in submenu_list_db:
        response.append({
            "id": str(i.id),
            "title": i.title,
            "description": i.description,
            "dishes_count": len(session.query(Dish).where(Dish.submenu_id == i.id).all())
        })
    return response


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
async def read_dishes_list(menu_id: int, submenu_id: int):
    session = Session(bind=engine, expire_on_commit=False)
    menu_db = session.query(Menu).get(menu_id)
    if not menu_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    dishes_list_db = session.query(Dish).filter(Dish.submenu_id == submenu_id).all()
    session.close()
    response = []
    for i in dishes_list_db:
        response.append({
            "id": str(i.id),
            "title": i.title,
            "description": i.description,
            "price": str(i.price)
        })
    return response


@app.post("/api/v1/menus", status_code=status.HTTP_201_CREATED)
async def create_menu(menu: schemas.MenuRequestCreate):
    session = Session(bind=engine, expire_on_commit=False)
    menu_db = Menu(title=menu.title, description=menu.description)
    session.add(menu_db)
    session.commit()
    session.refresh(menu_db)
    session.close()
    return {
        "id": str(menu_db.id),
        "title": menu_db.title,
        "description": menu_db.description,
        "submenus_count": 0,
        "dishes_count": 0
    }


@app.post("/api/v1/menus/{menu_id}/submenus", status_code=status.HTTP_201_CREATED)
async def create_submenu(menu_id: int, submenu: schemas.SubMenuRequestCreate):
    session = Session(bind=engine, expire_on_commit=False)
    menu_db = session.query(Menu).get(menu_id)
    if not menu_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    submenu_db = SubMenu(title=submenu.title, description=submenu.description, menu_id=menu_id)
    session.add(submenu_db)
    session.commit()
    session.refresh(submenu_db)
    session.close()
    return {
        "id": str(submenu_db.id),
        "title": submenu_db.title,
        "description": submenu_db.description,
        "dishes_count": 0
    }


@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=status.HTTP_201_CREATED)
async def create_dish(menu_id: int, submenu_id: int, dish: schemas.DishRequestCreate):
    session = Session(bind=engine, expire_on_commit=False)
    menu_db = session.query(Menu).get(menu_id)
    if not menu_db:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    submenu_db = session.query(SubMenu).get(submenu_id)
    if not submenu_db:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    dish_db = Dish(title=dish.title, description=dish.description, price=dish.price, submenu_id=submenu_db.id)
    session.add(dish_db)
    session.commit()
    session.refresh(dish_db)
    session.close()
    return {
        "id": str(dish_db.id),
        "title": dish_db.title,
        "description": dish_db.description,
        "price": str(dish_db.price)
    }


@app.get("/api/v1/menus/{menu_id}")
async def read_menu(menu_id: int):
    session = Session(bind=engine, expire_on_commit=False)
    menu_item_db = session.query(Menu).get(menu_id)
    submenus_count = len(session.query(SubMenu).where(SubMenu.menu_id == menu_id).all())
    dishes_count = 0
    for submenu in session.query(SubMenu).where(SubMenu.menu_id == menu_id).all():
        dishes_count += len(session.query(Dish).where(Dish.submenu_id == submenu.id).all())
    session.close()
    if not menu_item_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    return {
        "id": str(menu_item_db.id),
        "title": menu_item_db.title,
        "description": menu_item_db.description,
        "submenus_count": submenus_count,
        "dishes_count": dishes_count
    }


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def read_submenu(menu_id: int, submenu_id: int):
    session = Session(bind=engine, expire_on_commit=False)
    menu_item_db = session.query(Menu).get(menu_id)
    if not menu_item_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    submenu_item_db = session.query(SubMenu).where(SubMenu.menu_id == menu_id, SubMenu.id == submenu_id).first()
    session.close()
    if not submenu_item_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    return {
        "id": str(submenu_item_db.id),
        "title": submenu_item_db.title,
        "description": submenu_item_db.description,
        "dishes_count": len(session.query(Dish).where(Dish.submenu_id == submenu_id).all())
    }


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def read_dish(menu_id: int, submenu_id: int, dish_id: int):
    session = Session(bind=engine, expire_on_commit=False)
    menu_item_db = session.query(Menu).get(menu_id)
    if not menu_item_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    submenu_item_db = session.query(SubMenu).where(SubMenu.menu_id == menu_id, SubMenu.id == submenu_id).first()
    session.close()
    if not submenu_item_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    dish_item_db = session.query(Dish).where(SubMenu.menu_id == menu_id, SubMenu.id == submenu_id,
                                             Dish.id == dish_id).first()
    if not dish_item_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
    return {
        "id": str(dish_item_db.id),
        "title": dish_item_db.title,
        "description": dish_item_db.description,
        "price": str(dish_item_db.price)
    }


@app.patch("/api/v1/menus/{menu_id}")
async def update_menu(menu_id: int, menu: schemas.MenuRequestCreate):
    session = Session(bind=engine, expire_on_commit=False)
    menu_item_db = session.query(Menu).where(Menu.id == menu_id).first()
    if menu_item_db:
        menu_item_db.title = menu.title
        menu_item_db.description = menu.description
        session.commit()
        session.close()
    if not menu_item_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    dishes_count = 0
    for submenu in session.query(SubMenu).where(SubMenu.menu_id == menu_id).all():
        dishes_count += len(session.query(Dish).where(Dish.submenu_id == submenu.id).all())
    response = {
        "id": str(menu_item_db.id),
        "title": menu_item_db.title,
        "description": menu_item_db.description,
        "submenus_count": len(session.query(SubMenu).where(SubMenu.menu_id == menu_id).all()),
        "dishes_count": dishes_count
    }
    return response


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def update_submenu(menu_id: int, submenu_id: int, submenu: schemas.MenuRequestCreate):
    session = Session(bind=engine, expire_on_commit=False)
    submenu_item_db = session.query(SubMenu).where(SubMenu.menu_id == menu_id, SubMenu.id == submenu_id).first()
    if submenu_item_db:
        submenu_item_db.title = submenu.title
        submenu_item_db.description = submenu.description
        session.commit()
        session.close()
    if not submenu_item_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    return {
        "id": str(submenu_item_db.id),
        "title": submenu_item_db.title,
        "description": submenu_item_db.description,
        "dishes_count": len(session.query(Dish).where(Dish.submenu_id == submenu_id).all())
    }


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def update_dish(menu_id: int, submenu_id: int, dish_id: int, dish: schemas.DishRequestCreate):
    session = Session(bind=engine, expire_on_commit=False)
    dish_item_db = session.query(Dish).where(SubMenu.menu_id == menu_id, SubMenu.id == submenu_id,
                                             Dish.id == dish_id).first()
    if dish_item_db:
        dish_item_db.title = dish.title
        dish_item_db.description = dish.description
        dish_item_db.price = dish.price
        session.commit()
        session.close()
    if not dish_item_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
    return {
        "id": str(dish_item_db.id),
        "title": dish_item_db.title,
        "description": dish_item_db.description,
        "price": str(dish_item_db.price)
    }


@app.delete("/api/v1/menus/{menu_id}", status_code=status.HTTP_200_OK)
async def delete_menu(menu_id: int):
    session = Session(bind=engine, expire_on_commit=False)
    menu_item_db = session.query(Menu).get(menu_id)
    if menu_item_db:
        session.delete(menu_item_db)
        session.commit()
        session.close()
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    return {
        "status": True,
        "message": "The menu has been deleted"
    }


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}", status_code=status.HTTP_200_OK)
async def delete_submenu(menu_id: int, submenu_id: int):
    session = Session(bind=engine, expire_on_commit=False)
    submenu_item_db = session.query(SubMenu).where(SubMenu.menu_id == menu_id, SubMenu.id == submenu_id).first()
    if submenu_item_db:
        session.delete(submenu_item_db)
        session.commit()
        session.close()
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    return {
        "status": True,
        "message": "The submenu has been deleted"
    }


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", status_code=status.HTTP_200_OK)
async def delete_dish(menu_id: int, submenu_id: int, dish_id: int):
    session = Session(bind=engine, expire_on_commit=False)
    menu_db = session.query(Menu).get(menu_id)
    if not menu_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    dish_item_db = session.query(Dish).where(Dish.submenu_id == submenu_id, Dish.id == dish_id).first()
    if dish_item_db:
        session.delete(dish_item_db)
        session.commit()
        session.close()
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
    return {
        "status": True,
        "message": "The dish has been deleted"
    }

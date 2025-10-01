from multiprocessing import synchronize
from random import randrange
from sqlite3 import Cursor
from tkinter import END
from typing import Optional, List


import psycopg2
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
import sqlalchemy
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

from app import models


app = FastAPI()


class update_Post(BaseModel):
    title: str
    content: str
    published: bool
    # rating: Optional[int] = None


try:
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="d22csc1040",
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    my_posts = [
        {"title": "title of post 1", "content": "content of post 1", "id": 1},
        {"title": "favourite food", "content": "i like masa", "id": 2},
    ]

except Exception as e:
    print(e)
    raise e

#     Cursor = conn.cursor()
#     print ("Data base connection was successful")
# except Exception as error:
#     print("connecting to database failed")
#     print ("Error: ", error)


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
    pass


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
    pass


@app.get("/")
async def root():
    cursor.execute("SELECT * FROM posts")
    return {"message": "Hello World"}


# learning to use sqlalchemy
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends (get_db)):


#     posts = db.query(models.Post).all()
#     return{"data":"successful"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db), response_model=List[schemas.Post]):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s)
    #                RETURNING*
    #                """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(post.dict())
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts - 1)]
    return {"latest post": post}


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id=%s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return {"post details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    print(post)

    # cursor.execute("""DELETE FROM post WHERE id=%s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    post_query.update(new_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

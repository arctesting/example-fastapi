from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()




class Post(BaseModel):
    title: str
    content: str
    published: bool  = True

while True:
    try:
        conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', 
                            password='$password03', row_factory=dict_row)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break

    except Exception as error:   
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

    my_post = [{"title": "title numero 1", "content": "contnent 1", "id": 1},
            {"title": "Japan Place", "content": "Euno Station", "id": 2}]

def find_post(id):
    for item in my_post:
        if id == item['id']:
            return item

def del_post(id):
    post = find_post(id)
    if post:
        my_post.remove(post)
    return post
    
def change_post(id, post):
    post_index = find_index(id)
    if post_index:
        my_post[post_index] = post

    return post_index

def find_index(id):
    for index, value in enumerate(my_post):
        if id == value['id']:
            return index
     

@app.get("/")
async def root():
    return{"message": "Test to Api"}

@app.get("/sqlalchemy")
def test_alchemy(db: Session = Depends(get_db)):
    return{"status": "success"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    post = cursor.fetchone()
    print(post)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    conn.commit()
    return {"Data": new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (id,))
    delete_post = cursor.fetchone()

    conn.commit()

    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with iid: {id} not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """, 
                   (post.title, post.content, post.published, id))
    
    updated_post = cursor.fetchone()

    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    
    return {"message": "Successfully updated"}
    
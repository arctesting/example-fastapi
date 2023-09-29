from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool  = True
    rating: Optional[int] = None

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


@app.get("/posts")
def get_posts():
    return {"data": my_post}


@app.get("/posts/{id}")
def get_post(id: int):
    print(id)
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    print(post)
    post_dict = post.dict()
    post_dict["id"] = len(my_post) + 1
    my_post.append(post_dict)
    print(post.published)
    return {"Data": post_dict}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #deleting post
    post = del_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with iid: {id} not found")
    #return {"message": f"Post {id} deleted {post}"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    new_post = change_post(id, dict(post))
    if not new_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with iid: {id} not found")
    
    return {"message": "Successfully updated"}
    
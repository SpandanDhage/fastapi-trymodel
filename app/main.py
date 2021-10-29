from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from schemas import Blog, User
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from schemas import showBlog, showUser
from hashing import Hash
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.post("/login", tags=['Authentication'], response_model=showUser)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{request.username} not found")
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password")
    return user


@app.post("/addBlog", status_code=status.HTTP_201_CREATED, tags=['Blog'])
def addblog(req: Blog, db: Session = Depends(get_db)):
    request1 = dict(req)
    request: Blog = Blog(title=request1['title'], body=request1['body'], userId=request1['userId'])

    new_blog = models.Blog(title=request.title, body=request.body, userId=request.userId)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog", response_model=List[showBlog], tags=['Blog'])
def getBlog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{username}", status_code=status.HTTP_302_FOUND, tags=['Blog'])  # , response_model=List[showBlog]
def getBlogWithId(username: str, db: Session = Depends(get_db)):
    userBlogs = db.query(models.Blog).filter(models.Blog.userId == username).all()
    if not userBlogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Feedbacks entered")
    return userBlogs


# @app.delete("/deleteBlog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=['Blog'])
# def delete(id: int, db: Session = Depends(get_db), getCurrentUser : User= Depends(getCurrentUser)):
#     blog=db.query(models.Blog).filter(models.Blog.id == id)
#     if not blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     blog.delete(synchronize_session=False)
#     db.commit()
#     return "Done"

# @app.put("/updateBlog/{title}", status_code=status.HTTP_202_ACCEPTED, tags=['Blog'])
# def update(title: str, request: Blog, db: Session = Depends(get_db), getCurrentUser : User= Depends(getCurrentUser)):
#     blog=db.query(models.Blog).filter(models.Blog.title==title).first()
#     if not blog:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     blog.update(request)
#     db.commit()
#     return "updated"

@app.post("/addUser", status_code=status.HTTP_201_CREATED, tags=['User'])
def createUser(req: User, db: Session = Depends(get_db)):
    request1 = dict(req)
    request: User = User(name=request1['name'], email=request1['email'], password=request1['password'])

    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="User already exists !!")

    new_User = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_User)
    db.commit()
    db.refresh(new_User)
    return new_User.email


# @app.get("/Users", status_code=status.HTTP_302_FOUND, response_model=List[showUser], tags=['User'])
# def getUser(db: Session = Depends(get_db), getCurrentUser : User= Depends(getCurrentUser)):
#     return db.query(models.User).all()

# @app.get("/User/{id}", status_code=status.HTTP_302_FOUND, response_model=showUser, tags=['User'])
# def getUserWithId(id: int, db: Session = Depends(get_db), getCurrentUser : User= Depends(getCurrentUser)):
#     user= db.query(models.User).filter(models.User.id==id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
#     return user


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")

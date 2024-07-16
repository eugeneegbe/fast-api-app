from fastapi import APIRouter, Depends, HTTPException, status
from models.post import Post, PostCreate
from models.user import User
from utils.auth import get_current_user


router = APIRouter()


@router.post("/")
def create_post(post: PostCreate, current_user: User = Depends(get_current_user)):
    # Create a new post
    db_post = Post(**post.dict(), user_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {"id": db_post.id}


@router.get("/")
def get_posts(current_user: User = Depends(get_current_user)):
    # Fetch all posts for the current user
    posts = db.query(Post).filter(Post.user_id == current_user.id).all()
    return posts


@router.delete("/{post_id}")
def delete_post(post_id: int, current_user: User = Depends(get_current_user)):
    # Delete a post
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == current_user.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}

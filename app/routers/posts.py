from fastapi import APIRouter, Depends, HTTPException, status
from models.post import Post, PostCreate
from models.user import User
from utils.auth import get_current_user


from starlette.middleware.base import BaseHTTPMiddleware
from starlette_cache.backends.memory import MemoryCacheBackend
from starlette_cache.plugins.fastapi import FastAPIPlugin

# Initialize the cache backend and plugin
cache = MemoryCacheBackend()
cache_plugin = FastAPIPlugin(cache)

# Add the cache middleware to the FastAPI app
app.add_middleware(BaseHTTPMiddleware, dispatch=cache_plugin.cache_response)

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
    # Check if the posts are in the cache
    cache_key = f"posts_{current_user.id}"
    cached_posts = cache.get(cache_key)
    if cached_posts:
        return cached_posts

    # Fetch all posts for the current user
    posts = db.query(Post).filter(Post.user_id == current_user.id).all()

    # Store the posts in the cache for 5 minutes
    cache.set(cache_key, posts, timeout=300)
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

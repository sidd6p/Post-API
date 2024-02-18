from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, oauth2, schemas, models


router = APIRouter(prefix="/votes", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def set_vote(
    vote_payload: schemas.VoteBase,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(oauth2.get_current_user),
):
    post_id = vote_payload.post_id
    add_vote = bool(vote_payload.add_vote)

    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} not found",
        )
    voted = (
        db.query(models.Vote)
        .filter(models.Vote.post_id == post_id)
        .filter(models.Vote.user_id == user_id)
    )
    if add_vote:
        if voted.first() is None:
            vote = models.Vote()
            vote.user_id = user_id
            vote.post_id = post_id
            db.add(vote)
            db.commit()
            return {"message": f"Voted post with id: {post_id}"}
        else:
            return {"message": f"Post with id: {post_id} is already voted"}
    if not add_vote:
        if voted.first():
            voted.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

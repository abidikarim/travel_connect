from fastapi import APIRouter, Request, HTTPException, status
from app.dependencies import dbDep, formDataDep
from app.services import auth
from app import schemas

router = APIRouter(prefix="/auth", tags=["Authenticate"])


@router.post("/forgetpwd")
async def forget_pwd(db: dbDep, req: Request):
    body = await req.json()
    return await auth.forget_password(db, body.get("email"))


@router.post("/resetpwd")
async def reset_pwd(db: dbDep, reset_pwd_data: schemas.ResetPassword, code: str):
    if reset_pwd_data.password != reset_pwd_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords must match"
        )
    return auth.reset_password(
        db=db, reset_pwd_data={"password": reset_pwd_data.password, "code": code}
    )


@router.post("/login")
def login(db: dbDep, user_credentials: formDataDep):
    return auth.login(
        db=db,
        user_credentials={
            "email": user_credentials.username,
            "password": user_credentials.password,
        },
    )

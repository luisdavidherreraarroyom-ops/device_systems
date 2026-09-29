from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies.database_dependency import get_db
from app.models.user_model import User
from app.schemas.auth_schema import Token, UserRegister
from app.schemas.user_schema import UserResponse
from app.auth.security import verify_password, create_access_token, get_password_hash
from app.auth.dependencies import get_current_user
from app.core.limiter import limiter

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
def register_user(request: Request, user_data: UserRegister, db: Session = Depends(get_db)):
    """Registra un nuevo usuario con contraseña hasheada."""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado",
        )

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        role=user_data.role,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Autentica a un usuario y devuelve un token JWT de acceso."""
    # Buscar el usuario por su correo electrónico usando form_data.username
    user = db.query(User).filter(User.email == form_data.username).first()

    # Validar si el usuario existe y si la contraseña coincide
    if not user or not user.hashed_password or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear el token de acceso (expira en 30 minutos)
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    """Devuelve los datos del usuario autenticado."""
    return current_user
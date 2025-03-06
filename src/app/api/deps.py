from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from app.core.db.database import get_db


DbDep = Annotated[Session, Depends(get_db)]

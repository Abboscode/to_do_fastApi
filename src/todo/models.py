# todo/models.py

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String, Integer, Boolean

# --------------------
## 🏛️ Base Class
# --------------------

# Inheriting from DeclarativeBase provides the necessary .metadata attribute
class Base(DeclarativeBase):
    pass

# --------------------
## 📝 Todo Model
# --------------------

class TodoModel(Base):
    __tablename__ = "todos"
    
    # id is auto-incremented by default since it is the integer primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True) 
    
    # Mapped[str] defaults to String(255) in modern SQLAlchemy
    title: Mapped[str]
    dateAdded: Mapped[str] 
    description: Mapped[str]
    
    # Mapped[bool] defaults to Boolean type
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
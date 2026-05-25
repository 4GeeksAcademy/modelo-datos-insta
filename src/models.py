from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

# ==========================================
# 1. MODELO: USER
# ==========================================
class User(db.Model):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(80), nullable=False)
    lastname: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    # Relaciones bidireccionales hacia Post y Comment
    posts: Mapped[List["Post"]] = relationship(back_populates="author", lazy=True)
    comments: Mapped[List["Comment"]] = relationship(back_populates="author", lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }


# ==========================================
# 2. MODELO: FOLLOWER (Tabla Intermedia)
# ==========================================
class Follower(db.Model):
    __tablename__ = 'follower'
    
    # Clave primaria compuesta para la relación autorreferencial de User
    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }


# ==========================================
# 3. MODELO: POST
# ==========================================
class Post(db.Model):
    __tablename__ = 'post'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    
    # Relación inversa hacia el creador (User)
    author: Mapped["User"] = relationship(back_populates="posts")
    
    # Relaciones hacia Media y Comment
    media: Mapped[List["Media"]] = relationship(back_populates="post", lazy=True)
    comments: Mapped[List["Comment"]] = relationship(back_populates="post", lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "media": [m.serialize() for m in self.media]  # Incluye sus elementos multimedia al serializar
        }


# ==========================================
# 4. MODELO: MEDIA
# ==========================================
class Media(db.Model):
    __tablename__ = 'media'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(Enum('image', 'video', name='media_types'), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    
    # Relación inversa hacia Post
    post: Mapped["Post"] = relationship(back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }


# ==========================================
# 5. MODELO: COMMENT
# ==========================================
class Comment(db.Model):
    __tablename__ = 'comment'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(500), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    
    # Relaciones inversas hacia User y Post
    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }
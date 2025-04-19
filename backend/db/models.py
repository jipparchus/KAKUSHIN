"""
Plan tables for the RDB

1. User table
2. CameraMatrix Table
3. Climb Table
4. SharedClimb Table
"""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Text, Uuid, Date, DateTime, ForeignKey, Integer, Float, Boolean, JSON
import uuid
from datetime import date, datetime
from zoneinfo import ZoneInfo


class Base(DeclarativeBase):
    pass


"""
class -> table
class instance variable -> table column
"""


class User(Base):
    __tablename__ = 'users'
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo('Asia/Tokyo')),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo('Asia/Tokyo')),
        onupdate=lambda: datetime.now(ZoneInfo('Asia/Tokyo')),
    )
    first_climb: Mapped[date] = mapped_column(
        Date,
        nullable=True,
    )
    vgrade: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )
    height: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    weight: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    share_info: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    # Relationship
    myclimbs: Mapped[list['Climb']] = relationship(
        back_populates='user'
    )
    cam_matrices: Mapped[list['CameraMatrix']] = relationship(
        back_populates='user'
    )


class Climb(Base):
    __tablename__ = 'climbs'
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('users.id'),
        nullable=False,
    )
    camera_matrix_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('camera_matrices.id'),
        nullable=False,
    )
    video: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo('Asia/Tokyo')),
    )
    wall: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    problem: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    sent: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    attempt: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    share: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    reuse_data: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    # Relationship
    user: Mapped['User'] = relationship(
        back_populates='myclimbs'
    )


class CameraMatrix(Base):
    __tablename__ = 'camera_matrices'
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey('users.id'),
        nullable=False,
    )
    camera_matrix: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )
    # Relationship
    user: Mapped['User'] = relationship(
        back_populates='cam_matrices'
    )


class SharedClimb(Base):
    __tablename__ = 'shared_climbs'
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    climb_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey('climbs.id'),
        nullable=False,
    )

# app/models.py
from sqlalchemy import Column, String, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base
import uuid
import enum

# --- ENUM for file status ---
class FileStatus(str, enum.Enum):
    with_dept = "With Department"
    in_transit = "In Transit"
    archived = "Archived"

# --- Department Table ---
class Department(Base):
    __tablename__ = "departments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)

# --- File Table ---
class File(Base):
    __tablename__ = "files"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_number = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    current_dept_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    status = Column(Enum(FileStatus), default=FileStatus.with_dept)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    current_department = relationship("Department")

# --- Movement Log Table ---
class FileMovement(Base):
    __tablename__ = "file_movements"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id"))
    from_dept_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    to_dept_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    action = Column(String)  # "Sent", "Received"
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    file = relationship("File")

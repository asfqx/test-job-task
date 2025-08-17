from api.db.database import Base
from sqlalchemy.orm import MappedColumn, mapped_column
from sqlalchemy import BigInteger, String


class MethodNames(Base):
    __tablename__ = 'method_names'

    id = mapped_column(BigInteger, primary_key=True)
    name = mapped_column(String, nullable=False)
    currency = mapped_column(String, nullable=False)

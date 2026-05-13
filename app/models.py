from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Members(Base):
    __tablename__ = "Members"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    join_date = Column(Date, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    loans = relationship("Loans", back_populates="member")

class Authors(Base):
    __tablename__ = "Authors"

    authors_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    country = Column(String, nullable=False)

    books = relationship("Book_Authors", back_populates="author")

class Categories(Base):
    __tablename__ = "Categories"

    categories_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    books = relationship("Books", back_populates="category")

class Books(Base):
    __tablename__ = "Books"

    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    isbn = Column(String, nullable=False)
    total_copies = Column(Integer, nullable=False)
    published_year = Column(Date, nullable=False)
    category_id = Column(Integer, ForeignKey("Categories.categories_id"), nullable=True)

    category = relationship("Categories", back_populates="books")
    loans = relationship("Loans", back_populates="book")
    authors = relationship("Book_Authors", back_populates="book")

class Book_Authors(Base):
    __tablename__ = "Book_Authors"

    book_id = Column(Integer, ForeignKey("Books.book_id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("Authors.authors_id"), primary_key=True)

    book = relationship("Books", back_populates="authors")
    author = relationship("Authors", back_populates="books")

class Loans(Base):
    __tablename__ = "Loans"

    loans_id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("Members.id"), nullable=True)
    book_id = Column(Integer, ForeignKey("Books.book_id"), nullable=True)
    loan_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)

    member = relationship("Members", back_populates="loans")
    book = relationship("Books", back_populates="loans")
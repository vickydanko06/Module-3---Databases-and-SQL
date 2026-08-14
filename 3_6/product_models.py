"""
Exercise: Product Catalog Models
Module 3 | Lesson 6 | ~35 min

Objective:
  Define SQLAlchemy 2.0 ORM models for a product catalog and write
  queries using the ORM's select() API instead of raw SQL strings.
"""
from sqlalchemy import (
    create_engine, select,
    String, Float, Boolean, Integer, ForeignKey
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from typing import Optional, List

engine = create_engine("sqlite:///:memory:", echo=False)


class Base(DeclarativeBase):
    pass


# ── TODO: Define the Category model ──────────────────────────────────────────
# Table name: "categories"
# Columns:
#   id   — Integer, primary key
#   name — String, required, unique
# Relationship: one category -> many products
class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)# integer id that is a primary key
    name: Mapped[str] = mapped_column(nullable=False, unique=True) #name that is a string that is required and unique
    #on the online assignment it said to list a description but on the starter code it did not mention, so i did not add.
    products: Mapped[list["Product"]] = relationship(back_populates="category")
    # TODO: define columns using Mapped and mapped_column
    # TODO: add a relationship to Product (use back_populates="category")
    pass


# ── TODO: Define the Product model ────────────────────────────────────────────
# Table name: "products"
# Columns:
#   id          — Integer, primary key
#   name        — String, required
#   description — String, optional
#   price       — Float, required
#   in_stock    — Boolean, default True
#   category_id — Integer, ForeignKey("categories.id")
# Relationship: many products -> one category
class Product(Base):
    __tablename__ = "products"
    # TODO: define columns
    # TODO: add a relationship to Category (use back_populates="products")
    id: Mapped[int] = mapped_column(primary_key=True)#int id that is the primary key
    name: Mapped[str] = mapped_column(nullable=False)#name that is a string and is not able to be NULL.
    description: Mapped[Optional[str]] = mapped_column() #this is a description with no restrictions
    price: Mapped[float] = mapped_column(nullable=True)#price is a float(allows for decimals) that is not allowed to be NULL.
    in_stock: Mapped[bool] = mapped_column(default=True)#in stock flag that defaults to true(in stock).
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))#category id that is the foreign key
    category: Mapped[list["Category"]] = relationship(back_populates="products")

    pass


# ── Test block ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Create tables (run this once your models are defined)
    Base.metadata.create_all(engine)

    # ── Seed data ─────────────────────────────────────────────────────────────
    with Session(engine) as session:
        electronics = Category(name="Electronics")
        books       = Category(name="Books")
        sports      = Category(name="Sports")
        session.add_all([electronics, books, sports])
        session.flush()  # assigns IDs without committing

        session.add_all([
            Product(name="Wireless Headphones", price=79.99,  in_stock=True,  category_id=electronics.id),
            Product(name="Mechanical Keyboard", price=129.99, in_stock=True,  category_id=electronics.id),
            Product(name="USB-C Hub",           price=39.99,  in_stock=False, category_id=electronics.id),
            Product(name="Python Crash Course", price=39.99,  in_stock=True,  category_id=books.id),
            Product(name="SQL for Beginners",   price=29.99,  in_stock=True,  category_id=books.id),
            Product(name="Yoga Mat",            price=34.99,  in_stock=True,  category_id=sports.id),
        ])
        session.commit()

    # ── Query 1: All products in stock ────────────────────────────────────────
    print("Products in stock:")
    with Session(engine) as session:
        # TODO: write a select() query that returns all Products where in_stock == True
        # stmt = select(Product).where(...)
        # products = session.execute(stmt).scalars().all()
        # for p in products:
        #     print(f"  {p.name} — ${p.price:.2f}")
        pass
        stmt = select(Product).where(Product.in_stock==True) #variable to store products in stock
        products = session.execute(stmt).scalars().all() 
        for p in products:
            print(f"  {p.name} — ${p.price:.2f}")#prints items and price

    # ── Query 2: Products under $50, ordered by price ─────────────────────────
    print("Products under $50 (cheapest first):")
    with Session(engine) as session:
        # TODO: write a select() query with a price filter and order_by
        pass
        cheap = select(Product).where(Product.price < 50).order_by(Product.price)#variable to store products under 50
        products = session.execute(cheap).scalars().all()
        for p in products:
            print(f" {p.name} - {p.price:.2f}")

    # ── Query 3: All products with their category name ────────────────────────
    print("All products with category:")
    with Session(engine) as session:
        # TODO: write a select() that also loads the category relationship
        # Hint: you can access p.category.name after joining or via lazy load
        # stmt = select(Product).join(Product.category)
        pass
        stmt = select(Product).join(Product.category)
        products = session.execute(stmt).scalars().all()
        for p in products:
            print(f" {p.name} - {p.category.name}")

from sqlalchemy import Column, Integer, Boolean, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    # Relationship with subcategories
    subcategories = relationship("Subcategory", back_populates="category")
    products = relationship("Product", back_populates="category")

class Subcategory(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))

    # Relationship with category
    category = relationship("Category", back_populates="subcategories")
    products = relationship("Product", back_populates="subcategory")

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    # Relationship with products
    products = relationship("Product", back_populates="brand")

class ProductPhoto(Base):
    __tablename__ = "product_photos"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    url = Column(String)

    # Relationship with product
    product = relationship("Product", back_populates="photos")

class ProductSize(Base):
    __tablename__ = "product_sizes"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    size = Column(String)

    # Relationship with product
    product = relationship("Product", back_populates="sizes")

class ProductColor(Base):
    __tablename__ = "product_colors"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    color = Column(String)

    # Relationship with product
    product = relationship("Product", back_populates="colors")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    discount = Column(Float)
    stock = Column(Integer)
    material_type = Column(String)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    brand = relationship("Brand", back_populates="products")
    category = relationship("Category", back_populates="products")
    subcategory = relationship("Subcategory", back_populates="products")
    reviews = relationship("Review", back_populates="product")
    photos = relationship("ProductPhoto", back_populates="product")
    sizes = relationship("ProductSize", back_populates="product")
    colors = relationship("ProductColor", back_populates="product")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    rating = Column(Integer)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="reviews")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)
    address_id = Column(Integer, ForeignKey("user_addresses.id"))
    payment_method = Column(String)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    address = relationship("UserAddress", back_populates="orders")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Float)
    size = Column(String)
    color = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)

    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    size = Column(String)
    color = Column(String)
    is_gift = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="carts")
    product = relationship("Product")

class WishList(Base):
    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    size = Column(String)
    color = Column(String)
    is_gift = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="wishlists")
    product = relationship("Product")


class UserAddress(Base):
    __tablename__ = "user_addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    full_name = Column(String)
    mobile = Column(String)
    alternate_mobile = Column(String)
    address_line1 = Column(String)
    address_line2 = Column(String)
    landmark = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    pincode = Column(String)
    is_default = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="address")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    mobile = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)


    # Relationships
    orders = relationship("Order", back_populates="user")
    carts = relationship("Cart", back_populates="user")
    wishlists = relationship("WishList", back_populates="user")
    addresses = relationship("UserAddress", back_populates="user")

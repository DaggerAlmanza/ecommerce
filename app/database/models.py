import enum
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    DECIMAL,
    Enum,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import (
    declarative_base,
)
from sqlalchemy.orm import relationship
from app.config.constants import (
    DATABASE_URL
)


Base = declarative_base()


class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"


class OrderStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(
        Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False
    )
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    user = relationship("Users", back_populates="orders")
    order_items = relationship(
        "OrderItems", back_populates="order", cascade="all, delete-orphan"
    )

    def to_json(self, *args, **kwargs):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "total_amount": self.total_amount,
            "status": self.status.value,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }


class OrderItems(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    order = relationship("Orders", back_populates="order_items")
    product = relationship("Products", back_populates="order_items")

    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="_order_product_uc"),
    )

    def to_json(self, *args, **kwargs):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price_at_purchase": self.price_at_purchase,
            "created_at": str(self.created_at),
        }


class Carts(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    user = relationship("Users", back_populates="carts")
    cart_items = relationship(
        "CartItems", back_populates="cart", cascade="all, delete-orphan"
    )

    def to_json(self, *args, **kwargs):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_at": str(self.created_at),
        }


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(45), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    adress = Column(String)
    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True
    )

    orders = relationship("Orders", back_populates="user")
    carts = relationship("Carts", back_populates="user", uselist=False)
    products_created = relationship(
        "Products", back_populates="creator", cascade="all, delete-orphan"
    )

    def to_json(self, *args, **kwargs):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "role": self.role.value,
            "adress": self.adress,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    image_url = Column(String(255), nullable=True)
    creator_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True
    )

    cart_items = relationship("CartItems", back_populates="product")
    order_items = relationship("OrderItems", back_populates="product")
    creator = relationship("Users", back_populates="products_created")

    def to_json(self, *args, **kwargs):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "stock_quantity": self.stock_quantity,
            "image_url": self.image_url,
            "creator_id": self.creator_id,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }


class CartItems(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_add = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    cart = relationship("Carts", back_populates="cart_items")
    product = relationship("Products", back_populates="cart_items")

    __table_args__ = (
        UniqueConstraint("cart_id", "product_id", name="_cart_product_uc"),
    )

    def to_json(self, *args, **kwargs):
        return {
            "id": self.id,
            "cart_id": self.cart_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price_at_add": self.price_at_add,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }

    def to_dict(self, *args, **kwargs):
        cart_data = None
        if self.cart:
            cart_data = self.cart.to_dict()
        return {
            "id": self.id,
            "cart_id": cart_data,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price_at_add": self.price_at_add,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }


engine = create_engine(
    DATABASE_URL
)
Base.metadata.create_all(engine)

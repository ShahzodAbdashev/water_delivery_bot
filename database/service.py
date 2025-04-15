import logging

from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from database import models
from utils.translation import _

async def get_user_language(user_id):
    async with models.async_session() as session:
        try:
            stmt = await session.execute(select(models.User).where(models.User.telegram_id == str(user_id)))

            user = stmt.scalar_one_or_none()
            return user.language if user else None
        except Exception as e:
            logging.warning(f"Cannot get user language, Error says {e}")
    
async def get_user(user_id):
    async with models.async_session() as session:
        try:
            stmt = await session.execute(select(models.User).where(models.User.telegram_id == str(user_id)))

            user = stmt.scalar_one_or_none()
            return user
        except Exception as e:
            logging.warning(f"Cannot get user it self, Error says {e}")
    
async def create_new_user(data:dict, telegram_id:int):
    async with models.async_session() as session:
        try:
            stmt = models.User(
                full_name=data['full_name'],
                phone_number=data['phone_number'],
                language=data['language'],
                telegram_id=str(telegram_id)
            )
            session.add(stmt)
            await session.commit()
            logging.info("User created successfully")
        except Exception as e:
            logging.warning(f"Cannot create new user, Error says {e}")

async def change_language(language:str, user_id:int):
    async with models.async_session() as session:
        try:
            await session.execute(update(models.User)
                                        .where(models.User.telegram_id == str(user_id))
                                        .values(language=language))
            await session.commit()
            logging.info("Language changes successfully")
        except Exception as e:
            logging.warning(f"Cannot change langugae, Error says {e}")

async def get_product_with_name(lang:str):
    async with models.async_session() as session:
        try:
            stmt = await session.execute(select(models.Product))
            products = stmt.scalars().all()

            keyboard = []
            row = []

            for i, product in enumerate(products):
                row.append(KeyboardButton(text=product.name))
                if (i + 1) % 2 == 0 or i == len(products) - 1:
                    keyboard.append(row)
                    row = []  
            keyboard.append([KeyboardButton(text=_('⬅️ Back',lang))])
            return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        except Exception as e:
            logging.warning(f"Cannot get all products button, Error says {e}")
    
async def get_product_name(name:str):
    async with models.async_session() as session:
        try:
            stmt = await session.execute(select(models.Product).where(models.Product.name == name))

            product = stmt.scalar_one_or_none()
            return product
        except Exception as e:
            logging.warning(f"Cannot get product name button, Error says {e}")
    
async def create_order(product_id:int, quantity:int,
                       time:str, location:str,user_id:str):
    try:
        async with models.async_session() as session:
            order = models.Order(
                product_id=product_id,
                quantity=quantity,
                delivery_time=time,
                location=location,
                user_id=user_id
            )

            session.add(order)

            await session.commit()

            logging.info("Order created successfully")
    except Exception as e:
        logging.warning(f"Cannot create order, Error says {e}")

async def create_product(name:str, price:str, image:str):
    async with models.async_session() as session:
        try:
            product = models.Product(
                name=name,
                price=price,
                image=image,
                description='sassfsdfsdf'
            )
            session.add(product)

            await session.commit()
            logging.info("Product created successfully")
        except Exception as e:
            logging.warning(f"Cannot create product, Error says {e}")

async def get_orders_not_done():
    async with models.async_session() as session:
        try:
            orders = await session.execute(
                    select(models.Order)
                    .join(models.Order.user)        
                    .join(models.Order.product)     
                    .where(models.Order.is_delivered == False)
                    .options(
                        joinedload(models.Order.user),
                        joinedload(models.Order.product)
                    )
                )
            return orders.scalars().all()
        except Exception as e:
            logging.warning("Cannot get all order, Error says {e}")
    
async def update_order_done(order_id):
    async with models.async_session() as session:
        try:
            await session.execute(update(models.Order)
                                .where(models.Order.id == order_id)
                                .values(is_delivered=True))
            await session.commit()
            logging.info("Order delivered successfully")
        except Exception as e:
            logging.warning(f'Order not updated, Error says {e}')

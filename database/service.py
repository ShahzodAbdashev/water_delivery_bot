from sqlalchemy import select, update
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from database import models
from utils.translation import _

async def get_user_language(user_id):
    async with models.async_session() as session:
        stmt = await session.execute(select(models.User).where(models.User.telegram_id == str(user_id)))

        user = stmt.scalar_one_or_none()
        return user.language if user else None
    
async def get_user(user_id):
    async with models.async_session() as session:
        stmt = await session.execute(select(models.User).where(models.User.telegram_id == str(user_id)))

        user = stmt.scalar_one_or_none()
        return user
    
async def create_new_user(data:dict, telegram_id:int):
    async with models.async_session() as session:
        stmt = models.User(
            full_name=data['full_name'],
            phone_number=data['phone_number'],
            language=data['language'],
            telegram_id=str(telegram_id)
        )
        session.add(stmt)
        await session.commit()

async def change_language(language:str, user_id:int):
    async with models.async_session() as session:
        await session.execute(update(models.User)
                                     .where(models.User.telegram_id == str(user_id))
                                     .values(language=language))
        await session.commit()

async def get_product_with_name(lang:str):
    async with models.async_session() as session:
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
    
async def get_product_name(name:str):
    async with models.async_session() as session:
        stmt = await session.execute(select(models.Product).where(models.Product.name == name))

        product = stmt.scalar_one_or_none()
        return product
    
async def create_order(product_id:int, quantity:int,
                       time:str, location:str,user_id:str):
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

async def create_product(name:str, price:str, image:str):
    async with models.async_session() as session:
        product = models.Product(
            name=name,
            price=price,
            image=image,
            description='sassfsdfsdf'
        )
        session.add(product)

        await session.commit()
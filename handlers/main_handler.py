import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove

from database import service
from utils.translation import _
from utils.location_verification import verify_location_yandex
from keyboards import reply_keywords

main_router = Router()


class RegisterUser(StatesGroup):
    language = State()
    full_name = State()
    phone_number = State()

class ChangeLanguage(StatesGroup):
    language = State()

class OrderProduct(StatesGroup):
    product = State()
    quantity = State()
    time = State()
    location = State()
    location_type = State()


# user registration
@main_router.message(StateFilter(None), CommandStart())
async def start_chat(message:Message, state:FSMContext):
    user_lang = await service.get_user_language(message.from_user.id)

    if user_lang is not None:
        await message.answer(_("Botimizga xush kelibsiz !!!",user_lang),reply_markup=reply_keywords.main_menu(user_lang))
    else: 
        await state.set_state(RegisterUser.language)
        await message.answer("Til tanlang", reply_markup=reply_keywords.language_menu)

@main_router.message(RegisterUser.language, F.text)
async def choose_language(message:Message, state:FSMContext):
    languages = {
        '🇬🇧 English': "en",
        '🇺🇿 Uzbek': "uz",
        '🇷🇺 Russian': "ru"
    }
    await state.update_data(language=languages[message.text])
    if message.text not in languages:
        await message.answer('Faqatgina kerakli tilni tanglang')
        return 
    await state.set_state(RegisterUser.full_name)
    await message.answer(_("Enter your full name", languages[message.text]), reply_markup=ReplyKeyboardRemove())

@main_router.message(RegisterUser.full_name, F.text)
async def enter_fullname(message:Message, state:FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()

    await state.set_state(RegisterUser.phone_number)
    await message.answer(_('Enter phone number',data['language']), 
                         reply_markup=reply_keywords.back_and_phone_button(data['language']))
    
    
@main_router.message(RegisterUser.phone_number, F.contact)
async def enter_phone_number(message:Message, state:FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    
    data = await state.get_data()
    logging.info(data)
    await service.create_new_user(data=data, telegram_id=message.from_user.id)

    await message.answer(_("You successfully, registered", data['language']), reply_markup=reply_keywords.main_menu(data['language']))
    await state.clear()
# user registration end

#contact our people
@main_router.message(F.text.in_(['Contacts','Контакты','Aloqaga chiqish']))
async def contact_with_us(message:Message):
    lang = await service.get_user_language(message.from_user.id)
    await message.answer(_("Bizning operatorlarimiz bilan bog'laning: +998 94-924-29-45",lang), reply_markup=reply_keywords.main_menu(lang))
#contact our people end

#change language
@main_router.message(F.text.in_(['⚙️ Settings','⚙️ Sozlamalar','⚙️ Настройки']))
async def change_language(message:Message, state:FSMContext):
    lang = await service.get_user_language(message.from_user.id)

    await state.set_state(ChangeLanguage.language)
    await message.answer(_('Choose nessesery language', lang), reply_markup=reply_keywords.language_menu)

@main_router.message(ChangeLanguage.language, F.text)
async def change_valid_language(message:Message, state:FSMContext):
    languages = {
        '🇬🇧 English': "en",
        '🇺🇿 Uzbek': "uz",
        '🇷🇺 Russian': "ru"
    }
    await state.update_data(language=languages[message.text])
    if message.text not in languages:
        await message.answer('Faqatgina kerakli tilni tanglang')
        return 

    await service.change_language(language=languages[message.text], 
                                  user_id=message.from_user.id)
    await message.answer(_('Language changed successfully',languages[message.text]), reply_markup=reply_keywords.main_menu(languages[message.text]))
    await state.clear()
#change language end

#order product
@main_router.message(StateFilter(None), F.text.in_(['Order product','Заказать продукт','Mahsulot buyurtma berish']))
async def order_product_steps(message:Message, state:FSMContext):
    lang = await service.get_user_language(message.from_user.id)

    await state.set_state(OrderProduct.product)
    await message.answer(_("Choose one of the product",lang), reply_markup=await service.get_product_with_name(lang))

@main_router.message(OrderProduct.product, F.text)
async def order_product_name(message:Message, state:FSMContext):
    product_name = await service.get_product_name(message.text)
    await state.update_data(product=product_name)
    lang = await service.get_user_language(message.from_user.id)

    await state.set_state(OrderProduct.quantity)
    await message.answer(_('How many do you need',lang), reply_markup=reply_keywords.quantity_product(lang))

@main_router.message(OrderProduct.quantity, F.text)
async def order_product_quantity(message:Message, state:FSMContext):
    await state.update_data(quantity=message.text)
    lang = await service.get_user_language(message.from_user.id)

    await state.set_state(OrderProduct.time)
    await message.answer(_("In what time it need to delivered",lang), reply_markup=reply_keywords.time_interval(lang))

@main_router.message(OrderProduct.time, F.text)
async def order_product_time(message:Message, state:FSMContext):
    await state.update_data(time=message.text)
    lang = await service.get_user_language(message.from_user.id)

    await state.set_state(OrderProduct.location)
    await message.answer(_("Input you location",lang), 
                         reply_markup=reply_keywords.back_and_location_button(lang))

@main_router.message(OrderProduct.location, F.location)
async def order_product_location(message:Message, state:FSMContext):
    lang = await service.get_user_language(message.from_user.id)
    if message.location:
        location_=verify_location_yandex(message.location.latitude, message.location.longitude,)
        await message.answer(_('Bu mazilni tasdiqlaysizmi **{location_}**'.format(location_=location_),lang),
                             parse_mode="Markdown",
                             reply_markup=reply_keywords.keyboard_location_input(lang))
        
    elif message.text in ['Tasdiqlayman','Confirm','Подтверждаю']:
        data = await state.get_data()
        await state.update_data(location=data.get("location"))  
        user_id = await service.get_user(message.from_user.id)  
        product_id = await service.get_product_name(data['product'])
        await service.create_order(
            product_id=product_id.id,
            user_id=user_id.id,
            time=data['time'],
            location=data['location'],
            quantity=int(data['quantity'])
        )

        await message.answer(_("Product added successfully, just wait about 2 days", lang), reply_keywords.main_menu(lang))
        await state.clear()

    elif message.text in ["Qo'lda kiritaman",'Ввод вручную','Enter manually']:
        await message.answer(_("Enter by hand !!!",lang))
        await state.set_state(OrderProduct.location_type)

@main_router.message(OrderProduct.location_type, F.text)
async def order_product_location_type(message:Message, state:FSMContext):
    lang = await service.get_user_language(message.from_user.id)
    await state.update_data(location_type=message.text)

    await message.answer(_("Product added successfully, just wait", lang), reply_keywords.main_menu(lang))
    await state.clear()
#order product
    




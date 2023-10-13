from aiogram import Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import CommandStart

from database.database import add_user, user_in_test, current_question, show_question, get_current_question_content
from database.database import show_answers, score, result, process_stop_test, get_current_question
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.keyboards import create_inline_kb, create_url_inline_kb

router = Router()
GUIDE_PATH = 'media/documents/guide_reader.pdf'
PHOTO_START_PATH = 'media/photos/photo_1.jpg'
PHOTO_RESULT_PATH = 'media/photos/result.jpg'


@router.message(CommandStart())
async def process_start_command(message: Message):
    add_user(message.from_user.id)
    photo = FSInputFile(PHOTO_START_PATH)
    keyboard = create_inline_kb(1, 'download_guide', 'pass_test')
    await message.answer_photo(photo=photo, caption=LEXICON_RU['/start'],
                               reply_markup=keyboard)


@router.callback_query(F.data == 'download_guide')
async def process_start_command(callback: CallbackQuery):
    process_stop_test(callback.from_user.id)
    doc = FSInputFile(GUIDE_PATH)
    await callback.message.answer_document(document=doc)


@router.callback_query(F.data == 'pass_test')
async def process_start_command(callback: CallbackQuery):
    process_stop_test(callback.from_user.id)
    keyboard = create_inline_kb(1, 'start_test', 'refusal')
    await callback.message.answer(text=LEXICON_RU['info_test'],
                                  reply_markup=keyboard)


@router.callback_query(F.data == 'refusal')
async def process_start_command(callback: CallbackQuery):
    process_stop_test(callback.from_user.id)
    keyboard = create_inline_kb(1, 'start_test')

    await callback.message.answer(text=LEXICON_RU['text_refusal'],
                                  reply_markup=keyboard)


@router.callback_query(F.data == 'start_test')
async def process_start_test(callback: CallbackQuery):
    current_question(callback.from_user.id)
    question, answers = get_current_question_content(callback.from_user.id)
    keyboard = create_inline_kb(3, **{'1': '1', '2': '2', '3': '3'})
    if question:
        await callback.message.answer_photo(caption=f"{question[0]}\n\n"
                                                    f"{answers}",
                                            photo=FSInputFile(question[1]),
                                            reply_markup=keyboard)
    else:
        user_result = result(callback.from_user.id)
        keyboard = create_url_inline_kb('buy_book', url=user_result[0][1])
        photo = FSInputFile(PHOTO_RESULT_PATH)
        await callback.message.answer_photo(caption=f"{user_result[0][0]}\n\n{LEXICON_RU['result']}",
                                            photo=photo,
                                            reply_markup=keyboard)


@router.callback_query(F.data.in_({'1', '2', '3'}))
async def answer_choice(callback: CallbackQuery):
    if user_in_test(callback.from_user.id):
        score(callback.from_user.id, callback.data)
        await process_start_test(callback)
    else:
        keyboard = create_inline_kb(1, 'start_test')
        await callback.message.answer(text=LEXICON_RU['user_not_in_test'],
                                      reply_markup=keyboard)

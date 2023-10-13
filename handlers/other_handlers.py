from aiogram import Router
from aiogram.types import Message, FSInputFile

from database.database import user_in_test, get_current_question, show_question, show_answers, result, \
    get_current_question_content
from handlers.user_handlers import PHOTO_RESULT_PATH
from keyboards.keyboards import create_inline_kb, create_url_inline_kb
from lexicon.lexicon_ru import LEXICON_RU

router = Router()


@router.message()
async def answer_choice(message: Message):
    if user_in_test(message.from_user.id):
        question, answers = get_current_question_content(message.from_user.id)

        keyboard = create_inline_kb(3, **{'1': '1', '2': '2', '3': '3'})
        if question:
            await message.answer_photo(caption=f"{question[0]}\n\n"
                                               f"{answers}",
                                       photo=FSInputFile(question[1]),
                                       reply_markup=keyboard)
        else:
            user_result = result(message.from_user.id)
            keyboard = create_url_inline_kb('buy_book', url=user_result[0][1])
            photo = FSInputFile(PHOTO_RESULT_PATH)
            await message.answer_photo(caption=f"{user_result[0][0]}\n\n{LEXICON_RU['result']}",
                                       photo=photo,
                                       reply_markup=keyboard)

    else:
        keyboard = create_inline_kb(1, 'download_guide', 'pass_test')
        await message.answer(text=LEXICON_RU['warning'],
                             reply_markup=keyboard)

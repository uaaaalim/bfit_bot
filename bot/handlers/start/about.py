from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder


about_router = Router(name="start.about")

@about_router.callback_query(F.data == "start:about:education")
async def about_education(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="📄 Показать документы", callback_data="start:about:education:docs:0")
    keyboard.button(text="📘 Подход к тренировкам", callback_data="start:about:trains")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="start:survey")
    keyboard.button(text="⬅️ Назад", callback_data="start:about")

    keyboard.adjust(2, 1)

    await callback.answer()
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile("attachments/photo/photo_2026-05-31_23-36-57.jpg"),
            caption=(
                "Квалификация, обучение и спортивный опыт:\n\n"
                "— 15 лет в фитнесе и регулярной тренировочной практике;\n"
                "— диплом профессиональной переподготовки World Class University по квалификации "
                "“Тренер тренажёрного зала”;\n"
                "— удостоверение о повышении квалификации в Высшей школе фитнеса и бодибилдинга по программе оптимизации "
                "тренировочного процесса;\n"
                "— сертификат по программе “Персональный тренер”;\n"
                "— обучение в Invictus Academy;\n"
                "— практический семинар Banzai Fitness по тренировкам ног и ягодиц;\n"
                "— грамота World Class за высокий уровень сервиса.\n\n"
                "Это подтверждает не только спортивный опыт, но и подход к подбору нагрузки, "
                "технике и работе с людьми разного уровня."
            ),
        ),
        reply_markup=keyboard.as_markup(),
    )

@about_router.callback_query(F.data == "start:about:education:docs:0")
async def about_education_docs_0(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="➡️ Следующий документ", callback_data="start:about:education:docs:1")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="start:survey")
    keyboard.button(text="⬅️ Назад к квалификации", callback_data="start:about:education")
    keyboard.adjust(1)

    await callback.answer()
    await callback.message.edit_media(
        media=InputMediaPhoto(media=FSInputFile("attachments/photo/photo_2026-05-31_23-47-58.jpg")),
        reply_markup=keyboard.as_markup(),
    )

@about_router.callback_query(F.data == "start:about:education:docs:1")
async def about_education_docs_1(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="⬅️ Предыдущий документ", callback_data="start:about:education:docs:0")
    keyboard.button(text="➡️ Следующий документ", callback_data="start:about:education:docs:2")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="start:survey")
    keyboard.button(text="⬅️ Назад к квалификации", callback_data="start:about:education")
    keyboard.adjust(2, 1)

    await callback.answer()
    await callback.message.edit_media(
        media=InputMediaPhoto(media=FSInputFile("attachments/photo/photo_2026-05-31_23-49-51.jpg")),
        reply_markup=keyboard.as_markup(),
    )

@about_router.callback_query(F.data == "start:about:education:docs:2")
async def about_education_docs_2(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="⬅️ Предыдущий документ", callback_data="start:about:education:docs:1")
    keyboard.button(text="➡️ Следующий документ", callback_data="start:about:education:docs:3")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="start:survey")
    keyboard.button(text="⬅️ Назад к квалификации", callback_data="start:about:education")
    keyboard.adjust(2, 1)

    await callback.answer()
    await callback.message.edit_media(
        media=InputMediaPhoto(media=FSInputFile("attachments/photo/docs1.png")),
        reply_markup=keyboard.as_markup(),
    )

@about_router.callback_query(F.data == "start:about:education:docs:3")
async def about_education_docs_3(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="⬅️ Предыдущий документ", callback_data="start:about:education:docs:2")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="start:survey")
    keyboard.button(text="⬅️ Назад к квалификации", callback_data="start:about:education")
    keyboard.adjust(1)

    await callback.answer()
    await callback.message.edit_media(
        media=InputMediaPhoto(media=FSInputFile("attachments/photo/docs2.png")),
        reply_markup=keyboard.as_markup(),
    )

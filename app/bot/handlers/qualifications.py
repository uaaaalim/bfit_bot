from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.cache import attachments_cache
from app.utils.message_resolver import remove_old_message

qualifications_router = Router(name="qualifications")

@qualifications_router.callback_query(F.data == "qualifications")
async def qualifications_button(callback: CallbackQuery) -> None:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📄 Показать документы", callback_data="qualifications:documents")
    keyboard.button(text="📘 Подход к тренировкам", callback_data="qualifications:approach")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="survey")
    keyboard.button(text="⬅️ Назад", callback_data="about")
    keyboard.adjust(2, 1)

    await callback.answer()
    old_message = await remove_old_message(callback)
    await old_message.answer_photo(
        photo=attachments_cache.get("app/attachments/images/qualification.jpg"),
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
        reply_markup=keyboard.as_markup(),
    )


@qualifications_router.callback_query(F.data == "qualifications:documents")
async def documents_button(callback: CallbackQuery) -> None:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="survey")
    keyboard.button(text="⬅️ Назад к квалификации", callback_data="qualifications")
    keyboard.adjust(1)

    media = [
        InputMediaPhoto(media=attachments_cache.get("app/attachments/images/documents/banzai_fitness_seminar.png")),
        InputMediaPhoto(
            media=attachments_cache.get("app/attachments/images/documents/invictus_academy_certificate.png")),
        InputMediaPhoto(media=attachments_cache.get("app/attachments/images/documents/qualification_school.jpg")),
        InputMediaPhoto(media=attachments_cache.get("app/attachments/images/documents/sport_forum_diploma.jpg")),
    ]

    await callback.answer()
    old_message = await remove_old_message(callback)
    await old_message.answer_media_group(media=media)
    await old_message.answer(
        text=(
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
        reply_markup=keyboard.as_markup(),
    )

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.cache.photo_cache import get_photo, save_photo_id
from bot.handlers.message_replace import remove_old_message


about_router = Router(name="start.about")

DOC_PHOTO_KEYS = (
    "qualification_school",
    "sport_forum_diploma",
    "banzai_fitness_seminar",
    "invictus_academy_certificate",
)

@about_router.callback_query(F.data == "start:about")
async def about(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="🎓 Образование и квалификация", callback_data="start:about:education")
    keyboard.button(text="📘 Подход к тренировкам", callback_data="start:about:trains")
    keyboard.button(text="📸 Примеры работы", callback_data="start:results")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="start:survey")

    keyboard.adjust(2, 1)

    old_message = await remove_old_message(callback)
    sent_message = await old_message.answer_photo(
        photo=get_photo(callback.bot.id, "about"),
        caption=(
            "Илья Мун — персональный тренер, КМС по бодибилдингу, "
            "автор книг о фитнесе и создатель тренировочной системы MTR 10.\n\n"
            "В фитнесе с 2011 года. Илья работает с мужчинами и женщинами разного уровня подготовки: "
            "от новичков до тех, кто уже тренируется, но хочет более понятную систему и стабильный результат.\n\n"
            "Главный принцип работы — не давать всем одну и ту же программу, а подбирать тренировки под цель, "
            "опыт, ограничения и реальный образ жизни человека."
        ),
        reply_markup=keyboard.as_markup(),
    )
    save_photo_id(callback.bot.id, "about", sent_message)

@about_router.callback_query(F.data == "start:about:education")
async def about_education(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="📄 Показать документы", callback_data="start:about:education:docs")
    keyboard.button(text="📘 Подход к тренировкам", callback_data="start:about:trains")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="start:survey")
    keyboard.button(text="🏆 Кто такой Илья", callback_data="start:about")

    keyboard.adjust(2, 1)

    old_message = await remove_old_message(callback)
    sent_message = await old_message.answer_photo(
        photo=get_photo(callback.bot.id, "education"),
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
    save_photo_id(callback.bot.id, "education", sent_message)

@about_router.callback_query(F.data == "start:about:education:docs")
async def about_education_docs(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="start:survey")
    keyboard.button(text="⬅️ Назад к квалификации", callback_data="start:about:education")
    keyboard.adjust(1)

    old_message = await remove_old_message(callback)
    for photo_key in DOC_PHOTO_KEYS:
        sent_message = await old_message.answer_photo(
            photo=get_photo(callback.bot.id, photo_key),
            reply_markup=keyboard.as_markup() if photo_key == DOC_PHOTO_KEYS[-1] else None,
        )
        save_photo_id(callback.bot.id, photo_key, sent_message)

@about_router.callback_query(F.data == "start:about:trains")
async def about_trains(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📋 Как начинается работа", callback_data="start:about:trains:how")
    keyboard.button(text="📊 Как отслеживается прогресс", callback_data="start:about:trains:progress")
    keyboard.button(text="🧠 Авторская система MTR-10", callback_data="start:about:trains:mtr10")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="start:survey")
    keyboard.button(text="🏆 Кто такой Илья", callback_data="start:about")

    keyboard.adjust(1)

    old_message = await remove_old_message(callback)
    await old_message.answer(
        text=(
            "Подход к тренировкам\n\n"
            "Работа начинается не с готовой программы “для всех”, а со знакомства с человеком.\n\n"
            "Перед стартом Илья собирает основную информацию: цель, опыт тренировок, состояние здоровья, ограничения, "
            "график, уровень активности и то, что уже пробовали раньше.\n\n"
            "На основе этих данных составляется индивидуальный тренировочный план. Он может быть направлен на "
            "снижение веса, набор мышечной массы, функциональную подготовку, растяжку, бокс или другую задачу.\n\n"
            "Дальше работа строится по системе: тренировки фиксируются, прогресс отслеживается, "
            "при необходимости программа корректируется.\n\n"
            "Цель подхода — не просто дать набор упражнений, а выстроить понятный и безопасный путь к результату."
        ),
        reply_markup=keyboard.as_markup(),
    )

@about_router.callback_query(F.data == "start:about:trains:how")
async def about_trains_how(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📊 Как отслеживается прогресс", callback_data="start:about:trains:progress")
    keyboard.button(text="🧠 Что такое MTR-10", callback_data="start:about:trains:mtr10")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="start:survey")
    keyboard.button(text="⬅️ Назад", callback_data="start:about:trains")

    keyboard.adjust(1)

    old_message = await remove_old_message(callback)
    await old_message.answer(
        text=(
            "Как начинается работа\n\n"
            "Перед началом тренировок Илья знакомится с клиентом и собирает подробную информацию.\n\n"
            "Это нужно, чтобы понять:\n\n"
            "— какую цель ставит человек;\n"
            "— какой есть опыт тренировок;\n"
            "— есть ли травмы, боли или ограничения;\n"
            "— какой график и уровень активности;\n"
            "— какой формат занятий удобен;\n"
            "— что раньше мешало заниматься регулярно;\n"
            "— какие особенности важно учитывать при составлении программы.\n\n"
            "После этого Илья подбирает формат работы и составляет тренировочный план под конкретного человека, "
            "а не по шаблону."
        ),
        reply_markup=keyboard.as_markup(),
    )

@about_router.callback_query(F.data == "start:about:trains:progress")
async def about_trains_progress(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🧠 Что такое MTR-10", callback_data="start:about:trains:mtr10")
    keyboard.button(text="📸 Примеры работы", callback_data="start:results")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="start:survey")
    keyboard.button(text="⬅️ Назад", callback_data="start:about:trains")
    keyboard.adjust(1)

    old_message = await remove_old_message(callback)
    await old_message.answer(
        text=(
            "Как отслеживается прогресс\n\n"
            "После старта Илья фиксирует исходную точку и дальше отслеживает изменения.\n\n"
            "В зависимости от цели могут использоваться:\n\n"
            "— тренировочная таблица;\n"
            "— записи по нагрузке, весам, повторениям и упражнениям;\n"
            "— контроль веса;\n"
            "— замеры тела;\n"
            "— фотографии “до/после”;\n"
            "— сравнение результатов по неделям или месяцам.\n\n"
            "Например, при снижении веса можно отслеживать динамику по весу, объёмам и фото. "
            "При наборе мышечной массы — смотреть не только цифру на весах, но и качество формы, "
            "силовые показатели и визуальные изменения.\n\n"
            "Такой контроль помогает понимать, что работает, а что нужно скорректировать."
        ),
        reply_markup=keyboard.as_markup(),
    )

@about_router.callback_query(F.data == "start:about:trains:mtr10")
async def about_trains_mtr10(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📸 Примеры работы", callback_data="start:results")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="start:survey")
    keyboard.button(text="⬅️ Назад", callback_data="start:about:trains")
    keyboard.adjust(1)

    old_message = await remove_old_message(callback)
    await old_message.answer(
        text=(
            "MTR-10\n\n"
            "MTR-10, или Muscle Tissue Recruitment, — авторский протокол Ильи, основанный на контроле движения, "
            "технике и точном включении целевых мышц.\n\n"
            "Смысл системы — не просто поднимать большой вес, а выполнять упражнения так, "
            "чтобы нужная мышца работала максимально осознанно на протяжении подхода.\n\n"
            "MTR-10 может подойти тем, кто:\n\n"
            "— ограничен по времени и хочет тренироваться эффективнее;\n"
            "— живёт в режиме стресса и не хочет перегружать нервную систему;\n"
            "— хочет снизить лишнюю нагрузку на суставы и спину;\n"
            "— тренируется, но перестал видеть прогресс;\n"
            "— хочет лучше чувствовать работу мышц и технику упражнений.\n\n"
            "В основе подхода — индивидуальный подбор упражнений, контроль биомеханики и "
            "грамотная прогрессия нагрузки.\n\n"
            "Технические детали системы, параметры нагрузки и значение цифры “10” не раскрываются публично. "
            "Подопечные получают готовую схему, настроенную под их цель, уровень подготовки и ограничения."
        ),
        reply_markup=keyboard.as_markup(),
    )

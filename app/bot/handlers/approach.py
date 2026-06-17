from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.message_resolver import remove_old_message

approach_router = Router(name="approach")


async def show_approach(callback: CallbackQuery, back_to: str) -> None:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📋 Как начинается работа", callback_data=f"{back_to}:approach:getting_started")
    keyboard.button(text="📊 Как отслеживается прогресс", callback_data=f"{back_to}:approach:tracking")
    keyboard.button(text="🧠 Авторская система MTR-10", callback_data=f"{back_to}:approach:mtr10")
    keyboard.button(text="🎯 Подобрать формат занятий",  callback_data="survey")
    keyboard.button(text="⬅️ Назад", callback_data=back_to)
    keyboard.adjust(1)

    await callback.answer()
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


@approach_router.callback_query(F.data == "about:approach")
async def approach_from_about(callback: CallbackQuery) -> None:
    await show_approach(callback, back_to="about")

@approach_router.callback_query(F.data == "qualifications:approach")
async def approach_from_qualifications(callback: CallbackQuery) -> None:
    await show_approach(callback, back_to="qualifications")


@approach_router.callback_query(F.data.endswith("approach:getting_started"))
async def getting_started_button(callback: CallbackQuery) -> None:
    back_to_approach = callback.data.split(":")[0]

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📊 Как отслеживается прогресс", callback_data=f"{back_to_approach}:approach:tracking")
    keyboard.button(text="🧠 Что такое MTR-10", callback_data=f"{back_to_approach}:approach:mtr10")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="survey")
    keyboard.button(text="⬅️ Назад", callback_data=f"{back_to_approach}:approach")
    keyboard.adjust(1)

    await callback.answer()
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

@approach_router.callback_query(F.data.endswith("approach:tracking"))
async def tracking_button(callback: CallbackQuery) -> None:
    back_to_approach = callback.data.split(":")[0]

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🧠 Что такое MTR-10", callback_data=f"{back_to_approach}:approach:mtr10")
    keyboard.button(text="📸 Примеры работы", callback_data="results")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="survey")
    keyboard.button(text="⬅️ Назад", callback_data=f"{back_to_approach}:approach")
    keyboard.adjust(1)

    await callback.answer()
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

@approach_router.callback_query(F.data.endswith("approach:mtr10"))
async def mtr10_button(callback: CallbackQuery) -> None:
    back_to_approach = callback.data.split(":")[0]

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📸 Примеры работы", callback_data="results")
    keyboard.button(text="🎯 Подобрать формат занятий", callback_data="survey")
    keyboard.button(text="⬅️ Назад", callback_data=f"{back_to_approach}:approach")
    keyboard.adjust(1)

    await callback.answer()
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

from dataclasses import dataclass
from enum import StrEnum

from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto, InputMediaVideo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.cache import attachments_cache
from app.utils.message_resolver import remove_old_message


results_router = Router(name="results")


class ResultMediaType(StrEnum):
    PHOTO = "photo"
    VIDEO = "video"


@dataclass(frozen=True)
class ResultPage:
    path: str
    type: ResultMediaType
    caption: str


RESULTS: dict[int, ResultPage] = {
    1: ResultPage(
        path="app/attachments/results/video1.mp4",
        type=ResultMediaType.VIDEO,
        caption=(
            "Пример работы с учеником (1/4)\n\n"
            "В начале работы фиксируется исходная форма, затем тренировки строятся по индивидуальному плану: "
            "техника, контроль движения, постепенная нагрузка и отслеживание прогресса.\n\n"
            "В процессе Илья смотрит не только на упражнения, но и на то, как человек двигается: положение корпуса, "
            "работу мышц, амплитуду и безопасность выполнения.\n\n"
            "Такой подход помогает не просто “ходить в зал”, а двигаться к результату по понятной системе.\n\n"
            "Результаты индивидуальны и зависят от исходных данных, регулярности, питания, "
            "режима и соблюдения рекомендаций."
        ),
    ),
    2: ResultPage(
        path="app/attachments/results/video2.mp4",
        type=ResultMediaType.VIDEO,
        caption=(
            "Пример работы с учеником (2/4)\n\n"
            "Илья контролирует выполнение упражнения: технику, положение корпуса, амплитуду и качество движения.\n\n"
            "Такой подход помогает не просто выполнять задания по списку, а тренироваться осознанно, безопаснее и "
            "с корректировкой под свой уровень подготовки.\n\n"
            "Формат занятий подбирается индивидуально: под цель, опыт, физическую форму и возможные ограничения."
        ),
    ),
    3: ResultPage(
        path="app/attachments/results/photo_2026-06-17_23-14-47.jpg",
        type=ResultMediaType.PHOTO,
        caption=(
            "Пример работы: снижение веса и улучшение формы (3/4)\n\n"
            "Запрос: снизить лишний вес, подтянуть форму и вернуться к более регулярным тренировкам.\n\n"
            "В работе учитывались:\n"
            "— уровень подготовки;\n"
            "— техника упражнений;\n"
            "— регулярность тренировок;\n"
            "— питание;\n"
            "— контроль прогресса.\n\n"
            "Результат: заметное визуальное снижение объёмов и более подтянутая форма за период работы.\n"
            "Результаты индивидуальны и зависят от исходных данных, питания, режима и регулярности."
        ),
    ),
    4: ResultPage(
        path="app/attachments/results/photo_2026-06-17_23-16-33.jpg",
        type=ResultMediaType.PHOTO,
        caption=(
            "Пример работы: фиксация формы в процессе работы (4/4)\n\n"
            "Перед началом тренировок Илья может фиксировать исходную точку: фото в нескольких ракурсах, вес, "
            "замеры и тренировочные показатели.\n\n"
            "Это помогает дальше объективно отслеживать изменения: форму, осанку, тонус, объёмы и общий прогресс.\n\n"
            "Такой подход особенно полезен, когда цель — не просто “сбросить вес”, а улучшить качество тела и "
            "выстроить понятную систему тренировок."
        ),
    ),
}


def get_back_to(callback_data: str) -> str:
    return ":".join(callback_data.split(":")[:-2])


def result_callback(back_to: str, page: int) -> str:
    return f"{back_to}:results:{page}"


def result_keyboard(back_to: str, page: int):
    keyboard = InlineKeyboardBuilder()

    if page > 1:
        keyboard.button(
            text="⬅️ Предыдущее",
            callback_data=result_callback(back_to, page - 1),
        )

    if page < len(RESULTS):
        keyboard.button(
            text="➡️ Следующее",
            callback_data=result_callback(back_to, page + 1),
        )

    keyboard.button(
        text="🎯 Подобрать формат занятий",
        callback_data="survey",
    )

    keyboard.button(
        text="⬅️ Назад",
        callback_data=back_to,
    )

    if page == 1 or page == len(RESULTS):
        keyboard.adjust(1)
    else:
        keyboard.adjust(2, 1, 1)

    return keyboard.as_markup()


def build_input_media(page_data: ResultPage, file_id: str):
    if page_data.type == ResultMediaType.PHOTO:
        return InputMediaPhoto(
            media=file_id,
            caption=page_data.caption,
        )

    if page_data.type == ResultMediaType.VIDEO:
        return InputMediaVideo(
            media=file_id,
            caption=page_data.caption,
        )

    raise ValueError(f"Unsupported result media type: {page_data.type}")


async def show_result_page(
    callback: CallbackQuery,
    page: int
) -> None:
    back_to = get_back_to(callback.data)

    page_data = RESULTS.get(page)

    if page_data is None:
        await callback.answer("Такой страницы нет", show_alert=True)
        return

    file_id = attachments_cache.get(page_data.path)

    if file_id is None:
        await callback.answer("Медиа не найдено в кэше", show_alert=True)
        return

    await callback.answer()

    keyboard = result_keyboard(back_to=back_to, page=page)

    old_message = await remove_old_message(callback)

    if page_data.type == ResultMediaType.PHOTO:
        await old_message.answer_photo(
            photo=file_id,
            caption=page_data.caption,
            reply_markup=keyboard,
        )
    if page_data.type == ResultMediaType.VIDEO:
        await old_message.answer_video(
            video=file_id,
            caption=page_data.caption,
            reply_markup=keyboard,
        )

@results_router.callback_query(F.data.endswith("results:1"))
async def results_1_button(callback: CallbackQuery) -> None:
    await show_result_page(callback, page=1)


@results_router.callback_query(F.data.endswith("results:2"))
async def results_2_button(callback: CallbackQuery) -> None:
    await show_result_page(callback, page=2)


@results_router.callback_query(F.data.endswith("results:3"))
async def results_3_button(callback: CallbackQuery) -> None:
    await show_result_page(callback, page=3)


@results_router.callback_query(F.data.endswith("results:4"))
async def results_4_button(callback: CallbackQuery) -> None:
    await show_result_page(callback, page=4)

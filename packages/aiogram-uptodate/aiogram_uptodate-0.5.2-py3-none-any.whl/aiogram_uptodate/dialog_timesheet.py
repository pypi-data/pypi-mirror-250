import calendar
from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery

from .schemas import (
    DialogCalendarCallback,
    DialogCalAct,
    DialogTSheetAct,
    DialogTimeSheetCallback,
    highlight,
    superscript,
)
from .common import GenericCalendar


class DialogTimeSheet(GenericCalendar):
    ignore_callback = DialogTimeSheetCallback(
        act=DialogTSheetAct.ignore
    ).pack()  # placeholder for no answer buttons

    async def start_timesheet(
        self,
        available_times: list = None,
        previos_button: bool = False,
    ) -> InlineKeyboardMarkup:
        kb = []
        # time buttons
        for time in available_times:
            kb.append(
                [
                    InlineKeyboardButton(
                        text=time,
                        callback_data=DialogTimeSheetCallback(
                            act=DialogTSheetAct.time, time=time
                        ).pack(),
                    )
                ]
            )
        if previos_button:
            kb.append(
                [
                    InlineKeyboardButton(
                        text="<<",
                        callback_data=DialogTimeSheetCallback(
                            act=DialogTSheetAct.back
                        ).pack(),
                    )
                ]
            )
        return InlineKeyboardMarkup(row_width=5, inline_keyboard=kb)

    async def process_selection(
        self, query: CallbackQuery, data: DialogTimeSheetCallback
    ) -> tuple:
        return_data = (False, None)

        if data.act == DialogTSheetAct.ignore:
            await query.answer(cache_time=60)
        if data.act == DialogTSheetAct.time:
            await query.message.delete()
            return (True, data.time)
        if data.act == DialogTSheetAct.back:
            await query.message.delete()
            return (False, False)
        return return_data

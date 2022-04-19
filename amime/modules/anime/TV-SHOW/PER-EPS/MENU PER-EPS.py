from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime


@Amime.on_message(filters.cmd(r"ktgr-episode$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^ktgr-episode$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.lebih24_button, "ktgr-24+"),
            (lang.kurang24_button, "ktgr-24-"),

        ],    
    ]

    if is_callback:
        keyboard.append([(lang.back_button, "ktgr_tvshow-menu")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.anime_text,
        reply_markup=ikb(keyboard),
    )
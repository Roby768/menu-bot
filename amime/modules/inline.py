# MIT License
#
# Copyright (c) 2021 Amano Team
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import aioanilist
import re

from pyrogram import filters
from pyrogram.types import InlineQuery, InlineQueryResultPhoto
from typing import List

from ..amime import Amime


@Amime.on_inline_query()
async def answer(bot: Amime, inline_query: InlineQuery):
    lang = inline_query._lang
    results: List[InlineQueryResultPhoto] = []
    is_gallery: bool = False

    query = inline_query.query.split()
    if len(query) > 1:
        if query[0].startswith("!"):
            if query[0] in ["!a", "!m"]:
                if query[1].startswith("!"):
                    if query[1] == "!g":
                        is_gallery = True
                    search = " ".join(query[2:])
                else:
                    search = " ".join(query[1:])
                content_type = "anime" if query[0] == "!a" else "manga"

                async with aioanilist.Client() as client:
                    results_search = await client.search(content_type, search, limit=7)
                    for result in results_search:
                        result = await client.get(content_type, result.id)
                        photo = (
                            result.banner
                            or result.cover.extra_large
                            or result.cover.large
                            or result.cover.medium
                        )

                        description = result.description
                        if description:
                            description = re.sub(re.compile(r"<.*?>"), "", description)
                            description = description[0:180] + "..."

                        if is_gallery:
                            text = ""
                        else:
                            text = f"<b>{result.title.romaji}</b> (<code>{result.title.native}</code>)\n"
                            text += f"\n<b>{lang.id}</b>: <code>{result.id}</code> (<b>{content_type.upper()}</b>)"
                            text += f"\n<b>{lang.score}</b>: (<b>{lang.mean} = <code>{result.score.mean or 0}</code>, {lang.average} = <code>{result.score.average or 0}</code></b>)"
                            text += (
                                f"\n<b>{lang.status}</b>: <code>{result.status}</code>"
                            )
                            text += f"\n<b>{lang.genres}</b>: <code>{', '.join(result.genres)}</code>"
                            text += f"\n<b>{lang.start_date}</b>: <code>{result.start_date.day or 0}/{result.start_date.month or 0}/{result.start_date.year or 0}</code>"
                            if not result.status.lower() == "releasing":
                                text += f"\n<b>{lang.end_date}</b>: <code>{result.end_date.day or 0}/{result.end_date.month or 0}/{result.end_date.year or 0}</code>"
                        results.append(
                            InlineQueryResultPhoto(
                                photo_url=photo,
                                title=result.title.romaji,
                                description=description,
                                caption=text,
                            )
                        )

    if len(results) > 0:
        await inline_query.answer(
            results=results,
            is_gallery=is_gallery,
            cache_time=1,
        )
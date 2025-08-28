import asyncio
from googletrans import Translator


async def translate_text():
    async with Translator() as translator:
        result = await translator.translate('Hello', dest="ru")
        print(result.text)


asyncio.run(translate_text())

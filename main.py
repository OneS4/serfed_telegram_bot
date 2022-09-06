from aiogram.types import ContentTypes

from bot_importation_and_ostal import *


@dp.message_handler(content_types=['left_chat_member', 'new_chat_members'])
async def delete(message: Message):
    await message.delete()

executor.start_polling(dp, skip_updates=True)

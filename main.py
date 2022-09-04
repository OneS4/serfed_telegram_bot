from bot_importation_and_ostal import *


@dp.message_handler(commands=['start', 'video', 'playlist', 'weather'])
async def start_perform(message: Message):
    add_user_db(message.from_user.id)
    check_access_bool = check_access(message.from_user.id)
    if check_access_bool and message.text != '/start':
        # await message.answer('What do you want to do?', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        #     [InlineKeyboardButton('Download content from YouTube', callback_data='youtube')],
        #     [InlineKeyboardButton('Find out the weather', callback_data='weather')]
        # ]))
        if message.text == '/video':
            await message.answer('Send a link to the video:')
            await States.video_state.set()
        elif message.text == '/playlist':
            await message.answer('Send a link to the playlist:')
            await States.playlist_state.set()
        elif message.text == '/weather':
            await message.answer('Choose a city', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton('Tashkent', callback_data='tashkent-5331'),
                 InlineKeyboardButton('Kungrad', callback_data='kungrad-323387')]
            ]))
    elif not check_access_bool and message.chat.id == message.from_user.id:
        await message.answer('Get access to the bot:', reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton('Get', callback_data='check_access')]]))
        await States.delete_access_start.set()


@dp.message_handler(state=States.delete_access_start)
async def check_start_def(message: Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id - 2)
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await bot.delete_message(message.chat.id, message.message_id)
    await state.finish()


@dp.callback_query_handler(state='*')
async def callback_main(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'check_access':
        await state.finish()
        await callback.message.edit_text('Enter your code:')
        await States.check_access_state.set()
    # elif callback.data == 'youtube':
    #     await callback.message.edit_text('What do you want to download from YouTube?',
    #                                      reply_markup=InlineKeyboardMarkup(inline_keyboard=[
    #                                          [InlineKeyboardButton('Download video', callback_data='video')],
    #                                          [InlineKeyboardButton('Download video playlist',
    #                                                                callback_data='video playlist')]
    #                                      ]))
    # elif callback.data == 'video':
    #     await callback.message.edit_text('Send a link to the video:')
    #     await States.video_state.set()
    elif callback.data in ['144p', '240p', '360p', '480p', '720p']:
        resolution = callback.data
        await callback.message.delete()
        async with state.proxy() as datas:
            message_id = (await callback.message.answer('Please wait'))['message_id']
            if (await state.get_state()) == 'States:video_state':
                video = video_download(datas['url'], resolution)
                if video['Bool']:
                    title = f'{video["Title"]}.mp4'
                    await callback.message.answer_document(InputFile(title))
                    os.remove(title)
                else:
                    await callback.message.answer(
                        'The video could not be downloaded, perhaps this video does not exist or this permission is '
                        'not '
                        'available for download')
            else:
                playlist = playlist_download(datas['url'], resolution)
                if playlist['Bool']:
                    for video in playlist['Title']:
                        title = f'{video}.mp4'
                        await callback.message.answer_document(InputFile(title))
                        os.remove(title)
                else:
                    await callback.message.answer(
                        'The playlist could not be downloaded, perhaps this playlist does not exist or this '
                        'permission is not available for download')
            await bot.delete_message(callback.message.chat.id, message_id)
        await state.finish()
    elif callback.data in ['tashkent-5331', 'kungrad-323387']:
        weather = find_weather(callback.data)
        text = ''
        for i in range(14):
            if i != 0:
                text += '\n\n'
            text += f"<b>{weather['days'][i]}</b>\n{weather['weather'][i]}\nДнём: {weather['temperature_day'][i]} ℃\n" \
                    f"Ночью: {weather['temperature_night'][i]} ℃"
        await callback.message.answer(text, parse_mode='HTML')
        await callback.message.delete()


@dp.message_handler(state=States.check_access_state)
async def check_access_def(message: Message, state: FSMContext):
    user_id = message.from_user.id
    access(user_id, message.text)
    if check_access(user_id):
        await state.finish()
        await bot.delete_message(message.chat.id, message.message_id - 1)
        await message.delete()
        await message.answer('<b>Access received</b> - now you can use the bot',
                             parse_mode='HTML')
    else:
        await message.answer('Enter the code again')


@dp.message_handler(state=States.video_state)
@dp.message_handler(state=States.playlist_state)
async def video_def(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['url'] = message.text
    await message.answer('Select the resolution of the downloaded video:',
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton('144p', callback_data='144p'),
                              InlineKeyboardButton('240p', callback_data='240p')],
                             [InlineKeyboardButton('360p', callback_data='360p'),
                              InlineKeyboardButton('480p', callback_data='480p')],
                             [InlineKeyboardButton('720p', callback_data='720p')]
                         ]))


executor.start_polling(dp, skip_updates=True)

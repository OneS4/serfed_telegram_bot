from bot_importation_and_ostal import *


async def on_startup(_):
    global botname, bot_id
    await bot.set_my_commands([
        BotCommand('on_del_login', 'Enable deletion of group member login messages'),
        BotCommand('on_del_exit',
                   'Enable the deletion of the exit messages of the participants from the group'),
        BotCommand('off_del_login', 'Disable deletion of group member login messages'),
        BotCommand('off_del_exit',
                   'Disable the deletion of the exit messages of the participants from the group'),
    ], bot_command_scope.BotCommandScopeAllChatAdministrators())
    await bot.set_my_commands([
        BotCommand('video', 'Download videos from YouTube'),
        BotCommand('playlist',
                   'Download playlist from YouTube'),
        BotCommand('weather', 'Find out the weather'),
        BotCommand('files',
                   'Manage your remote files'),
    ], bot_command_scope.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands([
        BotCommand('call_everyone', 'Call everyone in the group')
    ], bot_command_scope.BotCommandScopeAllGroupChats())
    botname = '@' + (await bot.me)['username']
    bot_id = (await bot.me)['id']


@dp.message_handler(content_types=['new_chat_members'])
async def new_member_def(message: Message):
    add_new_user_call_all(message['new_chat_member']['id'], message.chat.id)
    if check_on_off_new_left_def(message.chat.id, 'new_chat_members'):
        await message.delete()


@dp.message_handler(content_types=['left_chat_member'])
async def left_member_def(message: Message):
    if check_on_off_new_left_def(message.chat.id, 'left_chat_member'):
        await message.delete()


@dp.message_handler(state='*', commands=['cancel'])
async def cancel_def(message: Message, state: FSMContext):
    await state.finish()


@dp.message_handler(
    commands=['start', 'video', 'playlist', 'weather', 'files', 'on_del_login', 'on_del_exit',
              'off_del_login', 'off_del_exit', 'call_everyone'])
async def main(message: Message):
    add_user_db(message.from_user.id)
    check_access_bool = check_access(message.from_user.id)
    if check_access_bool and message.text != '/start':
        # await message.answer('What do you want to do?', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        #     [InlineKeyboardButton('Download content from YouTube', callback_data='youtube')],
        #     [InlineKeyboardButton('Find out the weather', callback_data='weather')]
        # ]))
        if message.from_user.id == message.chat.id:
            if message.text == '/video':
                await message.answer('Send a link to the video:')
                await States.video_state.set()
            elif message.text == '/playlist':
                await message.answer('Send a link to the playlist:')
                await States.playlist_state.set()
            elif message.text == '/weather':
                await message.answer('Choose a city:', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton('Tashkent', callback_data='tashkent-5331'),
                     InlineKeyboardButton('Kungrad', callback_data='kungrad-323387')],
                    [InlineKeyboardButton('Moscow', callback_data='moscow-4368'),
                     InlineKeyboardButton('Kazan', callback_data='kazan-4364')],
                    [InlineKeyboardButton('Minsk', callback_data='minsk-4248')]
                ]))
            elif message.text == '/files':
                if not os.path.isdir(f"user_files/{message.from_user.id}"):
                    os.mkdir(f"user_files/{message.from_user.id}")
                list_files = ''
                os.chdir(f"user_files/{message.from_user.id}")
                for dirpach, dirnames, dirfiles in os.walk(f'.'):
                    if dirfiles:
                        list_files += 'There are files' + '\n'
                    else:
                        list_files += 'There are no files' + '\n'
                    for dirname in dirnames:
                        list_files += 'Catalog: ' + os.path.join(dirpach, dirname) + ' - '
                os.chdir('../../')
                await message.answer((list_files or 'Empty'), reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton('Create a directory', callback_data='create_dir'),
                     InlineKeyboardButton('Delete a directory', callback_data='delete_dir')],
                    [InlineKeyboardButton('Load files', callback_data='load_files'),
                     InlineKeyboardButton('Upload files', callback_data='upload_files')]
                ]))
        elif message.text in map(lambda x: x + f'{botname}',
                                 ['/on_del_login', '/on_del_exit', '/off_del_login', '/off_del_exit']):
            if message.chat.id != message.from_user.id and \
                    message.from_user.id in [user_id['user']['id'] \
                                             for user_id in (await message.chat.get_administrators())]:
                new_left_del(message.chat.id, message.text, botname)
                await message.delete()
        elif message.text == '/call_everyone':
            users_list = ''
            for i, user in enumerate(call_all(message.chat.id,
                                              filter(lambda admin: admin != bot_id, [admin['user']['id'] for admin in (
                                                      await message.chat.get_administrators())]))):
                if i != 0:
                    users_list += '\n'
                users_list += f'[Account](tg://user?id={user})'
            await message.answer(users_list, parse_mode=ParseMode.MARKDOWN_V2)
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
    elif callback.data in ['tashkent-5331', 'kungrad-323387', 'moscow-4368', 'kazan-4364', 'minsk-4248']:
        weather = find_weather(callback.data)
        text = ''
        for i in range(14):
            if i != 0:
                text += '\n\n'
            text += f"<b>{weather['days'][i]}</b>\n{weather['weather'][i]}\nДнём: {weather['temperature_day'][i]} ℃\n" \
                    f"Ночью: {weather['temperature_night'][i]} ℃"
        await callback.message.answer(text, parse_mode='HTML')
        await callback.message.delete()
    elif callback.data == 'create_dir':
        await States.create_dir.set()
        await callback.message.answer('Enter the folder name:')
    elif callback.data == 'delete_dir':
        await States.delete_dir.set()
        await callback.message.answer('Enter the folder name:')
    elif callback.data == 'load_files':
        await States.load_files.set()
        await callback.message.answer('Enter the folder name:')
    elif callback.data == 'upload_files':
        await States.upload_files.set()
        await callback.message.answer('Enter the folder name:')
    await callback.answer()


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


@dp.message_handler(state=[States.create_dir, States.delete_dir])
async def create_delete_dir_def(message: Message, state: FSMContext):
    if (await state.get_state()) == 'States:create_dir':
        # noinspection PyBroadException
        try:
            if not os.path.isdir(f"user_files/{message.from_user.id}/{message.text}"):
                os.makedirs(f"user_files/{message.from_user.id}/{message.text}")
        except:
            await message.answer('Failed to create directory')
    elif (await state.get_state()) == 'States:delete_dir':
        # noinspection PyBroadException
        try:
            if os.path.isdir(f"user_files/{message.from_user.id}/{message.text}"):
                shutil.rmtree(f"user_files/{message.from_user.id}/{message.text}")
        except:
            await message.answer('Failed to delete directory')
    await state.finish()


@dp.message_handler(state=[States.load_files, States.upload_files])
async def load_upload_files_def(message: Message, state: FSMContext):
    global path
    if (await state.get_state()) == 'States:load_files':
        # noinspection PyBroadException
        try:
            if not os.path.isdir(f"user_files/{message.from_user.id}/{message.text}"):
                os.makedirs(f"user_files/{message.from_user.id}/{message.text}")
            path = f"user_files/{message.from_user.id}/{message.text}"
            await States.send_files.set()
            await message.answer('Send your files, then use the /cancel command to complete:')
        except:
            await state.finish()
            await message.answer('Failed to create directory')
    else:
        # noinspection PyBroadException
        try:
            path = f"user_files/{message.from_user.id}/{message.text}"
            dirfiles = os.listdir(path)
            files = []
            for i, file in enumerate([(path + '/' + file) for file in dirfiles]):
                if os.path.isfile(file):
                    files.append(dirfiles[i])
            for document in files:
                await message.answer_document(document)
            await state.finish()
        except:
            await state.finish()
            await message.answer('This directory was not found')


@dp.message_handler(state=States.send_files, content_types=['document'])
async def send_files_def(message: Message):
    global path
    open(f'{path}/{message.document.file_id}', 'w')


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

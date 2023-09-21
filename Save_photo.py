# Сохранения фото пользователя как файла
# @bot.message_handler(content_types=['photo'])
# def save_profile_photo_file(message: Message):
#     try:
#         file_photo = bot.get_file(message.photo[0].file_id)
#         file_name, file_extension = os.path.splitext(file_photo.file_path)
#         downloaded_file_photo = bot.download_file(file_photo.file_path)
#
#         src = 'photos_profiles/' + message.photo[0].file_id + file_extension
#         with open(src, 'wb') as new_file:
#             new_file.write(downloaded_file_photo)
#     except TypeError:
#         pass
#

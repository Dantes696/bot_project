from telebot.types import InputMediaPhoto
from queries import get_category_photos, get_product_photos



def input_media_group_photos(category_id):
    photos = get_category_photos(category_id)
    cat_photos = []
    for f in photos:
        cat_photos.append(InputMediaPhoto(f))

    return cat_photos

def input_group_photos(category_id):
    photos = get_category_photos(category_id)
    products_photos = []
    for f in photos:
        products_photos.append(InputMediaPhoto(f))

    return  products_photos
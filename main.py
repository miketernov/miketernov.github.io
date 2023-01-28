import logging
import random
import os
from tokens import token
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

df = pd.DataFrame(columns=['Chat_id', 'First_name', 'Username', 'Last date of using'])

#функция старта
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    username = update.message.chat.username
    date_use = datetime.now().replace(microsecond=0)
    new_df = [chat_id, first_name, username, date_use]
    #проверка на присутствие пользователя в базе
    #проверка на пустой датафрейм
    if df.empty:
        df.loc[len(df)] = new_df
    else:
        if chat_id in df['Chat_id'].tolist():
            row_index = df.loc[df['Chat_id'] == chat_id].index
            df.loc[row_index, 'Last date of using'] = date_use
        else:
            df.loc[len(df)] = new_df

    #сохранение в файл
    df.to_excel('people.xlsx')

    #выбор рандомной картинки
    directory = 'images/' + random.choice(os.listdir('images'))
    im = Image.open(directory)
    drawer = ImageDraw.Draw(im)
    W, H = im.size

    if W > 1500:
        font = ImageFont.truetype('C:/Windows/Fonts/Corbel.ttf', 110)
    elif W > 700:
        font = ImageFont.truetype('C:/Windows/Fonts/Corbel.ttf', 60)
    else:
        font = ImageFont.truetype('C:/Windows/Fonts/Corbel.ttf', 30)

    w, h = drawer.textsize('Текущая дата и время \n{}'.format(datetime.now().replace(microsecond=0)), font=font)
    w_res = (W - w) / 2
    h_res = (H-h) / 2
    #создание красных границ
    drawer.text((w_res - 2, h_res - 2), 'Текущая дата и время \n{}'.format(datetime.now().replace(microsecond=0)),
                font=font, fill="red")
    drawer.text((w_res + 2, h_res - 2), 'Текущая дата и время \n{}'.format(datetime.now().replace(microsecond=0)),
                font=font, fill="red")
    drawer.text((w_res - 2, h_res + 2), 'Текущая дата и время \n{}'.format(datetime.now().replace(microsecond=0)),
                font=font, fill="red")
    drawer.text((w_res + 2, h_res + 2), 'Текущая дата и время \n{}'.format(datetime.now().replace(microsecond=0)),
                font=font, fill="red")
    drawer.text((w_res, h_res), 'Текущая дата и время \n{}'.format(datetime.now().replace(microsecond=0)), font=font,
                fill='yellow')
    im_new = 'C:/images/New_photo.jpg'
    im.save(im_new)
    await update.message.reply_photo(im_new)
    os.remove(im_new)


def main() -> None:
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()


if __name__ == "__main__":
    main()
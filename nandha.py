

import shelve
import logging
import os

from pyrogram import filters, types, Client


logging.basicConfig(level=logging.INFO)

class Database(object):

       @staticmethod
       def get_all_chats() -> list:
            with shelve.open("chat_data.db") as db:
                 return list(db.keys())

       @staticmethod
       def update_spawn_count(chat_id: str, value: int) -> int:
            with shelve.open("chat_data.db") as db:
                 db[chat_id] = value
                 return True                  

       @staticmethod
       def remove_chat(chat_id: str) -> bool:
             with shelve.open("chat_data.db") as db:
                  if chat_id in db:
                      del db[chat_id]
                      return True
                  return False

       @staticmethod
       def get_spawn_count(chat_id: str) -> int:
           chats = Database.get_all_chats()
           if chat_id in chats:
                with shelve.open("chat_data.db") as db:
                       return db.get(chat_id, 0)


                  
               
           

username = "TamilKuralBot"

bot = Client(
    name=username,
    api_id=int(os.getenv("API_ID", 0)),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("TOKEN")
)


db = Database()

temp = {}
temp["chat_ids"] = db.get_all_chats()

@bot.on_message(filters.command("start"))
async def _start(_, message):
      user = message.from_user
      if not user: return # To avoid channel and anonymous users
      text = \
f"""
Hello user ( {user.mention} ), 

I'm **tamil kural** ( தமிழ் குறள் ) Bot!
I can spawn **thirukkural** ( திருக்குறள் ) into your chat
To **submit** me in your group **press the below button**
thank you for using me. by @NandhaBots
"""
      button = types.InlineKeyboardMarkup([[types.InlineKeyboardButton(text="✨ Add Me To Group ✨", url=f"t.me/{username}?startgroup=True")]])
      return await message.reply_text(text, reply_markup=button)



async def can_set_spawn(chat, user):
      try:
        info = await chat.get_member(user.id)
        privilege = bool(getattr(info.privileges, "can_manage_chat", False)) if bool(getattr(info, "privileges", False)) is True else False
        return privilege
      except Exception as error:
           logging.error(str(error))
           return False


@bot.on_message(filters.command("setspawn"))
async def _setspawn(_, message):
       user = message.from_user
       if not user: return # no channel/anonymous is allowed to use
       chat = message.chat

       can_set = await can_set_spawn(chat, user)
       if not can_set:
            return await message.reply_text("Sorry, you are not allowed to use this command!")
       else:
            text = message.text
            if len(text.split()) < 2 or (text.split()[1].isdigit() is not True):
                 return await message.reply_text("**Invalid usage**:\n`/setspawn 30`")
            value = int(text.split()[1])
            chat_id = str(chat.id)
            db.update_spawn_count(chat_id, value)
            return await message.reply_text(f"✅ **Successfully updated spawn count for {chat.title} to {value}.**")
         

@bot.on_message(filters.all, group=2)
async def _okDo(_, message):

     chat = message.chat
     chat_id = str(chat.id)
     if chat_id in temp["chat_ids"]:
            if chat_id in temp:
                 msg_count, value = temp[chat_id]
                 if msg_count == value:
                       ...
          
    
      


       
bot.run()

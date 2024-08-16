from characterai import aiocai
import asyncio

class ChatBot:
    def __init__(self):
        self.token_id = None
        self.char_id = None
        self.new_id = None
        self.name_id = None
    async def CreateChar(self,  token:str, char:str):
        self.token_id = token
        async with aiocai.Client(token=self.token_id) as client:
            me = await client.get_me()
            async with await client.connect() as chat:
                new, answer = await chat.new_chat(
                    char, me.id
                )
            self.char_id = char
            self.new_id = new.chat_id
            self.answer_id = answer
            self.name_id = answer.name
            return self.new_id, self.name_id
            
    async def Send_msg(self, your_msg:str,char_id:str, chat_id:str, token:str):
        async with aiocai.Client(token=token) as client:
            async with await client.connect() as chat:
                message = await chat.send_message(
                    char_id, chat_id, your_msg
                )

                print(f'{message.name}: {message.text}')
                return message.name, message.text
        

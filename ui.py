import customtkinter
import os
import asyncio, json, queue
import tkinter as tk
import threading

"""from aiGirlfriend.main import Types"""
from characterAI.chat import ChatBot
from PIL import Image

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.character_window = None
        self.title("AIFU V0.01")
        self.geometry("1200x700")
        
        """self.types = Types()"""
        self.chatBot = ChatBot()
        """self.dropdown_values = ["en-US-AvaNeural", 
                                "en-US-AndrewNeural", 
                                "en-US-EmmaNeural",
                                "en-US-BrianNeural",
                                "en-US-JennyNeural",
                                "en-US-GuyNeural",
                                "en-US-AriaNeural",
                                "en-US-DavisNeural",
                                "en-US-JaneNeural",
                                "en-US-JasonNeural",
                                "en-US-SaraNeural",
                                "en-US-TonyNeural",
                                "en-US-NancyNeural",
                                "en-US-AmberNeural",
                                "en-US-AnaNeural",
                                "en-US-AshleyNeural",
                                "en-US-BrandonNeural",
                                "en-US-ChristopherNeural",
                                "en-US-CoraNeural",
                                "en-US-ElizabethNeural",
                                "en-US-EricNeural",
                                "en-US-JacobNeural",
                                "en-US-MonicaNeural"
                                ]"""

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        logo_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logos")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(logo_path, "logo_aifu.png")), size=(106, 56))
        self.logo_homePage = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo_homePage.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.mic_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "microphone_dark.png")),
                                            dark_image=Image.open(os.path.join(image_path, "microphone_light.png")), size=(20, 20))
        self.plus_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "plus_dark.png")),
                                            dark_image=Image.open(os.path.join(image_path, "plus_light.png")), size=(20, 20))
        self.reload_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "reload_dark.png")),
                                            dark_image=Image.open(os.path.join(image_path, "reload_light.png")), size=(20, 20))
        self.send_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "send_dark.png")),
                                            dark_image=Image.open(os.path.join(image_path, "send_light.png")), size=(20, 20))
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(20, weight=1)

        self.navigation_frame_label = customtkinter.CTkButton(self.navigation_frame,text="", image=self.logo_image,
                                                             compound="left", command=self.main_menu, fg_color="transparent", hover_color="#313131")
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20  )

        """self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        self.add_character_navMenu = customtkinter.CTkButton(self.navigation_frame,text="",image=self.plus_image, command=self.open_toplevel)
        self.add_character_navMenu.grid(row=5, column=0, padx=20, pady=20)"""

        if os.path.exists("characters.json"):
            try:
                with open("characters.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"ERROR: {e}")
                data = {}
        else:
            data = {}

        self.name_buttons = []

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid(row=0, column=1, sticky="nsew")
        
        self.home_frame_button_4 = customtkinter.CTkButton(self.home_frame, text="Create a new Chat or\nSelect an Existing one", 
                                                           image=self.plus_image, compound="right", anchor="w", 
                                                           fg_color="transparent", hover_color="#313131",command=self.open_toplevel)
        self.home_frame_button_4.grid(row=0, column=0, padx=20, pady=10)

        self.Rreload = customtkinter.CTkButton(self.home_frame, text="", image=self.reload_image, fg_color="transparent",hover_color="#2d2d2d", command=self.reload)
        self.Rreload.grid(row=2, column=0, padx=20, pady=20, sticky="s")

        self.load_characters()  # Call load_characters after home_frame is created

        self.toplevel_window = None
        self.select_frame_by_name("home")

    def load_characters(self):
        if os.path.exists("characters.json"):
            try:
                with open("characters.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"ERROR: {e}")
                data = {}
        else:
            data = {}

        def extract_names(d):
            names = []
            if isinstance(d, dict):
                for key, value in d.items():
                    if key == "name":
                        names.append(value)
                    else:
                        names.extend(extract_names(value))
            elif isinstance(d, list):
                for item in d:
                    names.extend(extract_names(item))
            return names

        name_values = extract_names(data)
        for index, name in enumerate(name_values):
            row = index 
            column = 0   # Tek sütun
            button = customtkinter.CTkButton(
                self.navigation_frame, text=name, command=lambda n=name: self.open_conversation_window(n)
            )
            button.grid(row=row + 1, column=column, padx=10, pady=10, sticky="ew")
            self.name_buttons.append(button)
            
    def reload(self):
        if os.path.exists("characters.json"):
            try:
                with open("characters.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"ERROR: {e}")
                data = {}
        else:
            data = {}

        def extract_names(d):
            names = []
            if isinstance(d, dict):
                for key, value in d.items():
                    if key == "name":
                        names.append(value)
                    else:
                        names.extend(extract_names(value))
            elif isinstance(d, list):
                for item in d:
                    names.extend(extract_names(item))
            return names
        name_values = extract_names(data)

        for index, name in enumerate(name_values):
            row = index 
            column = 0   # Tek sütun
            button = customtkinter.CTkButton(
                self.navigation_frame, text=name, command=lambda n=name: self.open_conversation_window(n)
            )
            button.grid(row=row + 1, column=column, padx=10, pady=10, sticky="ew")
            self.name_buttons.append(button)
    def main_menu(self):
        if not self.home_frame_button_4 and not self.Rreload:
            self.home_frame_button_4.grid(row=0, column=0, padx=20, pady=10)
            self.Rreload.grid(row=2, column=0, padx=0, pady=0, sticky="s")
        else:
            self.home_frame.grid_rowconfigure(0, weight=0)
            self.home_frame.grid_rowconfigure(0, weight=0)  
            self.home_frame.grid_columnconfigure(0, weight=1)
            self.home_frame_button_4.grid(row=0, column=0, padx=20, pady=10)
            self.Rreload.grid(row=2, column=0, padx=20, pady=20, sticky="s")

            self.TextBox.grid_forget()
            self.EntryBox.grid_forget()
            self.SendBtn.grid_forget()

    def fetch_character(self):
        try:
            with open('characters.json', 'r') as file:
                characters = json.load(file)
            return characters
        except Exception as e:
            print(f"Error loading characters: {e}")
            return None
    
    def get_character_details(self, name):
        characters = self.fetch_character()
        if characters is None:
            print("Character list could not be loaded.")
            return None
        
        for character in characters:
            if character['name'] == name:
                return character
        return None
    
    def open_character(self, name):
        character = self.get_character_details(name)
        if character is None:
            print("Character not found.")
            return
        
        if self.character_window and self.character_window.winfo_exists():
            self.character_window.lift()
            return
        
        self.character_window = customtkinter.CTkToplevel(self)
        self.character_window.title(f"Character Details: {name}")
        self.character_window.geometry("300x200")
        
        details_frame = customtkinter.CTkFrame(self.character_window, corner_radius=10)
        details_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        name_label = customtkinter.CTkLabel(details_frame, text=f"Name: {name}", font=("Arial", 16))
        name_label.pack(pady=10)
        
        chat_id_label = customtkinter.CTkLabel(details_frame, text=f"Chat ID: {character['chat_id']}", font=("Arial", 12))
        chat_id_label.pack(pady=10)
        
        close_button = customtkinter.CTkButton(details_frame, text="Close", command=self.character_window.destroy)
        close_button.pack(pady=10)

    def open_conversation_window(self, name):
        character = self.get_character_details(name)
        if character is None:
            print("Character not found.")
            return
        
        if self.character_window and self.character_window.winfo_exists():
            self.character_window.lift()
            return
        
        self.Rreload.grid_forget()
        self.home_frame_button_4.grid_forget()
        self.home_frame.grid_rowconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(1, weight=0)  
        self.home_frame.grid_columnconfigure(1, weight=0)

        self.TextBox = customtkinter.CTkTextbox(self.home_frame, corner_radius=0)
        self.TextBox.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        self.EntryBox = customtkinter.CTkEntry(self.home_frame, corner_radius=0)
        self.EntryBox.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.SendBtn = customtkinter.CTkButton(self.home_frame, text="Send", corner_radius=0, image=self.send_image, compound="right", 
                                               command=lambda n=name: self.SendButton(n))
        self.SendBtn.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def SendButton(self, name):
        self.SendBtn.configure(state="disabled")
        character = self.get_character_details(name)
        if character is None:
            print("Character not found.")
            return

        if self.character_window and self.character_window.winfo_exists():
            self.character_window.lift()
            return

        msg = self.EntryBox.get()
        chat_id = character["chat_id"]
        char_id = character["char"]
        token = character["token"]

        # Start a new thread to send the message
        thread = threading.Thread(target=self.threaded_send_message, args=(msg, char_id, chat_id, token))
        thread.start()

        self.EntryBox.delete(0, "end")

    def threaded_send_message(self, msg, char_id, chat_id, token):
        result = asyncio.run(self.chatBot.Send_msg(msg, char_id, chat_id, token))
        message_name, message_text = result
        self.update_textbox(msg, message_name, message_text)

    def update_textbox(self, msg, message_name, message_text):
        self.TextBox.insert("end", f"You: {msg}" + "\n")
        self.TextBox.insert("end", f"{message_name}: {message_text}" + "\n")
        self.SendBtn.configure(state="enabled")

    def select_frame_by_name(self, name):
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

        """if name == "Text Input":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

        if name == "Audio Input":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()"""

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = characterADD(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
    def option_menu_event(self, choice):
        # Seçilen değeri terminale yazdırır
        print(f"Selected Option: {choice}")

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("Text Input")

    def frame_3_button_event(self):
        self.select_frame_by_name("Audio Input")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

class characterADD(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chatbot = ChatBot()
        
        self.title("AIFU CHARADD V0.01")
        self.geometry("400x300")



        self.add_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.add_frame.grid(row=0, column=0)

        self.Label_characterAIChatToken = customtkinter.CTkLabel(self.add_frame, text="CharacterAI Token:")
        self.Label_characterAIChatToken.grid(row=0, column=0, padx=10, pady=10)

        self.characterAIChatToken = customtkinter.CTkEntry(self.add_frame, placeholder_text="CharacterAI Token ID..")
        self.characterAIChatToken.grid(row=0, column=2, padx=10, pady=10)

        self.Label_characterID = customtkinter.CTkLabel(self.add_frame, text="CharacterAI ID:")
        self.Label_characterID.grid(row=2, column=0, padx=10, pady=10)

        self.characterID = customtkinter.CTkEntry(self.add_frame, placeholder_text="CharacterAI ID..")
        self.characterID.grid(row=2, column=2, padx=10, pady=10)

        self.characterSave = customtkinter.CTkButton(self.add_frame, text="Save", command=self.save)
        self.characterSave.grid(row=3, column=2, padx=10, pady=10)

    def load_data(self):
        try:
            with open("characters.json", "r") as json_file:
                data = json.load(json_file)
            #self.characterAIChatToken.set(data["token"])
           # self.characterID.set(data["char"])
        except FileNotFoundError:
            print("settings.json dosyası bulunamadı.")
        except json.JSONDecodeError:
            print("settings.json dosyası okunurken bir hata oluştu.")


    def run_async(self, token, char, result_queue):
        async def async_task():
            result = await self.chatbot.CreateChar(token, char)
            result_queue.put(result)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(async_task())
        loop.close()

    def save(self):
        token = self.characterAIChatToken.get()
        char = self.characterID.get()
        
        if not token or not char:
            self.ERROR = customtkinter.CTkLabel(self.add_frame, text="ERROR!", fg_color="red")
            self.ERROR.grid(row=4, column=2, padx=10, pady=10)
        else:
            print(token)
            print(char)
            result_queue = queue.Queue()
            thread = threading.Thread(target=self.run_async, args=(token, char, result_queue))
            thread.start()
            thread.join() 
            result = result_queue.get()
            chat_id, name = result
            data = {
                "token": token,
                "char": char,
                "chat_id": chat_id,
                "name": name
            }
        if os.path.exists("characters.json"):
            try:
                with open("characters.json", "r", encoding="utf-8") as json_file:
                    existing_data = json.load(json_file)
                    if not isinstance(existing_data, list):
                        existing_data=[]
            except Exception as e:
                print(f"ERROR: {e}")
                existing_data = []
        else:
            existing_data = []

        existing_data.append(data)
        with open("characters.json", "w", encoding="utf-8") as json_file:
            json.dump(existing_data, json_file, indent=4, ensure_ascii=False)
        print(chat_id, name)


if __name__ == "__main__":
    app = App()
    app.iconbitmap("images/g.ico")
    app.mainloop()

import io
import webbrowser
import requests
from tkinter import *
import random
from urllib.request import urlopen
from PIL import ImageTk, Image
import os

class NewsApp:

    def __init__(self):
        
        # fetch data
        self.data = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=07ce6431517e45c5b04b589c36e5bed6').json()
        # initial GUI load
        self.load_gui()
        # load the 1st news item
        self.load_news_item(0)

    def load_gui(self):
        self.root = Tk()
        self.root.geometry('350x600')
        self.root.resizable(0, 0)
        self.root.title('Pheme')
        self.root.configure(background='white')

    # Generate a random hex code
    def random_hex(self):
        return '#' + ''.join(random.choices('0123456789ABCDEF', k=6)) 

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def load_news_item(self, index):
        # clear the screen for the new news item
        self.clear()

        # image
        try:
            img_url = self.data['articles'][index]['urlToImage']
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((350, 250))
            photo = ImageTk.PhotoImage(im)
        except:
                folder_path = r"\\DESKTOP-5KOOM96\Users\DELL\Desktop\Photos for Newsapp"
                image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                image_files = [f for f in image_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
               
                random_image = random.choice(image_files)
                image_path = os.path.join(folder_path, random_image)
                
                im = Image.open(image_path).resize((350, 250))
                photo = ImageTk.PhotoImage(im)


            

        title = Label(self.root, text="Pheme\nReport • Rumour • Gossip", bg='black', fg='white', justify='center')
        title.pack(pady=(10, 10))
        title.config(font=('Arial', 12, 'bold'), padx=80, pady=0)

        label = Label(self.root, image=photo)
        label.pack()

        heading = Label(self.root, text=self.data['articles'][index]['title'], bg='white', fg='black', wraplength=340, justify='center')
        heading.pack(pady=(10, 20))
        heading.config(font=('roboto', 12, "bold"))

        if 'description' in self.data['articles'][index] and self.data['articles'][index]['description']:
            details_text = self.data['articles'][index]['description']
        else:
            details_text = f"The requested information can not be retrieved at the moment.\nFor further details regarding the news, please click on read more"

            details = Label(self.root, text=details_text, bg='white', fg='red', wraplength=320, justify='left')
            details.pack(pady=(4, 60))
            details.config(font=('Roboto', 10))
        
        if details_text.strip() == "":
            details_text = "Error"

        details = Label(self.root, text=details_text, bg='white', fg='black', wraplength=320, justify='left')
        details.pack(pady=(4, 60))
        details.config(font=('Roboto', 10))

        frame = Frame(self.root, bg=self.random_hex())
        frame.place(x=0, y=550, relwidth=1, relheight=0.1)

        if index != 0:
            prev = Button(frame, text='Prev', width=10, height=2, command=lambda: self.load_news_item(index-1))
            prev.place(relx=0.1, rely=0.2)
            prev.config(bg='#FFB6C1', fg='black', font=('Roboto', 10))

        read = Button(frame, text='Read More', width=10, height=2, command=lambda: self.open_link(self.data['articles'][index]['url']))
        read.place(relx=0.4, rely=0.2)
        read.config(bg='#90EE90', fg='black', font=('Roboto', 10))

        if index != len(self.data['articles']) - 1:
            next = Button(frame, text='Next', width=10, height=2, command=lambda: self.load_news_item(index+1))
            next.place(relx=0.7, rely=0.2)
            next.config(bg='#FFB6C1', fg='black', font=('Roboto', 10))

        self.root.mainloop()

    def open_link(self, url):
        webbrowser.open(url)

obj = NewsApp()

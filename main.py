import requests
import sqlite3
from bs4 import BeautifulSoup

# connect to database
conn = sqlite3.connect('games.db')
cur = conn.cursor()

# create table Games
cur.execute('''CREATE TABLE IF NOT EXISTS Games(
    Name TEXT PRIMARY KEY,
    Price REAL
) ''')

# game links to get prices
links = [
    "https://www.gamivo.com/product/grand-theft-auto-v-gta-5",
    "https://www.gamivo.com/product/efootball-pes-2020",
    "https://www.gamivo.com/product/rocket-league"
]

headers = {
    "User-Agent" : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}

# get price for each game
for link in links:
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    price = soup.find("div", {"class": "price lowest-price"}).get_text()
    converted_price = float(price[2:])
    title = soup.title.string[3:]

    # print game prices
    print("Name: " + title + " | Price: " + '\033[91m' + price + '\033[0m')

    # save data in database
    try:
        cur.execute('''INSERT INTO Games 
                    (Name, Price) VALUES(?, ?)''', 
                    (title, converted_price))
        conn.commit()
        
    # update data if game is in database
    except sqlite3.IntegrityError:
        cur.execute('''UPDATE Games
                       SET 
                        Price = (?)
                       WHERE 
                        Name = (?) ''',
                        (converted_price,title)
        )
        conn.commit()

    
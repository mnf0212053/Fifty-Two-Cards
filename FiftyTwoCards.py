import sqlite3

con = sqlite3.connect("card52.db")

def create_cards(conn):
    sql_delete_table = ''' DROP TABLE IF EXISTS cards; '''
    sql_create = """ CREATE TABLE IF NOT EXISTS cards(
        id integer PRIMARY KEY,
        rank text,
        suit text,
        possession text
    ); """

    cur = conn.cursor()
    cur.execute(sql_delete_table)
    cur.execute(sql_create)
    
    sql_insert = ''' INSERT INTO cards(rank, suit, possession) VALUES (?, ?, ?) '''

    suits = ('Heart', 'Diamond', 'Club', 'Spade')
    royal_ranks = ('Ace', 'King', 'Queen', 'Jack')

    for royal in royal_ranks:
        for suit in suits:
            sql_cards_data = (royal, suit, 'None')
            cur.execute(sql_insert, sql_cards_data)

    for lower_ranks in range(2, 11):
        for suit in suits:
            sql_cards_data = (str(12 - lower_ranks), suit, 'None')
            cur.execute(sql_insert, sql_cards_data)
    conn.commit()


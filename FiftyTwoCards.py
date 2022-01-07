import sqlite3
import numpy as np

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

def create_dealer(conn):
    sql_delete_table = ''' DROP TABLE IF EXISTS dealer; '''
    sql_create = """ CREATE TABLE IF NOT EXISTS dealer(
        id integer PRIMARY KEY,
        card_rank text,
        card_suit text
    ); """

    cur = conn.cursor()
    cur.execute(sql_delete_table)
    cur.execute(sql_create)

def shuffle_numbers():
    rand_nums = []
    
    for i in range(0, 52):
        rand_num = np.random.randint(1, 1000)
        while rand_nums.__contains__(rand_num):
            rand_num = np.random.randint(1, 1000)
        rand_nums.append(rand_num)

    rand_nums_sorted = sorted(rand_nums)
    rand_52 = []

    for i in range(0, len(rand_nums)):
        for j in range(0, len(rand_nums_sorted)):
            if rand_nums[i] == rand_nums_sorted[j]:
                rand_52.append(j + 1)

    return rand_52






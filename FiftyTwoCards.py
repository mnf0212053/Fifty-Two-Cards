import sqlite3
import numpy as np

def db_connect():
    return sqlite3.connect("card52.db")

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
    
    suits = ('\u0003', '\u0004', '\u0005', '\u0006')
    royal_ranks = (' A', ' K', ' Q', ' J', '10')

    for royal in royal_ranks:
        for suit in suits:
            sql_cards_data = (royal, suit, 'None')
            cur.execute(sql_insert, sql_cards_data)

    for lower_ranks in range(2, 10):
        for suit in suits:
            sql_cards_data = (' ' + str(11 - lower_ranks), suit, 'None')
            cur.execute(sql_insert, sql_cards_data)
    conn.commit()

def create_dealer(conn):
    sql_delete_table = ''' DROP TABLE IF EXISTS dealer; '''
    sql_create = """ CREATE TABLE IF NOT EXISTS dealer(
        id integer PRIMARY KEY,
        card_rank text,
        card_suit text
    ); """
    sql_insert_stats = ''' INSERT INTO stats(character, total_cards) VALUES (?, ?) '''
    sql_data_stats = ('dealer', 0)

    cur = conn.cursor()
    cur.execute(sql_delete_table)
    cur.execute(sql_create)
    cur.execute(sql_insert_stats, sql_data_stats)
    conn.commit()

def create_player(conn):
    sql_delete_table = ''' DROP TABLE IF EXISTS player; '''
    sql_create = """ CREATE TABLE IF NOT EXISTS player(
        id integer PRIMARY KEY,
        card_rank text,
        card_suit text
    ); """
    sql_insert_stats = ''' INSERT INTO stats(character, total_cards) VALUES (?, ?) '''
    sql_data_stats = ('player', 0)

    cur = conn.cursor()
    cur.execute(sql_delete_table)
    cur.execute(sql_create)
    cur.execute(sql_insert_stats, sql_data_stats)
    conn.commit()

def create_stats(conn):
    sql_delete_table = ''' DROP TABLE IF EXISTS stats; '''
    sql_create = """ CREATE TABLE IF NOT EXISTS stats(
        id integer PRIMARY KEY,
        character text,
        total_cards integer
    ); """

    cur = conn.cursor()
    cur.execute(sql_delete_table)
    cur.execute(sql_create)

def init(conn):
    create_cards(conn)
    create_stats(conn)
    create_dealer(conn)
    create_player(conn)

def shuffle_numbers(cmnt = 52):
    rand_nums = []
    
    for i in range(0, cmnt):
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

def get_card(conn, cid):
    sql_retrieve = ''' SELECT rank, suit FROM cards WHERE id = ?; '''

    cur = conn.cursor()
    cur.execute(sql_retrieve, (cid,))

    return cur.fetchall()

def shuffle_cards(conn):
    sql_delete_dealer_cards = ''' DELETE FROM dealer '''

    card_id_lists = shuffle_numbers()
    sql_insert = ''' INSERT INTO dealer(card_rank, card_suit) VALUES (?, ?) '''

    cur = conn.cursor()
    cur.execute(sql_delete_dealer_cards)

    for i in range(0, len(card_id_lists)):
        sql_get_card = get_card(conn, card_id_lists[i])
        cur.execute(sql_insert, sql_get_card[0])
    conn.commit()

def get_card_amount(conn, chr):
    sql_chr_search = '''SELECT total_cards FROM stats WHERE character = ?; '''

    cur = conn.cursor()
    cur.execute(sql_chr_search, (chr,))

    chr_data = cur.fetchall()
    if len(chr_data) == 0:
        print('Character Not Found')
        return -1
    else:
        for x in chr_data:
            card_amount = x[0]
        return card_amount

def update_stats(conn):
    sql_chr_count = '''SELECT character FROM stats; '''
    sql_update_stats = ''' UPDATE stats SET total_cards = ? WHERE character = ?; '''

    cur = conn.cursor()
    cur.execute(sql_chr_count)

    chr_data = cur.fetchall()
    for x in chr_data:
        sql_look_chr = 'SELECT COUNT(*) FROM ' + x[0] +'; '
        cur.execute(sql_look_chr)
        t_cards = cur.fetchone()

        sql_update_data = (t_cards[0], x[0])
        cur.execute(sql_update_stats, sql_update_data)
    conn.commit()

def card_transfer(conn, chr1, chr2, cnum):
    sql_get_src_cards = ' SELECT card_rank, card_suit FROM ' + chr1 + ' WHERE id = ?;'
    sql_add_cards_dst = ' INSERT INTO ' + chr2 + '(card_rank, card_suit) VALUES (?, ?) '
    sql_del_src_cards = ' DELETE FROM ' + chr1 + ' WHERE id = ?;'
    sql_select_min_src = ' SELECT MIN(id) FROM ' + chr1
    cur = conn.cursor()

    cur.execute(sql_select_min_src)

    minid = cur.fetchone()
    for n in range(0, cnum):
        sql_card_id = (n + minid[0],)
        cur.execute(sql_get_src_cards, sql_card_id)

        cards_trf = cur.fetchone()
        cur.execute(sql_add_cards_dst, cards_trf)
        cur.execute(sql_del_src_cards, sql_card_id)

    conn.commit()

def render_cards(curs, sql_script, total_cards, min_id):
    for i in range(0, total_cards):
        print('-----', end = '')
    print('-')
    for i in range(0, total_cards):
        print('|    ', end = '')
    print('|')
    for c in range(0, total_cards):
        curs.execute(sql_script, (c + min_id,))

        cards = curs.fetchone()
        print('|' + cards[0] + cards[1], end = ' ')
    print('|')
    for i in range(0, total_cards):
        print('|    ', end = '')
    print('|')
    for i in range(0, total_cards):
        print('-----', end = '')
    print('-')

def show_cards(conn):
    sql_get_cards = ''' SELECT card_rank, card_suit FROM player WHERE id = ?; '''
    sql_get_total_cards = ''' SELECT COUNT(*) FROM player; '''
    sql_get_min_id = ''' SELECT MIN(id) FROM player; '''

    cur = conn.cursor()

    cur.execute(sql_get_total_cards)
    n_cards = cur.fetchone()

    cur.execute(sql_get_min_id)
    n_min = cur.fetchone()

    render_cards(cur, sql_get_cards, n_cards[0], n_min[0])

def reveal_cards(conn, chr, cmnt):
    sql_select = ' SELECT card_rank, card_suit FROM ' + chr + ' WHERE id = ?;'
    sql_select_min = ' SELECT MIN(id) FROM ' + chr

    cur = conn.cursor()

    cur.execute(sql_select_min)
    minid = cur.fetchone()
    
    for i in range(0, cmnt):
        print('-----', end = '')
    print('-')
    for i in range(0, cmnt):
        print('|    ', end = '')
    print('|')
    for c in range(0, cmnt):
        cur.execute(sql_select, (c + minid[0],))

        cards = cur.fetchone()
        print('|' + cards[0] + cards[1], end = ' ')
    print('|')
    for i in range(0, cmnt):
        print('|    ', end = '')
    print('|')
    for i in range(0, cmnt):
        print('-----', end = '')
    print('-')
    

import sqlite3
import numpy as np
import os

PATH = r"card52.db"

def create_cards():
    """ create_cards()
        Creates a 'cards' table into the database and fills it with a set of 52-card deck.
        The table consists of id (primary key), card rank, card suit, and card possession (which character possesses the card).
        The preceding table will be deleted.
    """
    conn = sqlite3.connect(PATH)

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

def create_dealer():
    """ create_dealer()
        Creates a 'dealer' table into the database.
        The table consists of id (primary key), card rank, and card suit the dealer possesses.
        The created dealer will be inputed into the stats table.
        The preceding table will be deleted.
    """
    conn = sqlite3.connect(PATH)
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

def create_player():
    """ create_player()
        Creates a 'player' table into the database.
        The table consists of id (primary key), card rank, and card suit the player possesses.
        The created player will be inputed into the stats table.
        The preceding table will be deleted.
    """
    conn = sqlite3.connect(PATH)
    sql_delete_table = ''' DROP TABLE IF EXISTS player; '''
    sql_create = """ CREATE TABLE IF NOT EXISTS player(
        id integer PRIMARY KEY,
        card_rank text,
        card_suit text
    ); """
    sql_insert_stats = ''' INSERT INTO stats(character, total_cards,chips) VALUES (?, ?, ?) '''
    sql_data_stats = ('player', 0, 0)

    cur = conn.cursor()
    cur.execute(sql_delete_table)
    cur.execute(sql_create)
    cur.execute(sql_insert_stats, sql_data_stats)
    conn.commit()

def create_custom(chr):
    """ create_custom( chr)
        Creates a custom 'chr' character table into the database.
        The table consists of id (primary key), card rank, and card suit the character possesses.
        The created character will be inputed into the stats table.
        The preceding table will be deleted.
    """
    conn = sqlite3.connect(PATH)
    sql_delete_table = ' DROP TABLE IF EXISTS ' + chr + '; '
    sql_create = """ CREATE TABLE IF NOT EXISTS """ + chr + """(
        id integer PRIMARY KEY,
        card_rank text,
        card_suit text
    ); """
    sql_insert_stats = ''' INSERT INTO stats(character, total_cards, chips) VALUES (?, ?, ?) '''
    sql_data_stats = (chr, 0, 0)

    cur = conn.cursor()
    cur.execute(sql_delete_table)
    cur.execute(sql_create)
    cur.execute(sql_insert_stats, sql_data_stats)
    conn.commit()

def create_stats():
    """ create_stats()
        Creates a 'stats' table into the database.
        The table consists of id (primary key), character list (e.g. dealer, player), the total cards and chips the corresponding character possesses.
        The preceding table will be deleted.
    """
    conn = sqlite3.connect(PATH)
    sql_delete_table = ''' DROP TABLE IF EXISTS stats; '''
    sql_create = """ CREATE TABLE IF NOT EXISTS stats(
        id integer PRIMARY KEY,
        character text,
        total_cards integer,
        chips integer
    ); """

    cur = conn.cursor()
    cur.execute(sql_delete_table)
    cur.execute(sql_create)

def delete_everything():
    """ delete_everything()
        Remove the database file from computer.
    """
    if os.path.exists(PATH):
        os.remove(PATH)

def init():
    """ init()
        Creates 'cards', 'stats',,'dealer', and 'player' tables respectively to the database.
    """
    create_cards()
    create_stats()
    create_dealer()
    create_player()

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

def add_chips(chr, nch):
    """ add_chips(chr, nch)
        Adds 'nch' amount of chips to 'chr' character.
    """
    sql_update = '''UPDATE stats SET chips = ? WHERE character = ?;'''
    sql_data = (nch, chr)

    conn = sqlite3.connect(PATH)
    cur = conn.cursor()
    cur.execute(sql_update, sql_data)
    conn.commit()

def chips_transfer(chr1, chr2, nch):
    """ chips_transfer(chr1, chr2, nch)
        Transfer 'nch' amount of chips from 'chr1' character to 'chr2' character.
    """
    sql_get_chips = ''' SELECT chips FROM stats WHERE character = ?; '''
    sql_update_chips = ''' UPDATE stats SET chips = ? WHERE character = ?; '''

    conn = sqlite3.connect(PATH)
    cur = conn.cursor()

    cur.execute(sql_get_chips, (chr1,))
    chr1_chips = cur.fetchone()

    cur.execute(sql_get_chips, (chr2,))
    chr2_chips = cur.fetchone()
    
    cur.execute(sql_update_chips, (chr1_chips[0] - nch, chr1))
    cur.execute(sql_update_chips, (chr2_chips[0] + nch, chr2))

    conn.commit()

def get_chips(chr):
    """ get_chips(chr)
        Returns the amount of chips that 'chr' character possess.
    """
    sql_get_chips = ''' SELECT chips FROM stats WHERE character = ?; '''
    
    conn = sqlite3.connect(PATH)
    cur = conn.cursor()
    cur.execute(sql_get_chips, (chr,))

    chips = cur.fetchone()
    return chips[0]

def get_card(cid):
    """ get_card( cid)
        Retrieves a card from 'cards' table in the database with a specific id (cid).
        Returns a tuple containing the card informations.
    """
    conn = sqlite3.connect(PATH)
    sql_retrieve = ''' SELECT rank, suit FROM cards WHERE id = ?; '''

    cur = conn.cursor()
    cur.execute(sql_retrieve, (cid,))

    return cur.fetchall()

def shuffle_cards_dealer():
    """ shuffle_cards_dealer()
        Fills the 'dealer' table with the entire 52-card deck, and shuffle the cards.
        The preceding cards will be deleted.
    """
    conn = sqlite3.connect(PATH)
    sql_delete_dealer_cards = ''' DELETE FROM dealer '''

    card_id_lists = shuffle_numbers()
    sql_insert = ''' INSERT INTO dealer(card_rank, card_suit) VALUES (?, ?) '''

    cur = conn.cursor()
    cur.execute(sql_delete_dealer_cards)

    for i in range(0, len(card_id_lists)):
        sql_get_card = get_card(card_id_lists[i])
        cur.execute(sql_insert, sql_get_card[0])
    conn.commit()

def get_card_amount(chr):
    """ get_card_amount( chr)
        Returns amount of cards possessed by 'chr'.
        Returns -1 if the 'chr' character doesn't exist in the database.
    """
    conn = sqlite3.connect(PATH)
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

def update_stats():
    """ update_stats()
        Updates the 'stats' table in the database.
    """
    conn = sqlite3.connect(PATH)
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

def card_transfer(chr1, chr2, cnum):
    """ card_transfer( chr1, chr2, cnum)
        Performs a card transaction with the amount of 'cnum' from character 'chr1' to character 'chr2'.
    """
    conn = sqlite3.connect(PATH)
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
    """ render_cards(curs, sql_script, total_cards, min_id)
        Generates the more user-friendly card interface that shows the cards to be displayed.
        Requires:
        1. The cursor argument 'curs' from a connection
        2. An 'sql_script' which contains an SQL command to select card from a character
        3. The total cards (total_cards) to be displayed
        4. The least 'id' number from the character's database
    """
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

def show_cards(chr):
    """ show_cards( chr)
        Display the cards possessed by the 'chr' character.
    """
    conn = sqlite3.connect(PATH)
    sql_get_cards = ' SELECT card_rank, card_suit FROM ' + chr +' WHERE id = ?; '
    sql_get_total_cards = ' SELECT COUNT(*) FROM ' + chr + '; '
    sql_get_min_id = ' SELECT MIN(id) FROM ' + chr + '; '

    cur = conn.cursor()

    cur.execute(sql_get_total_cards)
    n_cards = cur.fetchone()

    cur.execute(sql_get_min_id)
    n_min = cur.fetchone()

    print(chr + '\'s card')
    render_cards(cur, sql_get_cards, n_cards[0], n_min[0])

def reveal_cards(chr, cmnt):
    """ reveal_cards( chr, cmnt)
        Display a 'cmnt' amount of cards possessed by 'chr', starting from the least id number.        
    """
    conn = sqlite3.connect(PATH)
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
    

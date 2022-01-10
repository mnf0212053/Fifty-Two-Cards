import FiftyTwoCards as ftc

con = ftc.db_connect()
ftc.init(con)
ftc.shuffle_cards_dealer(con)
ftc.card_transfer(con, "dealer", "player", 2)
ftc.update_stats(con)
ftc.show_cards(con)
ftc.reveal_cards(con, 'dealer', 5)
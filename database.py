import sqlite3
import csv

DB_NAME = 'mtg_cards.db'

db = sqlite3.Connection(DB_NAME)
cur = db.cursor()


def _init_db():
    cur.execute("""CREATE TABLE CARDS (CARD_NAME TEXT, PRICE_EUR NUMBER,
                PRICE_USD NUMBER, QTY NUMBER)""")
    cur.execute("CREATE UNIQUE INDEX I1 ON CARDS (CARD_NAME)")
    db.commit()


def _drop_db():
    try:
        cur.execute("DROP INDEX I1")
        cur.execute("DROP TABLE CARDS")
    except sqlite3.OperationalError as e:
        print("WARN : {}".format(e))


def _reset_db():
    _drop_db()
    _init_db()


def card_exists(card_name):
    res = cur.execute("SELECT 1 FROM CARDS WHERE CARD_NAME == :card_name",
                      {'card_name': card_name})

    return True if res.fetchone() else False


def insert_card(card_name, price_eur, price_usd, qty=1):
    cur.execute("""INSERT INTO CARDS (CARD_NAME, PRICE_EUR, PRICE_USD
                    , QTY) VALUES (:card_name, :price_eur, :price_usd, :qty)
                    """, {'card_name': card_name, 'price_eur': price_eur,
                          'price_usd': price_usd, 'qty': qty})
    db.commit()


def update_card_qty(card_name, qty=1):
    cur.execute("""UPDATE CARDS SET QTY = QTY + :nb_cards WHERE
                CARD_NAME = :card_name""", {'card_name': card_name,
                                            'nb_cards': qty})
    db.commit()


def export_cards_as_csv(csv_name):
    data = cur.execute("SELECT * FROM CARDS")
    with open(csv_name, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')  # Excel style
        writer.writerow([i[0] for i in data.description])
        writer.writerows(data)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-init', action='store_true',
                       help='Initialize the database')
    group.add_argument('-drop', action='store_true',
                       help='Drop all tables in database')
    group.add_argument('-reset', action='store_true',
                       help='Reset database to the initial state')
    args = parser.parse_args()

    if args.drop:
        _drop_db()
        print("Database properly dropped")
    elif args.init:
        _init_db()
        print("Database properly initiated")
    elif args.reset:
        _reset_db()
        print("Database properly reset")

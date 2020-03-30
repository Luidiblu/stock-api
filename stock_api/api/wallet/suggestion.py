from stock_api.database.orm import User, Wallet, Stock, StockHistory, Transaction
from stock_api.database import Base, DBObject, DBContext, engine


def stock_suggestions(suggestion):
    with DBContext(engine) as db:
        stocks_suggests = db.session.query(Stock).filter(Stock.name == suggestion).all()
    if stocks_suggests == None:
        print('Nenhuma ação encontrada')
    print(f"Ações: {stocks_suggests}")

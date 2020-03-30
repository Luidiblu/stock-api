from stock_api.database.orm import User, Wallet, Stock, StockHistory, Transaction
from stock_api.database import Base, DBObject, DBContext, engine


def create_wallet(user_id, wallet_name):
    '''
    Cria uma wallet recebendo um nome e id de usuário. 
    '''
    with DBContext(engine) as db:
        user = db.session.query(User).filter(User.id == user_id).one_or_none()
        if user == None:
            return
        wallet = Wallet(**{
            "user_id": user_id,
            "name": wallet_name
        })
        try:
            db.session.add(wallet)
            db.session.commit()
        except Exception:
            db.session.rollback()

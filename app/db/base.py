from app.db.base_class import Base
from app.models.user import User
from app.models.wallet import Wallet 
from app.models.transaction import Transaction

# Import all models so Base.metadata.create_all() can discover them

import email
from app.base.models.users import User
from app.base.orm_tools import FactoryController

def add_test_user():
    user = User(email='test@company.ma',password='12345678',first_name='Test',last_name='User',is_active=True)
    FactoryController.createOne(user)    
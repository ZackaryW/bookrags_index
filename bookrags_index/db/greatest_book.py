from sqlalchemy.orm import declarative_base
import sqlalchemy
import os
package_path = os.path.dirname(os.path.abspath(__file__))

base = declarative_base()

class GreatestBook(base):
    __tablename__ = "records"
    rank = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    author = sqlalchemy.Column(sqlalchemy.String)

greatest_book_engine = sqlalchemy.create_engine("sqlite:///{}".format(os.path.join(package_path ,"greatest_book.db")))
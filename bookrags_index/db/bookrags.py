from sqlalchemy.orm import declarative_base
import sqlalchemy
import os
package_path = os.path.dirname(os.path.abspath(__file__))
base = declarative_base()

class BookRecord(base):
    __tablename__ = "records"
    link = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    book_name = sqlalchemy.Column(sqlalchemy.String)
    fetched_from = sqlalchemy.Column(sqlalchemy.String)

bookrags_engine = sqlalchemy.create_engine("sqlite:///{}".format(os.path.join(package_path ,"bookrags.db")))

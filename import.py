import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session (sessionmaker(bind=engine))

def main():
    b = open("books.csv")
    reader = csv.reader(b)

    for isbn, title, author, year, review_count, average_score in reader:
        
        db.execute("INSERT INTO books (isbn, title, author, year, review_count, average_score) VALUES (:isbn, :title, :author, :year, :review_count, :average_score)",{"isbn": isbn, "title": title, "author": author, "year": year,"review_count": review_count,"average_score": average_score})
        print (f"added book isbn: {isbn}")
    db.commit()

    
if __name__=="__main__":
    main()
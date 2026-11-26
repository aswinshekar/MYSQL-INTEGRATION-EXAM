import mysql.connector
class Library:
    def __init__(self):
        try:
            self.con=mysql.connector.connect(user="root" ,password="Root",host="localhost",database="library_management")

            print("\nCONNECTION SUCCESSFUL")
        except:
            print("FAILED TO CONNECT")

#--------------------------------INSERT
    def add_book(self,t,auth,cat,tot,avail):
        try:
            c=self.con.cursor()
            query="insert into books(title,author,category,total_copies,available_copies) values(%s,%s,%s,%s,%s)"
            data=(t,auth,cat,tot,avail)
            c.execute(query,data)
            self.con.commit()
            print("\nRECORD INSERTED INTO TABLE ")
        except:
            print("FAILED TO INSERT")
# --------------------------------INSERT

# --------------------------------VIEW_RECORD
    def view_record(self):
        try:
            c = self.con.cursor()
            query = "select * from books where available_copies >= 1 order by title asc limit 20"
            c.execute(query)
            record = c.fetchall()
            if record:
                for i in record:
                    print(i)
            else:
                print("NO RECORD")
        except:
            print("FAILED TO VIEW TABLE")
# --------------------------------VIEW_RECORD


# -----------------------------------SEARCH
    def search(self, ch, value):
        try:
            c = self.con.cursor()
            if ch == 1:
                query = "select * from books where book_id = %s"
                data = (value,)
            elif ch == 2:
                query = "select * from books where title like %s or author like %s"
                data = ('%' + value + '%', '%' + value + '%')
            else:
                print("INVALID CHOICE")

            c.execute(query, data)
            record = c.fetchall()
            if record:
                for i in record:
                    print(i)
            else:
                print("NO RECORD FOUND")
        except:
            print("FAILED TO SEARCH")
# ---------------------------------------SEARCH

#----------------------------------------UPDATE
    def update_book(self, bid, avail):
        try:
            c = self.con.cursor()
            query = "select total_copies from books where book_id = %s"
            data=(bid,)
            c.execute(query, data)
            record = c.fetchone()
            if record:
                total = record[0]
                if avail < 0:
                    print("AVAILABLE COPIES CANNOT BE NEGATIVE")
                elif avail > total:
                    print("AVAILABLE COPIES CANNOT EXCEED TOTAL COPIES")
                else:
                    query = "update books set available_copies = %s where book_id = %s"
                    data = (avail, bid)
                    c.execute(query, data)
                    self.con.commit()
                    print("AVAILABLE COPIES UPDATED SUCCESSFULLY")
            else:
                print("BOOK ID NOT FOUND")
        except:
            print("FAILED TO UPDATE")
# ----------------------------------------UPDATE

#---------------------------------------DELETE
    def delete_book(self, bid):
        try:

            c = self.con.cursor()
            query = "select * from books where book_id = %s"
            data=(bid,)
            c.execute(query, data)
            record = c.fetchone()
            if record:
                print(record)
                confirm = input("ARE YOU SURE YOU WANT TO DELETE? (yes/no): ")
                if confirm.lower() == "yes":
                    query = "delete from books where book_id = %s"
                    c.execute(query, data)
                    self.con.commit()
                    print("BOOK DELETED SUCCESSFULLY")
                else:
                    print("DELETION CANCELLED")
            else:
                print("BOOK ID NOT FOUND")
        except:
            print("FAILED TO DELETE")
# ---------------------------------------DELETE

#------------------------------------LIBRARY SUMMARY
    def library_summary(self):
        try:
            c = self.con.cursor()
            query = "Select count(book_id),sum(available_copies),avg(total_copies)from books"
            c.execute(query)
            record = c.fetchone()
            if record:
                print("\n----- LIBRARY SUMMARY -----")
                print("TOTAL NUMBER OF BOOKS:", record[0])
                print("TOTAL AVAILABLE COPIES:", record[1] )
                print("AVERAGE TOTAL COPIES:", record[2])
            else:
                print("NO RECORD")
        except:
            print("FAILED TO GET LIBRARY SUMMARY")
# ------------------------------------LIBRARY SUMMARY


l=Library()
# try:
while(1):
    try:
        print("\n1. ADD BOOK\n2. VIEW AVAILABLE BOOKS\n3. SEARCH BOOK\n4. UPDATE AVAILABLE COPIES\n5. DELETE BOOK\n6. LIBRARY SUMMARY\n7. EXIT\n")
        op=int(input("ENTER YOUR CHOICE: "))
        if op == 1:#ADD RECORDS INTO THE TABLE
            title = input("ENTER BOOK TITLE: ")
            author = input("ENTER AUTHOR: ")
            category = input("ENTER CATEGORY: ")
            total = int(input("ENTER TOTAL COPIES: "))
            available = int(input("ENTER AVAILABLE COPIES: "))
            if total < 0 or available < 0:
                print("COPIES CANNOT BE NEGATIVE")
            elif available > total:
                print("AVAILABLE COPIES CANNOT EXCEED TOTAL COPIES")
            else:
                l.add_book(title,author,category,total,available)
        elif op == 2:#READ ALL RECORDS
           l.view_record()
        elif op == 3:#SEARCH
            print("\n1. SEARCH BY BOOK ID")
            print("2. SEARCH BY TITLE OR AUTHOR")
            ch = int(input("\nENTER YOUR CHOICE: "))
            if ch == 1:
                bid = int(input("ENTER BOOK ID: "))
                l.search(ch, bid)
            elif ch == 2:
                name = input("ENTER TITLE OR AUTHOR: ")
                l.search(ch, name)
            else:
                print("INVALID CHOICE")
        elif op == 4:#UPDATE
            bid = int(input("ENTER BOOK ID: "))
            available = int(input("ENTER NEW AVAILABLE COPIES: "))
            l.update_book(bid, available)
        elif op == 5:#DELETE
            bid = int(input("ENTER BOOK ID TO DELETE: "))
            l.delete_book(bid)
        elif op == 6:#SUMMARY
            l.library_summary()
        elif op == 7:
            exit()
        else:
            print("INVALID CHOICE")
    except:
           print("\nPLEASE ENTER A NUMERIC VALUE")


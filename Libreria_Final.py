import json
import csv
import os

CWD = os.path.dirname(__file__)


with open(f"{CWD}/bookshop.json", encoding="utf8") as file:
    bookshop = json.load(file)["books"]

def json_save():
    with open("./bookshop.json", "w", encoding = "utf8") as file: 
        json.dump({"books": bookshop}, file, ensure_ascii=False, indent=4) 

def write_data_in_json(what, where): 
    with open(where, "w", encoding="utf8") as file:
        json.dump(what, file, ensure_ascii=False, indent=4)



print(bookshop)

def menu():
    print("Bookshop".center(50, "-"))
    print("1. ID")
    print("2. Author")
    print("3. Title")
    print("4. Genre")
    print("5. New book")
    print("6. Modify book")
    print("7. Delete book")   
    print("8. Export csv") 
    print("Q. Exit")

def book_by_id(id_book, libreria):
    for book in libreria:
        if book["id"] == id_book:
            return book 

def books_by_key(search_term, libreria, key):
    result = []
    for book in libreria:
        if book[key].lower().find(search_term.lower()) >= 0:      
            result.append(book)
    return result

def create_book(genre, bookshop):
    new_book = {}
    keys = list(bookshop[0].keys()) # which is ['id', 'title', 'author', 'genre']
    for key in keys[1:3]: # title, author
        new_book[key] = input(f"{key}: ") #here it adds new title and author
    new_book[keys[3]] = genre #here it says that genre is a function paramater that will be added later in create_book(user_genre,bookshop)

    genre = genre.lower() #it puts genre lowercase
    word_cut = genre.split(" ") #word_cut is splitting 2 words in a list of 2 values like ['Narrativa', 'extranjera']
    if len(word_cut) == 1: #if word_cut has only one value:
        book_id = f"{word_cut[0][0]}{word_cut[0][-1]}_{len(bookshop)}" # Here it adds the first letter from the first value, and 
    else:                                                              #if its more than 1 value:
        book_id = f"{word_cut[0][0]}{word_cut[1][0]}_{len(bookshop)}" #it creates first letter from the first value and first letter from the second plus "_" plus length of bookshop
    new_book[keys[0]] = book_id # New ID from the book will be the above
    bookshop.append(new_book) # it adds new book to bookshop

def print_genres():
    for i, genre in enumerate(genres): 
            print(f"{i + 1 }. {genre}")

def print_pretty(book_to_print):
    for k, v in book_to_print.items():
            print(f"{k}: {v}")

user = "0"
while user != "q":
    genres = ["Narrativa extranjera", "Divulgación científica", "Narrativa policíaca", "Ciencia ficción", "Autoayuda"]
    menu()
    user = input("Choose: ")

    if user == "1": # OPCIÓN ID:
        user_id = input("id: ")
        book = book_by_id(user_id, bookshop)
        if book != None:
            print_pretty(book)
        else:
            print("Libro no encontrado")
                
    elif user == "2": # GET BY AUTHOR
        key = "author"
        user_author = input("author: ").lower()
        books_by_author = books_by_key(user_author, bookshop, key)
        for book in books_by_author:
            print_pretty(book)
            print("------------")

    elif user == "3": # GET BY TITLE
        user_title = input("Title: ").lower()
        books_by_title = books_by_key(user_title, bookshop, "title")
        for book in books_by_title:
            print_pretty(book)
            print("------------")
        
    elif user == "4": # GET BY GENRE
        key = "genre"
        for i, genre in enumerate(genres): 
            print(f"{i + 1 }. {genre}")
        # print_genres()
        user_index = int(input("Choose: "))
        user_genre = genres[user_index - 1]
        result = books_by_key(user_genre, bookshop, key)        
        print(f"{user_genre}".center(50,"-"))

        for book in result:
            print_pretty(book)
            input("Continue...")
            print("".center(50,"-"))
        print(f"Se han encontrado {len(result)} libros.")

    elif user == "5":  # CREATE BOOK
        print_genres() #prints genres list 
        user = int(input("Choose: ")) - 1 #user chooses genre
        user_genre = genres[user] #user_genre is the genre that user chose
        create_book(user_genre,bookshop) #it calls the funcion to create book
        json_save()

    elif user == "6": # UPDATE BOOK
        book_id = input("ID: ") # dc_1
        book_to_update = book_by_id(book_id, bookshop)
        if book_to_update == None:
            print(f"El id: {book_id}, no se encuentra en nuestra base de datos.")
        else:
            keys = list(book_to_update)
            for i, key in enumerate(keys):
                print(f"{i + 1}. {key}")
            user = int(input("Choose: ")) - 1
            key = keys[user]
            bookshop.remove(book_to_update)
            book_to_update[key] = input("Nuevo valor: ")
            bookshop.append(book_to_update)

            json_save()

    elif user == "7": 
        user = input("id: ")
        book_to_delete = book_by_id(user, bookshop)
        user = input("Está seguro que desea eliminar el libro (y/n): ").lower()
        if user == "y":
            bookshop.remove(book_to_delete)
        json_save()

    elif user == "8":
        with open("export_bookshop.csv", "w" ,encoding="utf8") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(bookshop[0].keys())

            for book in bookshop:
                book_id = book["id"]
                book_title = book["title"]
                book_author = book["author"]
                book_genre = book["genre"]
                csv_writer.writerow([book_id, book_title, book_author, book_genre])
                

    elif user.lower() == "q":
        user = user.lower()
        print("Bye!")
    else:
        user = "1"
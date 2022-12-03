add_student (POST request)

http://127.0.0.1:8000/library_management/add_student/

Sample Request Body :

{\
"roll_number" : 1,\
"first_name" : "Shafiya",\
"last_name" : "Naaz",\
"email" : "abc@gmail.com",\
"department" : "CSE"\
}

add_book (POST request)

http://127.0.0.1:8000/library_management/add_book/

Sample Request Body :

{\
"title" : "The Alchemist",\
"author" : "Paulo Coelho",\
"description" : "The masterpiece tells the magical story of Santiago, an Andalusian shepherd boy who yearns to travel in search of a worldly treasure as extravagant as any ever found.",\
"quantity_available" : 5\
}

check_out (POST request)

http://127.0.0.1:8000/library_management/check_out/

Sample Request Body :

{\
"book_id" : 2,\
"student_id" : 1,\
"quantity" : 1\
}
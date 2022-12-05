Find the link to POSTMAN collection for the APIs here :
https://www.getpostman.com/collections/bf840ab7df2b35487cff

<b><u>view_all_books (GET request)</u></b> : \
Returns all the books present in the DB.

<b><u>view_all_students (GET request)</u></b> : \
Returns all the students present in the DB.

<b><u>add_student (POST request)</u></b>

Adds a student to the DB.

http://127.0.0.1:8000/library_management/add_student/

Sample Request Body :

{\
"roll_number" : 2,\
"name" : "def",\
"email" : "def@gmail.com",\
"department" : "CSE"\
}

<b><u>add_book (POST request)</u></b>

Adds a book to the DB.

http://127.0.0.1:8000/library_management/add_book/

Sample Request Body :

{\
"title" : "Think and Grow Rich",\
"author" : "Napolean Hill",\
"description" : "Some people see it as one of the best books of all time to pull you out of depression. It will help you
see the positive side of things in life. It will help you realize the person you are deep inside of letting you focus on
the negative side of life.",\
"quantity_available" : 10\
}

<b><u>check_out (POST request)</b></u>

Borrows a book from the library.

http://127.0.0.1:8000/library_management/check_out/

Sample Request Body :

{\
"book_id" : 4,\
"student_id" : 1\
}

<b><u>check_in (PUT request)</b></u>

Returns a book to the library.

http://127.0.0.1:8000/library_management/check_in/

Sample Request Body :

{\
"book_id" : 4,\
"student_id" : 1\
}

<b><u> filter_books (GET request) </b></u>

Filters checked_out books based on book_name, student_name and checkout_date

http://127.0.0.1:8000/library_management/filter_books/?book_name=Think and Grow Rich 1&student_name=Shafiya
Naaz&checkout_date=2022-12-04

<b><u>book_by_id (GET request)</b></u>

Get book by book_id :

http://127.0.0.1:8000/library_management/book_by_id/<book_id>

<b><u>student_by_id (GET request)</b></u>

Get student by student_id :

http://127.0.0.1:8000/library_management/student_by_id/<student_id>

<b><u> delete_book (DELETE request) </b></u>

Deletes book by book id :

http://127.0.0.1:8000/library_management/delete_book/<book_id>

<b><u> delete_student (DELETE request) </b></u>

Deletes student by student id :

http://127.0.0.1:8000/library_management/delete_student/<student_id>

<b><u> update_book_details (PUT request) </u></b>

Updates book details by given book id :

http://127.0.0.1:8000/library_management/update_book_details/<book_id>

Sample request body :

{\
"title": "Think and Grow Rich",\
"author": "abc",\
"description": "Some people see it as one of the best books of all time to pull you out of depression. It will help you
see the positive side of things in life. It will help you realize the person you are deep inside of letting you focus on
the negative side of life.",\
"quantity_available": 10\
}

<b><u> update_student_details (PUT request) </u></b>

Updates student details by given student id :

http://127.0.0.1:8000/library_management/update_student_details/<student_id>

Sample request body :

{\
"roll_number": "1",\
"name": "xyz",\
"email": "xyz@gmail.com",\
"department": "CSE"\
}

<b><u> update_check_in (PUT request) </u></b>

Takes book_id of the book to be returned and book_id of the new book to be issued and the student_id in request
body and checks in the book returned and checks out the book issued :

http://127.0.0.1:8000/library_management/update_check_in/

Sample request body :

{\
"return_book_id" : 4,\
"new_book_id" : 3,\
"student_id" : 1\
}
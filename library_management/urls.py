from django.urls import path
from .views import views_book, views_student, views_book_issue

urlpatterns = [
    path('book_by_id/<int:id>', views_book.get_book_details_by_id),
    path('student_by_id/<int:id>', views_student.get_student_details_by_id),
    path('add_book/', views_book.add_book),
    path('add_student/', views_student.add_student),
    path('view_all_books/', views_book.view_all_books),
    path('view_all_students/', views_student.view_all_students),
    path('delete_book/<int:id>', views_book.delete_book),
    path('delete_student/<int:id>', views_student.delete_student),
    path('update_book_details/<int:id>', views_book.update_book_details),
    path('update_student_details/<int:id>', views_student.update_student_details),
    path('check_out/', views_book_issue.check_out),
    path('check_in/', views_book_issue.check_in),
    path('filter_books/', views_book_issue.get_all_books_with_filters),
    path('update_check_in/', views_book_issue.update_checkin),
]

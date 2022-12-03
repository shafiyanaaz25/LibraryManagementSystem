from django.urls import path
from . import views

urlpatterns = [
    path('books/<int:id>', views.get_book_details_by_id),
    path('add_book/', views.add_book),
    path('add_student/', views.add_student),
    path('view_all_books/', views.view_all_books),
    path('view_all_students/', views.view_all_students),
    path('check_out/', views.check_out),
    path('check_in/', views.check_in),
    path('filter_books/', views.get_all_books_with_filters),
    path('delete_book/', views.delete_book),
    path('delete_student/', views.delete_student),
    path('update_book_details/', views.update_book_details),
    path('update_student_details/', views.update_student_details),

    # (r'^user/(?P<username>\w{0,50})/$', views.profile_page,),
]

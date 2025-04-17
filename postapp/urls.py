from django.urls import path
from postapp import views

app_name='Myapp'
urlpatterns=[

    path("ticket/",views.ticket,name="ticket_page"),
    # path("review/",views.review,name="review_page"),
    path("posts/",views.Myposts,name="post_page"),
    path("update/<int:id>/",views.Update,name="update_page"),
    path("delete/<int:id>/",views.Delete,name="delete_page"),
    path("editrev/<int:id>/",views.Editcomment,name="editcomment_page"),
    path("deleterev/<int:id>/",views.Deletecomment,name="deletecomment_page"),
    path("dashboard/",views.Dashboard,name="mydash_page"),
    path("followpage/",views.Follow,name="follow_page"),
    path("unfollowpage/<int:id>/",views.Unfollow,name="unfollow_page"),
    path("revtickpage/<int:id>/",views.Review_ticket,name="revtick_page"),
    path("profilepage/",views.profile,name="profile_page"),
    path("commentpage/<int:id>/",views.view_comment,name="comment_page"),
    path('react/<int:ticket_id>/',views.React_to_ticket,name="react_page"),
    path('chat/<int:recipient_id>/', views.chat_view, name='chat'),

]
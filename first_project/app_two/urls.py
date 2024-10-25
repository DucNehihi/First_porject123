
from django.urls import path
from . import views 

from app_two.views import (
    IndexView, 
    HomeView, 
    BlogMainView, 
    BlogDetailView,
    draft_post_view,  # Nếu bạn có view riêng cho draft
    save_draft, 
    draft_post,
    list_posts,
    delete_draft,  # Đảm bảo có view này
    approve_post,
    delete_post,
    edit_post,
    add_draft_comment,
    edit_draft,
    like_post,
    dislike_post,
    user_management,
    
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('demo/', IndexView.as_view(), name='index'),
    path('home/', HomeView.as_view(), name='home'),
    path('blogs/', BlogMainView.as_view(), name='blog_main'),
    path('blog/', BlogDetailView.as_view(), name='blog_detail'),
  
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('write/', views.write_post, name='write_post'),
    path('draft/', views.draft_post, name='draft'),  # Nếu view này hiển thị danh sách bài viết nháp
    path('list/', views.list_posts, name='blog_list'),
    
    path('write_post/', save_draft, name='save_draft'),
    
    path('draft/<int:post_id>/', draft_post_view, name='draft_post'),  # Nếu view này hiển thị bài viết nháp cụ thể
    path('listpost/', views.list_post, name='list_post'),  # Đảm bảo tên này không trùng lặp
    path('approve_post/', views.approve_post, name='approve_post'),

    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),  # Xóa bài viết
    path('post/edit/<int:post_id>/', views.edit_post, name='edit_post'),

    path('draft/<int:post_id>/', views.draft_post, name='draft_post'),  # Đường dẫn này có thể gây nhầm lẫn
    path('delete/', delete_draft, name='delete_draft'),  # Xóa nháp

    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),

      path('delete/', views.delete_draft, name='delete_draft'),  
    path('draft/', views.draft_post, name='draft_post'), 
     path('add_draft_comment/<int:post_id>/', add_draft_comment, name='add_draft_comment'),

     
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike/<int:post_id>/', views.dislike_post, name='dislike_post'),
    path('comment/<int:post_id>/', views.comment_post, name='comment_post'),

     path('like-comment/<int:comment_id>/', views.like_comment, name='like_comment'),

      path('detail_post/<int:post_id>/', views.detail_post, name='detail_post'),


       path('comments/<int:post_id>/', views.comment_post, name='comment_post'),

         path('edit/<int:post_id>/', edit_post, name='edit_post'),

            path('edit_post/<int:post_id>/', edit_post, name='edit_post'),

               path('edit_draft/<int:post_id>/', edit_draft, name='edit_draft'),
                path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('post/<int:post_id>/dislike/', dislike_post, name='dislike_post'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),




    path('admin/user-management/', user_management, name='user_management'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

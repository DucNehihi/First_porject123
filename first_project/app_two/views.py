from django.views.generic import TemplateView, ListView, DetailView
from .models import BlogPost, AccessRecord
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from .forms import RegisterForm
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect 
from django.urls import reverse
from .models import PostAction
from django.contrib.auth.models import User
# -*- coding: utf-8 -*-

# @login_required
def post_list(request):
    posts = Post.objects.all()

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('blog_list')  # Điều hướng lại trang sau khi gửi bình luận

    else:
        form = CommentForm()

    return render(request, 'list_post.html', {'posts': posts, 'form': form})







# Trang index hiển thị danh sách các access record
class IndexView(ListView):
    model = AccessRecord
    template_name = 'index2.html'
    context_object_name = 'access_records'
    ordering = ['date']

# Trang chủ
class HomeView(TemplateView):
    template_name = 'index1.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lấy 3 bài viết có lượt like cao nhất
        context['top_posts'] = Post.objects.filter(is_draft=False).order_by('-likes')[:3]
        return context

# Hiển thị bài blog chính và các bài blog nhỏ
class BlogMainView(TemplateView):
    template_name = 'blog_main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_blog = BlogPost.objects.latest('created_at')
        small_blogs = BlogPost.objects.exclude(id=main_blog.id)[:4]
        context['main_blog'] = main_blog
        context['small_blogs'] = small_blogs
        return context

# Hiển thị danh sách các blog
class BlogListView(ListView):
    model = BlogPost
    template_name = 'all_blogs.html'
    context_object_name = 'blogs'

# Hiển thị chi tiết từng bài blog
class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        recommended_blogs = BlogPost.objects.exclude(id=blog.id)[:3]
        context['recommended_blogs'] = recommended_blogs
        return context






# View đăng ký
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Tự động đăng nhập sau khi đăng ký thành công
            return redirect('login')  # Điều hướng về trang chủ hoặc trang khác
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# View đăng nhập
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Điều hướng về trang chủ hoặc trang khác
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
from django.contrib.auth.decorators import login_required

#@login_required
def home_view(request):
    return render(request, 'home.html')


# views.py (nếu bạn đã định nghĩa view cho login)
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Đảm bảo template này tồn tại



def list_posts(request):
    # Danh sách bài viết (cần điều chỉnh theo yêu cầu của bạn)
    posts = []  # Thay thế bằng logic thực tế

    return render(request, 'list_post.html', {'posts': posts})




# views.py
from django.shortcuts import render, get_object_or_404
from .models import Post  # Đảm bảo bạn đã nhập đúng model


def draft_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'draft.html', {'post': post})
from django.core.paginator import Paginator
#@login_required

def list_post(request):
    continent = request.GET.get("continent", None)
    query = request.GET.get("q", None)

    # Chỉ lấy bài viết đã được phê duyệt và sắp xếp theo thời gian mới nhất
    posts = Post.objects.filter(is_draft=False).order_by('-created_at')

    if query:
        posts = posts.filter(title__icontains=query)

    if continent:
        posts = posts.filter(continent=continent)

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get("post_id")
            post = get_object_or_404(Post, id=post_id)

            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

            return redirect("list_post")
    else:
        form = CommentForm()

    return render(request, "list_post.html", {"posts": page_obj, "form": form})





def save_draft(request):
    if request.method == 'POST':
        title = request.POST.get('title')  # Lấy tiêu đề từ form
        content = request.POST.get('content')
        continent = request.POST.get("continent")
        image = request.FILES.get('image')

        post = Post(title=title, content=content, image=image, continent=continent)
        post.save()

        # Chuyển hướng ngay sau khi lưu để tránh submit lại form
        return redirect('draft_post', post_id=post.id)

    return render(request, 'write_post.html')



@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.user and not request.user.is_staff:
        return HttpResponse("Bạn không có quyền xóa bài viết này.")

    post.delete()
    return redirect('list_post')






# View phê duyệt bài viết
@login_required
def approve_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        
        # Đánh dấu bài viết đã được phê duyệt (is_draft=False)
        post.is_draft = False
        post.save()
        
        # Thay vì chuyển hướng mà không có post_id, bạn cần truyền post_id vào URL
        return redirect('draft_post', post_id=post.id)  # Chuyển hướng lại trang nháp sau khi phê duyệt
    return HttpResponse("Yêu cầu không hợp lệ.")

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        
        # Đánh dấu bài viết đã được phê duyệt (is_draft=False)
        post.is_draft = False
        post.save()
        
        return redirect('draft_post')  # Chuyển hướng lại trang nháp sau khi phê duyệt
    return HttpResponse("Yêu cầu không hợp lệ.")

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        post.is_draft = False  # Đánh dấu bài viết đã được phê duyệt
        post.save()
        return redirect('list_post')
    return HttpResponse("Yêu cầu không hợp lệ.")

# View xóa bài viết nháp


# View chỉnh sửa bài viết
from django.contrib import messages
@login_required

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Lấy giá trị của 'redirect_to' từ chuỗi query (nếu có), mặc định là 'list_post'
    redirect_to = request.GET.get('redirect_to', 'list_post')

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        
        if 'image' in request.FILES:
            post.image = request.FILES['image']
        
        # Kiểm tra xem title có giá trị không
        if post.title:
            post.save()

            # Chuyển hướng về trang mong muốn sau khi lưu
            if redirect_to == 'draft_post':
                return redirect('draft_post', post_id=post.id)
            else:
                return redirect('list_post')
        else:
            # Thêm thông báo lỗi nếu title không hợp lệ
            messages.error(request, "Title không được để trống.")

    return render(request, 'edit_post.html', {'post': post})



# View thêm bài viết mới
@login_required
def write_post(request):
    if request.method == "POST":
        title = request.POST.get("title")  # Lấy tiêu đề
        content = request.POST.get("content")
        image = request.FILES.get("image")
        continent = request.POST.get("continent")
        # Lưu hình ảnh nếu có
        if image:
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            image_url = fs.url(filename)
        else:
            image_url = None

        # Lưu bài viết dưới dạng nháp
        post = Post(
            title=title,
            content=content,
            image=image_url,
            continent=continent,
            is_draft=True,
        )
        post.save()

        # Chuyển hướng đến trang draft để xem nháp
        return redirect("write_post", post_id=post.id)

    return render(request, "write_post.html")

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image', None)

        post = Post(title=title, content=content, image=image, is_draft=True)
        post.save()
        return redirect('draft_post')

    return render(request, 'write_post.html')



    
@login_required
def delete_draft(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')  # Lấy post_id từ form
        post = get_object_or_404(Post, id=post_id)  # Lấy bài viết tương ứng
        
        # Kiểm tra nếu bài viết là nháp (is_draft=True)
        if post.is_draft:
            post.delete()  # Xóa bài viết
            return redirect('draft_post')  # Chuyển hướng lại trang nháp sau khi xóa
        else:
            return HttpResponse("Bạn không thể xóa bài viết đã được phê duyệt.")

    if request.method == 'POST':
        post_id = request.POST.get('post_id')  # Lấy post_id từ form
        post = get_object_or_404(Post, id=post_id)  # Lấy bài viết tương ứng
        post.delete()  # Xóa bài viết
        return redirect('draft')  # Hoặc bạn có thể điều hướng


@login_required
def add_draft_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user  # Gắn người dùng hiện tại vào bình luận
            comment.save()
            return redirect('draft_post')  # Chuyển hướng về trang nháp sau khi thêm bình luận
    
    return redirect('draft_post')  # Nếu không có POST reques

@login_required
def draft_post(request):
    posts = Post.objects.filter(is_draft=True)  # Chỉ lấy bài viết nháp
    return render(request, 'draft.html', {'posts': posts})





# Tăng like
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Kiểm tra xem người dùng đã like hoặc dislike bài viết chưa
    post_action, created = PostAction.objects.get_or_create(user=request.user, post=post)

    if post_action.action != 'like':
        if post_action.action == 'dislike':
            post.dislikes -= 1  # Nếu trước đó đã dislike, giảm dislike
        post.likes += 1
        post_action.action = 'like'
        post_action.save()
        post.save()
    return redirect('list_post')


from .models import PostAction
# Tăng dislike
@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Kiểm tra xem người dùng đã like hoặc dislike bài viết chưa
    post_action, created = PostAction.objects.get_or_create(user=request.user, post=post)

    if post_action.action != 'dislike':
        if post_action.action == 'like':
            post.likes -= 1  # Nếu trước đó đã like, giảm like
        post.dislikes += 1
        post_action.action = 'dislike'
        post_action.save()
        post.save()
    return redirect('list_post')






# Trang bình luận riêng
@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('comment_post', post_id=post_id)
    else:
        form = CommentForm()

    return render(request, 'comment_page.html', {'post': post, 'form': form})



@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Kiểm tra xem người dùng đã "like" bình luận chưa
    if request.user not in comment.liked_users.all():
        comment.likes += 1
        comment.liked_users.add(request.user)  # Thêm người dùng vào liked_users
        comment.save()

    return HttpResponseRedirect(reverse('comment_post', args=[comment.post.id]))


from .models import Post  # Giả sử bạn có một model tên là Post

def detail_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'detail_post.html', {'post': post})






def edit_draft(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        title = request.POST.get('title')  # Lấy tiêu đề từ POST
        content = request.POST.get('content')  # Lấy nội dung từ POST

        # Kiểm tra xem tiêu đề và nội dung có giá trị không
        if not title or not content:
            return render(request, 'edit_draft.html', {'post': post, 'error': 'Tiêu đề và nội dung không được để trống.'})

        post.title = title
        post.content = content

        # Nếu có hình ảnh mới
        if request.FILES.get('image'):
            post.image = request.FILES['image']

        post.save()  # Lưu bài viết đã được cập nhật
        return redirect('draft_post')  # Chuyển hướng về trang draft

    return render(request, 'edit_draft.html', {'post': post})

def delete_comment(request, comment_id):
    # Lấy bình luận cần xóa
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Lưu post_id của bình luận
    post_id = comment.post.id

    # Xóa bình luận nếu người dùng là tác giả hoặc admin
    if request.user == comment.user or request.user.is_staff:
        comment.delete()

    # Redirect về trang bình luận của bài viết
    return redirect('comment_post', post_id=post_id)

    from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required  # Chỉ cho phép admin truy cập
def user_management(request):
    users = User.objects.all()  # Lấy tất cả người dùng

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        User.objects.filter(id=user_id).delete()  # Xóa người dùng
        return redirect('user_management')  # Điều hướng lại trang quản lý

    return render(request, 'user_management.html', {'users': users})

import os
from django.core.management.base import BaseCommand
from app_two.models import Post, User  # Thay 'app_two' bằng tên ứng dụng của bạn
from django.core.files import File
from django.conf import settings  # Để lấy đường dẫn tới static
from faker import Faker
import random
import shutil  # Thư viện để copy file

fake = Faker()

class Command(BaseCommand):
    help = 'Tạo dữ liệu giả cho model Post'

    def handle(self, *args, **kwargs):
        users = User.objects.all()  # Lấy danh sách người dùng hiện có

        if not users.exists():
            self.stdout.write(self.style.ERROR('Không có người dùng nào. Vui lòng tạo ít nhất một người dùng.'))
            return

        # Đường dẫn tới thư mục static/images
        static_image_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
        image_choices = [f'b-{i}.jpg' for i in range(1, 13)]  # Tên các ảnh b-1.jpg đến b-12.jpg

        for _ in range(20):  # Tạo 20 bài viết
            title = fake.sentence(nb_words=random.randint(6, 10))  # Tạo tiêu đề ngẫu nhiên từ 6 đến 10 từ
            content = fake.paragraph(nb_sentences=random.randint(40, 60))  # Nội dung ngẫu nhiên gồm 10 câu
            continent = random.choice([choice[0] for choice in Post.CONTINENT_CHOICES])  # Lựa chọn ngẫu nhiên châu lục

            # Chọn ảnh ngẫu nhiên từ thư mục static/images
            image_name = random.choice(image_choices)
            static_image_path = os.path.join(static_image_dir, image_name)  # Đường dẫn tới tệp ảnh trong static

            # Copy ảnh từ static sang media
            media_image_path = os.path.join(settings.MEDIA_ROOT, 'images', image_name)
            shutil.copy(static_image_path, media_image_path)  # Copy file từ static sang media

            with open(media_image_path, 'rb') as img_file:
                image_file = File(img_file)

                created_at = fake.date_time_this_year()  # Ngày tạo trong năm hiện tại
                is_draft = random.choice([True, False])  # Ngẫu nhiên đánh dấu bài viết là nháp hay không
                user = random.choice(users)  # Chọn ngẫu nhiên một người dùng từ danh sách người dùng hiện có
                likes = random.randint(10, 40)  # Số lượt thích ngẫu nhiên từ 0 đến 20
                dislikes = random.randint(0, 10)  # Số lượt không thích ngẫu nhiên từ 0 đến 10

                post = Post(
                    title=title,
                    content=content,
                    continent=continent,
                    created_at=created_at,
                    is_draft=is_draft,
                    user=user,
                    likes=likes,
                    dislikes=dislikes
                )
                post.image.save(image_name, image_file)  # Lưu tệp ảnh vào trường image
                post.save()

        self.stdout.write(self.style.SUCCESS('Tạo dữ liệu giả cho Post thành công!'))

from django.contrib import admin
from app_two.models import AccessRecord, Topic, Webpage,Post,Comment,PostAction
# Register your models here.
admin.site.register(Topic)
admin.site.register(Webpage)
admin.site.register(AccessRecord)
admin.site.register(Post)
admin.site.register(Comment)
#chucnang
admin.site.register(PostAction)
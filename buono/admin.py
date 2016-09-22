from django.contrib import admin
from .models import AppealPoint
from .models import Vote
from .models import Comment

admin.site.register(AppealPoint)
admin.site.register(Vote)
admin.site.register(Comment)

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Task)
admin.site.register(TaskIconSetter)
admin.site.register(ClaendarTask)
admin.site.register(Player)
admin.site.register(MatchResult)
admin.site.register(Calendar)
admin.site.register(APIKey)
admin.site.register(DailySession)
admin.site.register(Session)
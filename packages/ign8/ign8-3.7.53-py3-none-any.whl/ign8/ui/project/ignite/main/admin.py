from django.contrib import admin

# Register your models here.
from .models import projects
from .models import services
from .models import maindata
from .models import users
from .models import groups


admin.site.register(projects)
admin.site.register(services)
admin.site.register(maindata)
admin.site.register(users)
admin.site.register(groups)


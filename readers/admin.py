from django.contrib import admin
from .models import *


admin.site.register(Reader)
admin.site.register(StudentReader)
admin.site.register(TeacherReader)
admin.site.register(WorkerReader)
admin.site.register(RetireeReader)

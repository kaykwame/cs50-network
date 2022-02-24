from django.contrib import admin
from .models import User, Posts, Likes, Followers

#class ShowDateAdmin(admin.ModelAdmin):
#    readonly_fields = ('listing_date_time_created',)

# Register your models here.
admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Likes)
admin.site.register(Followers)

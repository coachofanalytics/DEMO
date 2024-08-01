from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomerUser, Tracker ,LoginHistory,Credential,CredentialCategory,Department,Team_Members # , Profile


# admin.site.register(CustomerUser)UserAdmin
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone', 'country', 'category', 'is_admin','is_active')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)



class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'logout_time')
    list_filter = ('user', 'login_time', 'logout_time')
    search_fields = ('user__username',)

# Now register the new UserAdmin...
admin.site.register(CustomerUser, CustomerAdmin)
admin.site.register(LoginHistory, LoginHistoryAdmin)

# Register your models here.
# admin.site.register(LoginHistory)
admin.site.register(Tracker)
admin.site.register(Credential)
admin.site.register(CredentialCategory)
admin.site.register(Team_Members)

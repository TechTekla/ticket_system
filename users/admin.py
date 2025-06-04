# from django.contrib import admin
# from .models import User

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('first_name ', 'email', 'phone_number', 'gender', 'created')
#     list_filter = ('gender', 'created')
#     search_fields = ('first_name ', 'email', 'phone_number')
#     readonly_fields = ('created', 'updated')
#     fieldsets = (
#         (None, {
#             'fields': ('first_name ', 'email')
#         }),
#         ('Contact Info', {
#             'fields': ('phone_number', 'gender'),
#             'classes': ('collapse',)
#         }),
#         ('Metadata', {
#             'fields': ('created', 'updated'),
#             'classes': ('collapse',)
#         })
#     )
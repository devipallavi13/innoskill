from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Problem, Solution

# Register Problem model
admin.site.register(Problem)

# Register Solution model
@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('problem', 'organizer', 'timestamp')  # Show problem title, organizer username, and timestamp
    search_fields = ('problem__title', 'organizer__username')  # Make problem title and organizer username searchable
    list_filter = ('timestamp', 'organizer')  # Filter by timestamp and organizer

# CustomUser Admin Panel
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):  
    model = CustomUser

    # Display fields in admin panel
    list_display = ('username', 'email', 'name', 'user_type', 'status')  # Ensure 'name' exists in CustomUser
    list_filter = ('status', 'user_type')
    search_fields = ('username', 'email', 'name')

    # Define fieldsets (inherits default UserAdmin fieldsets and adds custom fields)
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('name', 'profile_picture', 'user_type', 'organization_verification', 'status')
        }),
    )

    # Define admin actions
    actions = ['approve_organizer', 'reject_organizer']

    def approve_organizer(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "Selected organizer accounts have been approved.")

    def reject_organizer(self, request, queryset):
        queryset.update(status='on_hold')
        self.message_user(request, "Selected organizer accounts have been placed on hold.")
    
    approve_organizer.short_description = "Approve selected organizers"
    reject_organizer.short_description = "Reject selected organizers"


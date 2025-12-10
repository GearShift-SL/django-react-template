# django
from django.contrib import admin

# Local App
from .models import Tenant, TenantLogo, TenantUser, Invitation


class TenantUserInline(admin.TabularInline):
    model = TenantUser
    autocomplete_fields = ["user"]  # This enables select with search
    extra = 0
    can_delete = True
    show_change_link = True


# Register the Tenant model
@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]
    ordering = ["-created_at"]
    list_filter = ["created_at"]
    readonly_fields = ["created_at"]
    fieldsets = (
        (None, {"fields": ["name", "slug", "website", "phone", "email"]}),
        ("Metadata", {"fields": ["created_at"]}),
    )
    add_fieldsets = ((None, {"fields": ["name"]}),)

    inlines = [TenantUserInline]


@admin.register(TenantLogo)
class TenantLogoAdmin(admin.ModelAdmin):
    list_display = ["tenant", "created_at"]
    search_fields = ["tenant__name"]
    ordering = ["-created_at"]
    list_filter = ["tenant"]
    readonly_fields = ["created_at"]
    autocomplete_fields = ["tenant"]
    fieldsets = (
        (None, {"fields": ["tenant", "image"]}),
        ("Metadata", {"fields": ["created_at"]}),
    )
    add_fieldsets = ((None, {"fields": ["tenant", "image"]}),)


@admin.register(TenantUser)
class TenantUserAdmin(admin.ModelAdmin):
    list_display = ["user", "tenant"]
    search_fields = ["user__username", "tenant__name"]
    ordering = ["-tenant__created_at"]
    list_filter = ["tenant"]
    autocomplete_fields = ["user"]
    fieldsets = ((None, {"fields": ["user", "tenant", "role"]}),)
    add_fieldsets = ((None, {"fields": ["user", "tenant"]}),)


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ["email", "invited_by", "last_sent_at", "accepted_at", "created_at"]
    search_fields = ["email", "invited_by__user__email"]
    ordering = ["-created_at"]
    list_filter = ["accepted_at", "created_at"]
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["invited_by"]
    fieldsets = (
        (None, {"fields": ["email", "invited_by"]}),
        ("Status", {"fields": ["last_sent_at", "accepted_at"]}),
        ("Metadata", {"fields": ["created_at", "updated_at"]}),
    )

from django.contrib import admin
from .models import *
from .import views
from django.urls import path
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter

# Register your models here.
admin.site.register(Document)
admin.site.register(User)




class VerifikovanoFIlter(SimpleListFilter):
    title = "Status verifikacije"  # a label for our filter
    parameter_name = "verifikovano"  # you can put anything here
    no_filter_value = 'sve'

    def lookups(self, request, model_admin):
        # This is where you create filter options; we have two:
        return [
            ("verifikovano", "verifikovano"),
            ("nije verifikovano", "nije verifikovano"),
        ]

    def queryset(self, request, queryset):
        # This is where you process parameters selected by use via filter options:
        if self.value() == "verifikovano":
            # Get websites that have at least one page.
            return queryset.distinct().filter(verifikovan=True)
        if self.value():
            # Get websites that don't have any pages.
            return queryset.distinct().filter(verifikovan=False)

@admin.action(description='Verifikuj vozacku')
def verifikuj(modeladmin, request, queryset):
    queryset.update(verifikovan=True)
    for ver in queryset:
        user = ver.user
        user.doc_verified = True
        user.idd = ver.document
        user.save(update_fields=["doc_verified", "idd"])



@admin.action(description='Ukloni verifikaciju')
def odverifikuj(modeladmin, request, queryset):
    queryset.update(verifikovan=False)
    for ver in queryset:
        user = ver.user
        user.doc_verified = False
        user.idd = None
        user.save(update_fields=["doc_verified", "idd"])

@admin.action(description='Izbrisi oznaceno')
def delete_model(self, request, obj):
        for o in obj.all():
            o.delete()

@admin.register(Validacija)
class ValidationAdmin(admin.ModelAdmin):

    def get_actions(self, request):
        actions = super(ValidationAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def image1_tag(self, object): 
        return format_html('<img src="{}" height="200"/>'.format(object.getImage1()))

    image1_tag.short_description = 'Image1'

    def image2_tag(self, object): 
        return format_html('<img src="{}" height="200"/>'.format(object.getImage2()))

    image2_tag.short_description = 'Image2'

    list_display= ('verifikovan', 'user', 'image1_tag', 'image2_tag', )
    list_filter = (VerifikovanoFIlter,)
    search_fields = ('user__email',)
    actions = [verifikuj, odverifikuj, delete_model,]




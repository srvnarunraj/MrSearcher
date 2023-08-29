from django.contrib import admin
from Toolbar.models import SearchText
# Register your models here.
admin.site.register(SearchText)

admin.site.site_header="Mr Search Admin Login"
admin.site.site_title="Admin Portal"
admin.site.index_title="Mr Admin"



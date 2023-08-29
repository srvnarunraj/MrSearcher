from django.contrib import admin
from Toolbar.models import SearchText
# Register your models here.
admin.site.register(SearchText)

admin.site.site_header="Mr Searcher Portal"
admin.site.site_title="Mr Searcher Admin Login"
admin.site.index_title="Mr Searcher"
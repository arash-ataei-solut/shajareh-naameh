from django.contrib import admin

from places.models import Country, Province, City, Place, ResidencePlace


admin.site.register(Country)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(Place)
admin.site.register(ResidencePlace)

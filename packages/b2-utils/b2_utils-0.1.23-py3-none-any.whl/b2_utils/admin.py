from django.contrib import admin

from b2_utils import models


class AddressAdmin(admin.ModelAdmin):
    search_fields = ["zip_code", "district", "street", "number", "additional_info"]


class CityAdmin(admin.ModelAdmin):
    search_fields = ["name", "state"]


class PhoneAdmin(admin.ModelAdmin):
    search_fields = ["country_code", "area_code", "number"]


admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.City, CityAdmin)
admin.site.register(models.Phone, PhoneAdmin)

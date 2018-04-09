from django.contrib import admin
from gibdd_app import models
from django.contrib.auth.models import Permission

# Register your models here.


admin.site.register(Permission)
admin.site.register(models.Driver)
admin.site.register(models.Category)
admin.site.register(models.License)
admin.site.register(models.MedicalCertificate)
admin.site.register(models.AccidentReport)
admin.site.register(models.Inspector)
admin.site.register(models.Fine)
admin.site.register(models.Witness)
admin.site.register(models.Car)
admin.site.register(models.AutoSchool)
admin.site.register(models.Stealing)
admin.site.register(models.RegistrationCertificate)
admin.site.register(models.Owner)
admin.site.register(models.Insurance)
admin.site.register(models.DiagnosticCard)
admin.site.register(models.Decree)
# admin.site.register(models.PDD)
# admin.site.register(models.KOAP)
admin.site.register(models.CarHistory)
admin.site.register(models.LicenseDisqualification)
admin.site.register(models.Lisense_Category)
admin.site.register(models.Accident_Car)
admin.site.register(models.InsuranceLicense)
admin.site.register(models.Europrotocol)

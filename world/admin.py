from django.contrib import admin
from .models import Stainless, Tag, TensileStrength, YieldStrength, ThermodynamicProperty, Composition
# Register your models here.
admin.site.register([Stainless, Tag, TensileStrength, YieldStrength, ThermodynamicProperty, Composition])
from django.contrib import admin
from .models import Controller, IrrigationController, ValveController

admin.site.register(Controller)
admin.site.register(IrrigationController)
admin.site.register(ValveController)
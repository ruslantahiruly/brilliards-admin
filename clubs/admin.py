from django.contrib import admin

from .models import Country
from .models import Region
from .models import City
from .models import Club
from .models import Photo
from .models import WorkingTime
from .models import Hall
from .models import Game
from .models import Table
from .models import Price
from .models import Booking
from .models import SocialNetwork
from .models import Promotion

admin.site.register(Country)
admin.site.register(Region)
class CityAdmin(admin.ModelAdmin):
    fields = ('region', 'name', 'url',)
admin.site.register(City, CityAdmin)
class ClubAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Club, ClubAdmin)
admin.site.register(Photo)
admin.site.register(SocialNetwork)
admin.site.register(Promotion)
admin.site.register(WorkingTime)
admin.site.register(Hall)
class GameAdmin(admin.ModelAdmin):
    readonly_fields = ('read_club',)
    fields = ('hall', 'name', 'read_club',)
admin.site.register(Game, GameAdmin)
class TableAdmin(admin.ModelAdmin):
    readonly_fields = ('read_club', 'read_hall',)
    fields = ('game', 'name', 'size', 'read_club', 'read_hall',)
admin.site.register(Table, TableAdmin)
admin.site.register(Price)
class BookingAdmin(admin.ModelAdmin):
    # readonly_fields = ('read_club',)
    pass
admin.site.register(Booking, BookingAdmin)

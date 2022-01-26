from django.db import models
from django.urls import reverse
from django.conf import settings
from multiselectfield import MultiSelectField
from datetime import date, time, datetime
from django.utils.translation import gettext_lazy as _
import random
import string
from decimal import *

class Country(models.Model):
    name = models.CharField(_('name'), max_length=50)
    url = models.CharField(_('url'), max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')

class Region(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('country'))
    name = models.CharField(_('name'), max_length=50)
    def __str__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('country'))
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name=_('region'))
    name = models.CharField(_('name'), max_length=50)
    url = models.CharField(_('url'), max_length=50)
    def save(self, *args, **kwargs):
        self.country = self.region.country
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')

def club_code_number_generator(instance):
    code_number = ''.join(random.choices(string.digits, k=7))
    Club= instance.__class__
    qs_exists= Club.objects.filter(code_number=code_number).exists()
    if qs_exists:
        return club_code_number_generator(instance)
    return code_number

class Club(models.Model):
    CASH = 'CS'
    CARD = 'VS'
    # MASTERCARD = 'MC'
    # MIR = 'MR'
    PAYMENT_METHODS_CHOICES = (
        (CASH, 'Наличные'),
        (CARD, 'Карты'),
        # (MASTERCARD, 'MasterCard'),
        # (MIR, 'МИР'),
    )
    COMMERCIAL = 'CM'
    COMMERCIAL_SPORTS = 'CS'
    SPORTS = 'ST'
    ELITE = 'ET'
    TYPE_CHOICES = (
        (COMMERCIAL, 'коммерческий (развлекатальный)'),
        (COMMERCIAL_SPORTS, 'коммерческо-спортивный'),
        (SPORTS, 'спортивный'),
        (ELITE, 'элитный (закрытый)'),
    )
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('users'), blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('country'))
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name=_('region'))
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_('city'))
    name = models.CharField(_('name'), max_length=50)
    code_number = models.PositiveIntegerField(_('club number'), default=0)
    time_zone = models.DecimalField('time zone', max_digits=2, decimal_places=1, default=0)
    slug = models.SlugField(_('slug'), max_length=50, db_index=True)
    district = models.CharField(_('district'), max_length=50, blank=True)
    metro = models.CharField(_('metro'), max_length=50, blank=True)
    address = models.CharField(_('address'), max_length=100)
    house = models.CharField(_('находится в здании'), max_length=50, blank=True)
    entrance = models.CharField(_('вход'), max_length=100, blank=True)
    floor = models.CharField(_('floor'), max_length=50, blank=True)
    phone = models.CharField(_('phone'), max_length=50)
    email = models.EmailField(_('email'))
    requisites = models.TextField(_('requisites'), blank=True)
    type = models.CharField(_('type'), max_length=5, choices=TYPE_CHOICES, default=COMMERCIAL)
    works_since = models.CharField(_('works since'), max_length=50, blank=True)
    website = models.URLField(_('website'), blank=True)
    payment_methods = MultiSelectField(_('payment methods'), max_length=50, choices=PAYMENT_METHODS_CHOICES, default=CASH)
    billing = models.BooleanField(_('почасовая тарификация'), default=False)
    discount_cards = models.BooleanField(_('дисконтные карты'), default=False)
    school = models.BooleanField(_('school'), default=False)
    tournaments = models.BooleanField(_('tournaments'), default=False)
    shop = models.BooleanField(_('shop'), default=False)
    repair = models.BooleanField(_('мастерская'), default=False)
    cues_lockers = models.PositiveSmallIntegerField(_('шкафчики для киев'), default=0)
    is_pre_entry = models.BooleanField(_('entrance by appointment'), default=False)
    is_medical_masks = models.BooleanField(_('entrance only with medical masks'), default=False)
    is_qr_code = models.BooleanField(_('entrance by QR code'), default=False)
    is_active = models.BooleanField(_('club is active'), default=False)
    is_open = models.BooleanField(_('club is open'), default=True)
    is_verified = models.BooleanField(_('club is verified'), default=False)
    is_available_for_booking = models.BooleanField(_('club is available for booking'), default=False)
    parking = models.BooleanField(_('parking'), default=False)
    wardrobe = models.BooleanField(_('wardrobe'), default=False)
    wc = models.BooleanField(_('wc'), default=False)
    air_conditioning = models.BooleanField(_('air conditioning'), default=False)
    wifi = models.BooleanField(_('Wi-Fi'), default=False)
    smoking_room = models.BooleanField(_('smoking room'), default=False)
    vip_hall = models.BooleanField(_('VIP hall'), default=False)
    barroom = models.BooleanField(_('barroom'), default=False)
    kitchen = models.BooleanField(_('kitchen'), default=False)
    sports_broadcasts = models.BooleanField(_('sports broadcasts'), default=False)
    table_reservation = models.BooleanField(_('table reservation'), default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    def save(self, *args, **kwargs):
        self.region = self.city.region
        self.country = self.city.region.country
        if not self.code_number:
            self.code_number = club_code_number_generator(self)
        super().save(*args, **kwargs)
    def __str__(self):
        return '%s, %s' % (self.name, self.city)
    def get_absolute_url(self):
        return reverse('clubs:club_detail', kwargs={'city': self.city.url, 'club_slug': self.slug })

class SocialNetwork(models.Model):
    VK = 'VK'
    OK = 'OK'
    FACEBOOK = 'FB'
    TWITTER = 'TW'
    TELEGRAM = 'TM'
    INSTAGRAM = 'IN'
    YOUTUBE = 'UT'
    TIKTOK = 'TT'
    NAME_CHOICES = (
        (VK, 'Вконтакте'),
        (OK, 'Одноклассники'),
        (FACEBOOK, 'Facebook'),
        (TWITTER, 'Twitter'),
        (TELEGRAM, 'Telegram'),
        (INSTAGRAM, 'Instagram'),
        (YOUTUBE, 'YouTube'),
        (TIKTOK, 'Tiktok'),
    )
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name=_('club'), related_name='social_networks')
    name = models.CharField(_('name'), max_length=5, choices=NAME_CHOICES)
    address = models.URLField(_('account'))
    def __str__(self):
        return self.name

def random_string_generator(size=18, chars=string.digits + string.digits + string.ascii_lowercase + string.digits + string.digits + string.ascii_lowercase + string.digits + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def update_filename(instance, filename):
    ext = filename.split('.')[-1]
    file_name = random_string_generator()
    return 'uploads/{0}.{1}'.format(file_name, ext)

class Photo(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name=_('club'), related_name='photos')
    file = models.ImageField(_('photo'), upload_to=update_filename)
    is_main = models.BooleanField(_('main photo'), default=False)
    def __str__(self):
        return 'Photo %s' % self.file

class WorkingTime(models.Model):
    MONDAY = 'MO'
    TUESDAY = 'TU'
    WEDNESDAY = 'WE'
    THURSDAY = 'TH'
    FRIDAY = 'FR'
    SATURDAY = 'SA'
    SUNDAY = 'SU'
    NAME_CHOICES = (
        (MONDAY, 'понедельник'),
        (TUESDAY, 'вторник'),
        (WEDNESDAY, 'среда'),
        (THURSDAY, 'четверг'),
        (FRIDAY, 'пятница'),
        (SATURDAY, 'суббота'),
        (SUNDAY, 'воскресенье'),
    )
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name=_('club'), related_name='working_times')
    name = models.CharField(_('day of the week'), max_length=2, choices=NAME_CHOICES)
    opening_time = models.TimeField(_('opening time'), null=True, blank=True)
    closing_time = models.TimeField(_('closing time'), null=True, blank=True)
    day_off = models.BooleanField(_('day off'), default=False)
    is_available_for_booking = models.BooleanField(_('day is available for booking'), default=True)
    @property
    def duration(self):
        if self.opening_time and self.closing_time:
            opening_time_str = self.opening_time.strftime('%H:%M')
            closing_time_str = self.closing_time.strftime('%H:%M')
            if opening_time_str == '00:00' and closing_time_str == '00:00':
                return 24
            else:
                delta = datetime.combine(date(1,1,1), self.closing_time) - datetime.combine(date(1,1,1), self.opening_time)
                delta = delta.seconds / 3600
                delta = int(delta)
                return delta
        else:
            return 0
    def __str__(self):
        return '%s' % self.get_name_display()
    class Meta:
        verbose_name = _('working time')
        verbose_name_plural = _('working time')

class Hall(models.Model):
    COMMON = 'CM'
    VIP = 'VP'
    TYPE_CHOICES = (
        (COMMON, 'Общий'),
        (VIP, 'VIP'),
    )
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name=_('club'), related_name='halls')
    name = models.CharField(_('hall'), max_length=50, blank=True)
    type = models.CharField(_('type'), max_length=5, choices=TYPE_CHOICES, default=COMMON)
    is_available_for_booking = models.BooleanField(_('hall is available for booking'), default=True)
    booking_duration = models.PositiveSmallIntegerField(_('duration of booking'), default=2)
    booking_days_in_advance = models.PositiveSmallIntegerField('количество дней вперед для бронирования', default=7)
    booking_hours_before = models.PositiveSmallIntegerField('количество часов до бронирования', default=1)
    booking_step = models.TimeField('шаг брони', default='00:30')
    def __str__(self):
        return self.get_type_display()

class Game(models.Model):
    RUSSIAN = 'RS'
    POOL = 'PL'
    SNOOKER = 'SK'
    CAROM = 'CR'
    GAME_CHOICES = (
        (RUSSIAN, 'Русский бильярд'),
        (POOL, 'Пул'),
        (SNOOKER, 'Снукер'),
        (CAROM, 'Карамболь'),
    )
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name=_('club'), related_name='games')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name=_('hall'), related_name='games')
    name = models.CharField(_('game'), max_length=5, choices=GAME_CHOICES, default=RUSSIAN)
    is_available_for_booking = models.BooleanField(_('game is available for booking'), default=True)
    booking_duration = models.PositiveSmallIntegerField(_('duration of booking'), default=2)
    booking_days_in_advance = models.PositiveSmallIntegerField('количество дней вперед для бронирования', default=7)
    booking_hours_before = models.PositiveSmallIntegerField('количество часов до бронирования', default=1)
    booking_step = models.TimeField('шаг брони', default='00:30')
    def __str__(self):
        return self.get_name_display()
    # ****************
    @property
    def read_club(self):
        return self.club
    def save(self, *args, **kwargs):
        self.club = self.hall.club
        super().save(*args, **kwargs)

class Table(models.Model):
    TWELVE = '12'
    ELEVEN = '11'
    TEN = '10'
    NINE = '9'
    EIGHT = '8'
    SIZE_CHOICES = (
        (TWELVE, '12 футов'),
        (ELEVEN, '11 футов'),
        (TEN, '10 футов'),
        (NINE, '9 футов'),
        (EIGHT, '8 футов'),
    )
    START = 'ST'
    RUPTUR = 'RP'
    ARSENAL = 'AR'
    IGRA = 'IR'
    DYNAMIC = 'DN'
    BRUNSWICK = 'BR'
    OTHER = 'OT'
    BRAND_CHOICES = (
        (START, 'Фабрика "Старт"'),
        (RUPTUR, 'РуптуР'),
        (ARSENAL, 'Брянская бильярдная фабрик "Арсенал"'),
        (IGRA, 'Московская бильярдная фабрика "Игра"'),
        (DYNAMIC, 'Dynamic'),
        (BRUNSWICK, 'Brunswick'),
        (OTHER, 'Другой'), 
    )
    MANCHESTER = 'MN'
    GALAXY = 'GL'
    IWAN_SIMONIS = 'IW'
    MILLIKEN = 'ML'
    CLOTH_CHOICES = (
        (MANCHESTER, 'Manchester'),
        (GALAXY, 'Galaxy'),
        (IWAN_SIMONIS, 'Iwan Simonis'),
        (MILLIKEN, 'Milliken'),
    )
    CUETEC = 'CT'
    CUES_CHOICES = (
        (CUETEC, 'Cuetec'),
    )
    ARAMITH = 'AR'
    BALLS_CHOICES = (
        (ARAMITH, 'Aramith'),
    )
    REGULAR = 'RG'
    HEATED = 'HT'
    DOUBLE_ILLUMINATION = 'DI'
    CORNER = 'CN'
    TYPE_CHOICES = (
        (REGULAR, 'Обычный стол'),
        (HEATED, 'Стол с подогревом'),
        (DOUBLE_ILLUMINATION, 'Стол с двойным освещением'),
        (CORNER, 'Угловой стол'),
    )
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name=_('club'))
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name=_('hall'))
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name=_('game'), related_name='tables')
    name = models.CharField(_('table number'), max_length=5)
    quantity = models.PositiveSmallIntegerField('количество', default=1)
    type = MultiSelectField(_('type'), max_length=50, choices=TYPE_CHOICES, default=REGULAR)
    size = models.CharField(_('size'), max_length=5, choices=SIZE_CHOICES, blank=True)
    brand = models.CharField(_('brand'), max_length=5, choices=BRAND_CHOICES, blank=True)
    cloth = models.CharField(_('cloth'), max_length=5, choices=CLOTH_CHOICES, blank=True)
    cues = models.CharField(_('cues'), max_length=5, choices=CUES_CHOICES, blank=True)
    balls = models.CharField(_('balls'), max_length=5, choices=BALLS_CHOICES, blank=True)
    description = models.CharField(_('description'), max_length=50, blank=True)
    is_available_for_booking = models.BooleanField(_('table is available for booking'), default=True)
    booking_duration = models.PositiveSmallIntegerField(_('duration of booking'), default=2)
    booking_days_in_advance = models.PositiveSmallIntegerField('количество дней вперед для бронирования', default=7)
    booking_hours_before = models.PositiveSmallIntegerField('количество часов до бронирования', default=1)
    booking_step = models.TimeField('шаг брони', default='00:30')
    def __str__(self):
        return 'Стол %s, %s, %s, %s' % (self.name, self.game, self.hall, self.club)
    # *************
    @property
    def read_club(self):
        return self.club
    @property
    def read_hall(self):
        return self.hall
    def save(self, *args, **kwargs):
        self.club = self.game.hall.club
        self.hall = self.game.hall
        super().save(*args, **kwargs)

class Price(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name=_('club'), null=True, blank=True, related_name='prices')
    tables = models.ManyToManyField(Table, verbose_name=_('tables'))
    working_times = models.ManyToManyField(WorkingTime, verbose_name=_('working times'))
    price_from = models.TimeField(_('from'))
    price_to = models.TimeField(_('to'))
    value = models.DecimalField('цена', max_digits=7, decimal_places=2)
    description = models.CharField(_('description'), max_length=50, blank=True)
    is_available_for_booking = models.BooleanField(_('hours are available for booking'), default=True)
    def __str__(self):
        return 'Price %s' % self.value

class Promotion(models.Model):
    DISCOUNT = 'DC'
    CERTIFICATE = 'CR'
    OTHER = 'OT'
    TYPE_CHOICES = (
        (DISCOUNT, 'Скидка'),
        (CERTIFICATE, 'Подарочный сертификат'),
        (OTHER, 'Остальные'),
    )
    MONDAY = 'MO'
    TUESDAY = 'TU'
    WEDNESDAY = 'WE'
    THURSDAY = 'TH'
    FRIDAY = 'FR'
    SATURDAY = 'SA'
    SUNDAY = 'SU'
    DAYS_OF_THE_WEEK_CHOICES = (
        (MONDAY, 'Пн'),
        (TUESDAY, 'Вт'),
        (WEDNESDAY, 'Ср'),
        (THURSDAY, 'Чт'),
        (FRIDAY, 'Пт'),
        (SATURDAY, 'Сб'),
        (SUNDAY, 'Вс'),
    )
    ALL = 'AL'
    RETIREE = 'RT'
    PUPIL = 'PP'
    STUDENT = 'ST'
    BIRTHDAY = 'BD'
    REG_CUSTOMER = 'RC'
    SUBSCRIBER = 'SB'
    CUSTOMER_CATEGORIES_CHOICES = (
        (ALL, 'Всем'),
        (RETIREE, 'Пенсионерам'),
        (PUPIL, 'Школьникам'),
        (STUDENT, 'Студентам'),
        (BIRTHDAY, 'Именинникам'),
        (REG_CUSTOMER, 'Постоянным клиентам'),
        (SUBSCRIBER, 'Подписчикам'),
    )
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name=_('club'), null=True, blank=True, related_name='promotions')
    tables = models.ManyToManyField(Table, verbose_name=_('tables'))
    name = models.CharField(_('promotion'), max_length=50)
    type = models.CharField(_('type'), max_length=5, choices=TYPE_CHOICES, default=DISCOUNT)
    customer_categories = MultiSelectField(_('customer categories'), max_length=20, choices=CUSTOMER_CATEGORIES_CHOICES, default=ALL)
    is_active = models.BooleanField('промоакция активна', default=True)
    is_perpetual = models.BooleanField('промоакция бессрочная', default=True)
    date_from = models.DateTimeField('date from', null=True, blank=True)
    date_to = models.DateTimeField('date to', null=True, blank=True)
    days_of_the_week = MultiSelectField(_('days of the week'), max_length=20, choices=DAYS_OF_THE_WEEK_CHOICES, blank=True)
    time_from = models.TimeField(_('time from'), null=True, blank=True)
    time_to = models.TimeField(_('time to'), null=True, blank=True)
    discount = models.PositiveSmallIntegerField(_('discount'), default=0)
    promo_code = models.CharField(_('promo code'), max_length=50, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

def unique_code_number_generator(instance):
    code_number = ''.join(random.choices(string.digits, k=8))
    Booking= instance.__class__
    qs_exists= Booking.objects.filter(code_number=code_number).exists()
    if qs_exists:
        return unique_code_number_generator(instance)
    return code_number

class Booking(models.Model):
    ACCEPTED = 'AC'
    CANCELED = 'CN'
    ACTIVE = 'AT'
    COMPLETED = 'CP'
    PAID = 'PD'
    STATUS_CHOICES = (
        (ACCEPTED, 'подтверждено'),
        (CANCELED, 'отменено'),
        (ACTIVE, 'активно'),
        (COMPLETED, 'завершено'),
        (PAID, 'оплачено'),
    )
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name=_('club'))
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name=_('hall'))
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name=_('game'))
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name=_('table'))
    start = models.DateTimeField('время начала')
    end = models.DateTimeField('время окончания')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField('статус', max_length=3, choices=STATUS_CHOICES, default=ACCEPTED)
    code_number = models.PositiveIntegerField('номер брони')
    client_name = models.CharField('имя', max_length=50)
    client_email = models.EmailField('email', blank=True)
    cost = models.DecimalField('стоимость', max_digits=7, decimal_places=2)
    commission = models.DecimalField('комиссия', max_digits=7, decimal_places=2)
    def __str__(self):
        return 'Booking %s' % self.code_number
    def save(self, *args, **kwargs):
        self.club = self.table.game.hall.club
        self.hall = self.table.game.hall
        self.game = self.table.game
        self.commission = self.cost * Decimal(0.05)
        if not self.code_number:
            self.code_number = unique_code_number_generator(self)
        super().save(*args, **kwargs)

class TableHolding(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name=_('table'))
    start = models.DateTimeField('время начала')
    end = models.DateTimeField('время окончания')

class NotAvailableTime(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name=_('club'), null=True, blank=True)
    tables = models.ManyToManyField(Table, verbose_name=_('tables'))
    start = models.DateTimeField('недоступен с')
    end = models.DateTimeField('недоступен до')
    def __str__(self):
        return 'not available time %s' % self.id
    class Meta:
        verbose_name = 'not available time'
        verbose_name_plural = 'not available time'

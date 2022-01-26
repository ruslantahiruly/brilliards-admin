from django.forms import ModelForm
from django import forms
from .models import Country, Region, City, Club, Photo, WorkingTime, Hall, Game, Table, Price, Booking

class ClubCreateForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    # error_messages = {
    #     'required': _("This field is required."),
    # }
    city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label='Город')
    class Meta:
        model = Club
        fields = ['city', 'name', 'address', 'phone', 'email',]
        widgets = {
            'city': forms.Select(attrs={'data-placeholder' : 'Город'}),
            'name': forms.TextInput(attrs={'placeholder': 'Название клуба', 'autocomplete': 'off'}),
            'address': forms.TextInput(attrs={'placeholder': 'Адрес', 'autocomplete': 'off'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон', 'class': 'phone', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'autocomplete': 'off'}),
        }

class ClubUpdateForm(ModelForm):
    class Meta:
        model = Club
        fields = ['city', 'name', 'address', 'phone', 'email', 'requisites', 'is_active', 'is_open', 'is_available_for_booking', 'parking', 'wifi', 'wardrobe', 'wc', 'barroom', 'air_conditioning', 'smoking_room', 'vip_hall', 'kitchen', 'sports_broadcasts', 'table_reservation',]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название клуба', 'autocomplete': 'off'}),
            'district': forms.TextInput(attrs={'placeholder' : 'Район'}),
            'address': forms.TextInput(attrs={'placeholder': 'Адрес', 'autocomplete': 'off'}),
            'metro': forms.TextInput(attrs={'placeholder': 'Метро (если есть)'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'autocomplete': 'off'}),
            'requisites': forms.Textarea(attrs={'placeholder': 'Наименование и юридический адрес (необходимы для выставления счета)', 'autocomplete': 'off'}),
            # 'available_for_booking': forms.CheckboxInput(attrs={'class': 'left-checkbox'}),
            # 'club_payment_methods': forms.CheckboxSelectMultiple(),
            # 'club_website': forms.URLInput(attrs={'placeholder': 'Официальный сайт'}),
        }
        labels = {
            'city': 'Город',
            'name': 'Название',
            'address': 'Адрес',
            'phone': 'Телефон',
            'requisites': 'Реквизиты',
            'is_available_for_booking': 'Клуб открыт для бронирования',
            'is_active': 'Клуб активирован',
            'parking': 'Парковка',
            'wifi': 'Wi-Fi',
            'wardrobe': 'Гардероб',
            'wc': 'Туалет',
            'air_conditioning': 'Кондиционер',
            'vip_hall': 'VIP-зал',
            'smoking_room': 'Зал для курящих',
            'barroom': 'Бар',
            'kitchen': 'Кухня',
            'sports_broadcasts': 'Спортивные трансляции',
            'table_reservation': 'Бронирование столов',
        }

class WorkingTimeForm(ModelForm):
    class Meta:
        model = WorkingTime
        fields = ['opening_time', 'closing_time', 'day_off', 'is_available_for_booking',]
        widgets = {
            'opening_time': forms.TextInput(attrs={'placeholder': 'С', 'class': 'working-hours-input', 'autocomplete': 'off'}),
            'closing_time': forms.TextInput(attrs={'placeholder': 'До', 'class': 'working-hours-input', 'autocomplete': 'off'}),
        }
        labels = {
            'opening_time': 'Время открытия',
            'closing_time': 'Время закрытия',
            'day_off': 'Выходной день',
        }

class HallForm(ModelForm):
    class Meta:
        model = Hall
        fields = ['name', 'type']
        widgets = {
            # 'name': forms.TextInput(attrs={'placeholder': 'Зал'}),
            'name': forms.TextInput(attrs={'autocomplete': 'off'}),
        }
        labels = {
            'name': 'Название',
            'type': 'Тип',
        }

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name',]
        widgets = {
            # 'game_kind_name': forms.CheckboxSelectMultiple,
            # 'name': forms.TextInput(attrs={'autocomplete': 'off'}),
        }
        labels = {
            'name': 'Игра',
        }

class TableForm(ModelForm):
    class Meta:
        model = Table
        fields = ['name', 'quantity', 'size', 'description', 'type', 'brand', 'cloth', 'cues', 'balls']
        widgets = {
            # 'game_kind_name': forms.CheckboxSelectMultiple,
            'name': forms.TextInput(attrs={'autocomplete': 'off'}),
        }
        labels = {
            'name': 'Номер стола',
            'quantity': 'Количество столов',
            'size': 'Размер стола',
            'description': 'Описание стола',
            'type': 'Тип стола',
            'brand': 'Производитель стола',
            'cloth': 'Сукно стола',
            'cues': 'Кии стола',
            'balls': 'Шары стола',
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['hall'].queryset = Hall.objects.filter(club_id=self.instance.club.id)

class TableAdminForm(ModelForm):
    class Meta:
        model = Table
        fields = '__all__'
        widgets = {
            # 'game_kind_name': forms.CheckboxSelectMultiple,
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hall'].queryset = Hall.objects.filter(club=self.instance.club)
        self.fields['game_kind'].queryset = GameKind.objects.filter(hall=self.instance.hall)

class PriceForm(ModelForm):
    class Meta:
        model = Price
        fields = ['club', 'tables', 'working_times', 'price_from', 'price_to', 'value', 'description',]
        widgets = {
            'tables': forms.SelectMultiple(attrs={'class': 'price-select', 'autocomplete': 'off', 'size': '7'}),
            'working_times': forms.SelectMultiple(attrs={'class': 'price-select', 'autocomplete': 'off', 'size': '7'}),
            'price_from': forms.TextInput(attrs={'class': 'price-hours-input', 'autocomplete': 'off'}),
            'price_to': forms.TextInput(attrs={'class': 'price-hours-input', 'autocomplete': 'off'}),
            'value': forms.TextInput(attrs={'class': 'price-hours-value', 'autocomplete': 'off'}),
            'description': forms.TextInput(attrs={'class': '', 'autocomplete': 'off'}),
        }
        labels = {
            'tables': 'Столы',
            'working_times': 'Дни',
            'price_from': 'С',
            'price_to': 'До',
            'value': 'Цена',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.fields['tables'].queryset = Table.objects.filter(club=self.initial['club'])
            self.fields['working_times'].queryset = WorkingTime.objects.filter(club=self.initial['club'])

class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['club', 'file',]
        widgets = {
            # 'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class BookingCreateForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['table', 'start', 'end', 'client_name', 'cost',]
        widgets = {
            'client_name': forms.TextInput(attrs={'placeholder': 'Ваше имя','autocomplete': 'off'}),
            # 'cost': forms.TextInput(),
            # 'booking_date': forms.DateInput(attrs={'placeholder': 'Дата', 'id': 'datepicker', 'autocomplete': 'off'}),
            # 'start': forms.TimeInput(attrs={'placeholder': 'Время начала'}),
            # 'end': forms.TimeInput(attrs={'placeholder': 'Время окончания'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs:
            pass
            # self.fields['table'].queryset = Table.objects.filter(game=self.initial['game'])
        # booking_date = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"))

class BookingUpdateForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['status',]
        widgets = {
            # 'cost': forms.TextInput(attrs={'disabled': 'true'}),
            # 'client_name': forms.TextInput(attrs={'placeholder': 'Ваше имя','autocomplete': 'off'}),
            # 'booking_date': forms.DateInput(attrs={'placeholder': 'Дата', 'id': 'datepicker', 'autocomplete': 'off'}),
            # 'start': forms.TimeInput(attrs={'placeholder': 'Время начала'}),
            # 'end': forms.TimeInput(attrs={'placeholder': 'Время окончания'}),
        }

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.contrib.auth.models import User
from .models import Country, Region, City, Club, Photo, WorkingTime, Hall, Game, Table, Price, Booking
from .forms import ClubCreateForm, ClubUpdateForm, PhotoForm, WorkingTimeForm, HallForm, GameForm, TableForm, PriceForm, BookingCreateForm, BookingUpdateForm
from .mixins import AjaxableResponseMixin
from django.contrib.gis.geoip2 import GeoIP2
from django.core.paginator import Paginator
from datetime import date, time, datetime, timedelta
from decimal import *
from django.db.models import Q

class IndexView(TemplateView):
    """Display index page."""
    template_name = 'clubs/index.html'
    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            if self.request.GET.get('city'):
                user_city = self.request.GET.get('city')
                request.session['user_city'] = user_city
                city = City.objects.get(url=user_city)
                context = {}
                context['city'] = city
                city_list = City.objects.all()

                club_list = Club.objects.filter(city=city).filter(is_verified=True).filter(is_active=True)[:3]
                context['club_list'] = club_list

                context['city_list'] = city_list
                return render(request, self.template_name, context)
        else:
            if request.session.get('user_city', False):
                user_city = self.request.session['user_city']
                city = City.objects.get(url=user_city)
                context = {}
                context['city'] = city
                city_list = City.objects.all()

                club_list = Club.objects.filter(city=city).filter(is_verified=True).filter(is_active=True)[:3]
                context['club_list'] = club_list

                context['city_list'] = city_list
                return render(request, self.template_name, context)
            else:
                if City.objects.exists():
                    # g = GeoIP2()
                    # x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
                    # if x_forwarded_for:
                    #     ip = x_forwarded_for.split(',')[0]
                    # else:
                    #     ip = self.request.META.get('REMOTE_ADDR')
                    # if ip:
                    #     ip_city = g.city(ip)['city']
                    #     if City.objects.filter(url__icontains=ip_city).exists():
                    #         user_city = City.objects.get(url__icontains=ip_city).url
                    #     else:
                    #         user_city = 'moscow'
                    # else:
                    #     user_city = 'moscow'
                    user_city = 'moscow'
                    request.session['user_city'] = user_city
                    city = City.objects.get(url=user_city)
                    context = {}
                    context['city'] = city
                    city_list = City.objects.all()

                    club_list = Club.objects.filter(city=city).filter(is_verified=True).filter(is_active=True)[:3]
                    context['club_list'] = club_list

                    context['city_list'] = city_list
                    return render(request, self.template_name, context)
                else:
                    return render(request, self.template_name)

class AboutView(TemplateView):
    """Display the about page."""
    template_name = 'clubs/about.html'

class ClubListView(ListView):
    """Display clubs list by city."""
    template_name = 'clubs/club_list.html'
    context_object_name = 'club_list'
    # paginate_by = 3
    def get_queryset(self):
        city = City.objects.get(url=self.kwargs['city'])
        return Club.objects.filter(city=city).filter(is_verified=True).filter(is_active=True)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = City.objects.get(url=self.kwargs['city'])
        city_list = City.objects.all()
        context['city'] = city
        context['city_list'] = city_list
        return context

class ClubDetailView(DetailView):
    """Display club's detail."""
    slug_field = 'slug'
    slug_url_kwarg = 'club_slug'
    template_name = 'clubs/club_detail.html'
    context_object_name = 'club'
    def get_object(self):
        city = City.objects.get(url=self.kwargs['city'])
        return Club.objects.filter(city=city).get(slug=self.kwargs['club_slug'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = City.objects.get(url=self.kwargs['city'])
        club = Club.objects.filter(city=city).get(slug=self.kwargs['club_slug'])
        games_src = club.games.all()
        if games_src.exists():
            games = []
            game_names = []
            for game in games_src:
                if game.name not in game_names:
                    game_names.append(game.name)
                    games.append(game)
            context['games'] = games
        prices = club.prices.all()
        if prices.exists():
            values = []
            for price in prices:
                values.append(price.value)
            price_min = min(values)
            price_max = max(values)
            price_min = price_min.quantize(Decimal('1'))
            price_max = price_max.quantize(Decimal('1'))
            context['price_min'] = price_min
            context['price_max'] = price_max
        workingtimes = club.working_times.all()
        days = {}
        opening_time = None
        closing_time = None
        name = None
        name_plus = None
        days_trans = {
            'MO': 'Пн',
            'TU': 'Вт',
            'WE': 'Ср',
            'TH': 'Чт',
            'FR': 'Пт',
            'SA': 'Сб',
            'SU': 'Вс',
        }
        for workingtime in workingtimes:
            if opening_time and closing_time:
                name_new = workingtime.name
                for key, value in days_trans.items():
                    if key == name_new:
                        name_new = value
                opening_time_new = workingtime.opening_time.strftime('%H:%M')
                closing_time_new = workingtime.closing_time.strftime('%H:%M')
                if opening_time == opening_time_new and closing_time == closing_time_new:
                    days.pop(name, None)
                    days[name +'-'+ name_new] = opening_time + ' – ' + closing_time
                else:
                    opening_time = opening_time_new
                    closing_time = closing_time_new
                    name = name_new
                    days[name_new] = opening_time + ' – ' + closing_time

            else:
                name = workingtime.name
                for key, value in days_trans.items():
                    if key == name:
                        name = value
                # if not workingtime.day_off:
                opening_time = workingtime.opening_time.strftime('%H:%M')
                closing_time = workingtime.closing_time.strftime('%H:%M')
                days[name] = opening_time + ' – ' + closing_time
                # else:
                #     days[name] = 'Выходной'

        days_key = None
        days_value = None
        for key, value in list(days.items()):
            if days_value == value:
                days.pop(days_key, None)
            days_value = value
            days_key = key
        context['city'] = city
        context['days'] = days
        city_list = City.objects.all()
        context['city_list'] = city_list
        return context

class ClubCreateView(AjaxableResponseMixin, CreateView):
    """Display the club creating form."""
    model = Club
    form_class = ClubCreateForm
    template_name = 'clubs/club_create_form.html'
    success_url = '/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get('user_city', False):
            user_city = self.request.session['user_city']
            city = City.objects.get(url=user_city)
            context['city'] = city
            city_list = City.objects.all()
            context['city_list'] = city_list
        return context

class ClubUpdateView(LoginRequiredMixin, AjaxableResponseMixin, UpdateView):
    """Display the club updating form."""
    model = Club
    form_class = ClubUpdateForm
    template_name = 'clubs/extranet/club/club_update_form.html'
    success_url = '/'

class ExtranetBookingUpdateView(LoginRequiredMixin, AjaxableResponseMixin, UpdateView):
    """Display the club updating form."""
    model = Booking
    form_class = BookingUpdateForm
    template_name = 'clubs/extranet/extranet_booking_update_form.html'
    success_url = '/'

class ExtranetBookingCreateView(LoginRequiredMixin, FormView):
    """Display booking creation form."""
    def post(self, request, *args, **kwargs):
        booking_form = BookingCreateForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save()
            if self.request.is_ajax():
                data = {
                    'pk': booking.id,
                    'codeNumber': booking.code_number,
                }
                return JsonResponse(data)
            else:
                return HttpResponseRedirect(reverse('clubs:club_list'))
    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            if self.request.GET.get('day_of_the_week'):
                # city = City.objects.get(url=self.kwargs['city'])
                day_of_the_week = self.request.GET.get('day_of_the_week')
                booking_day = self.request.GET.get('booking_day')
                table = self.request.GET.get('table')
                # table = Table.objects.get(pk=table)
                club = Club.objects.get(pk=self.kwargs['pk'])
                workingtime = WorkingTime.objects.filter(club=club).get(name=day_of_the_week)
                club = self.request.GET.get('club')
                start = workingtime.opening_time
                end = workingtime.closing_time
                duration = workingtime.duration * 2
                duration = range(duration)
                steps = {}
                time = None
                for value in duration:
                    if time != None:
                        steps[value] = time.time
                        time = time + timedelta(minutes=30)
                    else:
                        steps[value] = start
                        time = datetime.combine(date(1,1,1), start) + timedelta(minutes=30)
                context = {}
                context['day_of_the_week'] = day_of_the_week
                context['booking_day'] = booking_day
                context['table'] = table
                context['club'] = club
                context['steps'] = steps
                context['workingtime'] = workingtime
                return render(request, 'clubs/extranet/time.html', context)
            if self.request.GET.get('start_time'):
                # city = City.objects.get(url=self.kwargs['city'])
                club = self.request.GET.get('club')
                club = Club.objects.get(pk=club)
                # next_day = self.request.GET.get('next_day')
                # next_day = int(next_day)
                next_day = 0
                start_date = self.request.GET.get('booking_date')
                start_date = datetime.strptime(start_date,'%Y-%m-%d') + timedelta(days=next_day)
                start_date = start_date.strftime('%Y-%m-%d')
                start_time = self.request.GET.get('start_time')
                end_time = self.request.GET.get('end_time')
                end_date = datetime.strptime(start_date,'%Y-%m-%d') + timedelta(days=1)
                end_date = end_date.date()
                end_date = end_date.strftime('%Y-%m-%d')
                start_booking = datetime.strptime(start_time,'%H:%M').time()
                end_booking = datetime.strptime(end_time,'%H:%M').time()
                if datetime.combine(date(1,1,1), start_booking) > datetime.combine(date(1,1,1), end_booking):
                    start = start_date + ' ' + start_time
                    end = end_date + ' ' + end_time
                else:
                    start = start_date + ' ' + start_time
                    end = start_date + ' ' + end_time
                start_form = datetime.strptime(start,'%Y-%m-%d %H:%M')
                end_form = datetime.strptime(end,'%Y-%m-%d %H:%M')
                table = self.request.GET.get('selected_table')
                table = Table.objects.get(pk=table)
                day_of_the_week = self.request.GET.get('week_day')
                workingtime = WorkingTime.objects.filter(club=club).get(name=day_of_the_week)
                prices = Price.objects.filter(tables=table).filter(working_times=workingtime)
                cost = 0
                cost_cur_1 = 0
                cost_cur_2 = 0
                cost_cur_3 = 0
                for price in prices:
                    print('3333333333333333333333')
                    if datetime.combine(date(1,1,1), start_booking) > datetime.combine(date(1,1,1), end_booking):
                        print('55555555555555555555555555555')
                        if datetime.combine(date(1,1,1), price.price_from) > datetime.combine(date(1,1,1), price.price_to):
                            if datetime.combine(date(1,1,1), price.price_from) <= datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,2), price.price_to) >= datetime.combine(date(1,1,2), end_booking):
                                if cost_cur_1 == 0:
                                    booking_duration = datetime.combine(date(1,1,2), end_booking) - datetime.combine(date(1,1,1), start_booking)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_1 = price.value * booking_duration
                                    cost = cost + cost_cur_1
                                    cost = cost.quantize(Decimal("1"))
                                    print('!!!!!!!!!!!!!!!!!!',cost)
                            elif datetime.combine(date(1,1,1), price.price_from) < datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,2), price.price_to) < datetime.combine(date(1,1,2), end_booking) and datetime.combine(date(1,1,2), price.price_to) > datetime.combine(date(1,1,1), start_booking):
                                if cost_cur_2 == 0:
                                    booking_duration = datetime.combine(date(1,1,2), price.price_to) - datetime.combine(date(1,1,1), start_booking)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_2 = price.value * booking_duration
                                    cost = cost + cost_cur_2
                                    cost = cost.quantize(Decimal("1"))
                                    print('?????????????????????',cost)
                            elif datetime.combine(date(1,1,1), price.price_from) > datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,2), price.price_to) > datetime.combine(date(1,1,2), end_booking) and datetime.combine(date(1,1,1), price.price_from) < datetime.combine(date(1,1,2), end_booking):
                                if cost_cur_3 == 0:
                                    booking_duration = datetime.combine(date(1,1,2), end_booking) - datetime.combine(date(1,1,1), price.price_from)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_3 = price.value * booking_duration
                                    cost = cost + cost_cur_3
                                    cost = cost.quantize(Decimal("1"))
                                    print('********************',cost)
                        else:
                            if datetime.combine(date(1,1,1), price.price_from) < datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,1), price.price_to) < datetime.combine(date(1,1,1), end_booking) and datetime.combine(date(1,1,1), price.price_to) > datetime.combine(date(1,1,1), start_booking):
                                if cost_cur_2 == 0:
                                    booking_duration = datetime.combine(date(1,1,1), price.price_to) - datetime.combine(date(1,1,1), start_booking)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_2 = price.value * booking_duration
                                    cost = cost + cost_cur_2
                                    cost = cost.quantize(Decimal("1"))
                                    print('?????????????????????',cost)
                            elif datetime.combine(date(1,1,1), price.price_from) > datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,1), price.price_to) > datetime.combine(date(1,1,1), end_booking) and datetime.combine(date(1,1,1), price.price_from) < datetime.combine(date(1,1,1), end_booking):
                                if cost_cur_3 == 0:
                                    booking_duration = datetime.combine(date(1,1,1), end_booking) - datetime.combine(date(1,1,1), price.price_from)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_3 = price.value * booking_duration
                                    cost = cost + cost_cur_3
                                    cost = cost.quantize(Decimal("1"))
                                    print('********************',cost)
                    else:
                        if datetime.combine(date(1,1,1), price.price_from) > datetime.combine(date(1,1,1), price.price_to):
                            if datetime.combine(date(1,1,1), price.price_from) > datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,1), price.price_to) >= datetime.combine(date(1,1,1), end_booking):
                                if cost_cur_1 == 0:
                                    booking_duration = datetime.combine(date(1,1,1), end_booking) - datetime.combine(date(1,1,1), start_booking)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_1 = price.value * booking_duration
                                    cost = cost + cost_cur_1
                                    cost = cost.quantize(Decimal("1"))
                                    print('!!!!!!!!!!!!!!!!!!',cost)
                            elif datetime.combine(date(1,1,1), price.price_from) > datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,1), price.price_to) < datetime.combine(date(1,1,1), end_booking) and datetime.combine(date(1,1,1), price.price_to) > datetime.combine(date(1,1,1), start_booking):
                                if cost_cur_2 == 0:
                                    booking_duration = datetime.combine(date(1,1,1), price.price_to) - datetime.combine(date(1,1,1), start_booking)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_2 = price.value * booking_duration
                                    cost = cost + cost_cur_2
                                    cost = cost.quantize(Decimal("1"))
                                    print('?????????????????????',cost)
                        else:
                            if datetime.combine(date(1,1,1), price.price_from) <= datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,1), price.price_to) >= datetime.combine(date(1,1,1), end_booking):
                                if cost_cur_1 == 0:
                                    booking_duration = datetime.combine(date(1,1,1), end_booking) - datetime.combine(date(1,1,1), start_booking)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_1 = price.value * booking_duration
                                    cost = cost + cost_cur_1
                                    cost = cost.quantize(Decimal("1"))
                                    print('!!!!!!!!!!!!!!!!!!',cost)
                            elif datetime.combine(date(1,1,1), price.price_from) < datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,1), price.price_to) < datetime.combine(date(1,1,1), end_booking) and datetime.combine(date(1,1,1), price.price_to) > datetime.combine(date(1,1,1), start_booking):
                                if cost_cur_2 == 0:
                                    booking_duration = datetime.combine(date(1,1,1), price.price_to) - datetime.combine(date(1,1,1), start_booking)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_2 = price.value * booking_duration
                                    cost = cost + cost_cur_2
                                    cost = cost.quantize(Decimal("1"))
                                    print('?????????????????????',cost)
                            elif datetime.combine(date(1,1,1), price.price_from) > datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,1), price.price_to) > datetime.combine(date(1,1,1), end_booking) and datetime.combine(date(1,1,1), price.price_from) < datetime.combine(date(1,1,1), end_booking):
                                if cost_cur_3 == 0:
                                    booking_duration = datetime.combine(date(1,1,1), end_booking) - datetime.combine(date(1,1,1), price.price_from)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_3 = price.value * booking_duration
                                    cost = cost + cost_cur_3
                                    cost = cost.quantize(Decimal("1"))
                                    print('********************',cost)
                booking_form = BookingCreateForm(initial={'table': table, 'start': start, 'end': end, 'cost': cost})
                context = {}
                context['form'] = booking_form
                context['cost'] = cost
                context['start'] = start_form
                context['end'] = end_form
                context['table'] = table
                context['club'] = club
                return render(request, 'clubs/extranet/extranet_booking_create_form.html', context)

class BookingCreateView(FormView):
    """Display booking creation form."""
    def post(self, request, *args, **kwargs):
        form = BookingCreateForm(request.POST)
        if form.is_valid():
            booking = form.save()
            if self.request.is_ajax():
                data = {
                    'pk': booking.id,
                    'codeNumber': booking.code_number,
                }
                return JsonResponse(data)
            else:
                return HttpResponseRedirect(reverse('clubs:club_list'))
    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            if self.request.GET.get('hall'):
                city = City.objects.get(url=self.kwargs['city'])
                club = Club.objects.filter(city=city).get(slug=self.kwargs['club_slug'])
                hall = self.request.GET.get('hall')
                if Game.objects.filter(hall=hall).count() > 1:
                    game_set = Game.objects.filter(hall=hall)
                    context = {}
                    context['club'] = club
                    context['game_set'] = game_set
                    return render(request, 'clubs/booking/games.html', context)
                else:
                    game = Game.objects.get(hall=hall)
                    workingtime = club.working_times.all().first()
                    start = workingtime.opening_time
                    end = workingtime.closing_time
                    duration = workingtime.duration * 2
                    duration = range(duration)
                    steps = {}
                    time = None
                    for value in duration:
                        if time != None:
                            steps[value] = time.time
                            time = time + timedelta(minutes=30)
                        else:
                            steps[value] = start
                            time = datetime.combine(date(1,1,1), start) + timedelta(minutes=30)
                    context = {}
                    context['club'] = club
                    context['duration'] = duration
                    context['steps'] = steps
                    context['start'] = start
                    context['end'] = end
                    context['game'] = game.id
                    return render(request, 'clubs/booking/datetime.html', context)
            if self.request.GET.get('game'):
                city = City.objects.get(url=self.kwargs['city'])
                game = self.request.GET.get('game')
                club = Club.objects.filter(city=city).get(slug=self.kwargs['club_slug'])
                workingtime = club.working_times.all().first()
                start = workingtime.opening_time
                end = workingtime.closing_time
                duration = workingtime.duration * 2
                duration = range(duration)
                steps = {}
                time = None
                for value in duration:
                    if time != None:
                        steps[value] = time.time
                        time = time + timedelta(minutes=30)
                    else:
                        steps[value] = start
                        time = datetime.combine(date(1,1,1), start) + timedelta(minutes=30)
                context = {}
                context['club'] = club
                context['duration'] = duration
                context['steps'] = steps
                context['start'] = start
                context['end'] = end
                context['game'] = game
                return render(request, 'clubs/booking/datetime.html', context)
            if self.request.GET.get('day_of_the_week'):
                city = City.objects.get(url=self.kwargs['city'])
                day_of_the_week = self.request.GET.get('day_of_the_week')
                club = Club.objects.filter(city=city).get(slug=self.kwargs['club_slug'])
                workingtime = WorkingTime.objects.filter(club=club).get(name=day_of_the_week)
                start = workingtime.opening_time
                end = workingtime.closing_time
                duration = workingtime.duration * 2
                duration = range(duration)
                steps = {}
                time = None
                for value in duration:
                    if time != None:
                        steps[value] = time.time
                        time = time + timedelta(minutes=30)
                    else:
                        steps[value] = start
                        time = datetime.combine(date(1,1,1), start) + timedelta(minutes=30)
                context = {}
                context['day_of_the_week'] = day_of_the_week
                context['steps'] = steps
                context['workingtime'] = workingtime
                return render(request, 'clubs/booking/time.html', context)
            if self.request.GET.get('selected_game'):
                city = City.objects.get(url=self.kwargs['city'])
                club = Club.objects.filter(city=city).get(slug=self.kwargs['club_slug'])
                next_day = self.request.GET.get('next_day')
                next_day = int(next_day)
                start_date = self.request.GET.get('booking_date')
                end_date = datetime.strptime(start_date,'%Y-%m-%d') + timedelta(days=1)
                start_date = datetime.strptime(start_date,'%Y-%m-%d') + timedelta(days=next_day)
                start_time = self.request.GET.get('start_time')
                start_time = datetime.strptime(start_time, '%H:%M')
                end_time = self.request.GET.get('end_time')
                end_time = datetime.strptime(end_time, '%H:%M')
                game = self.request.GET.get('selected_game')
                start_datetime = datetime.combine(start_date.date(), start_time.time())
                if datetime.combine(date(1,1,1), start_time.time()) > datetime.combine(date(1,1,1), end_time.time()):
                    end_datetime = datetime.combine(end_date.date(), end_time.time())
                else:
                    end_datetime = datetime.combine(start_date.date(), end_time.time())
                    print('!!!!!!!!!!!!', start_datetime)
                    print('!!!!!!!!!!!!', end_datetime.time())
                # table_set = Table.objects.filter(game=game).exclude(booking__start__date=start_date.date(), booking__start__time__lt=end_time.time(), booking__end__time__gt=start_time.time())
                # if datetime.combine(date(1,1,1), start_time.time()) > datetime.combine(date(1,1,1), end_time.time()):
                #     table_set = Table.objects.filter(game=game).exclude(booking__in=Booking.objects.filter(start__date=start_date.date(), start__time__gt=end_time.time(), end__time__lt=start_time.time()))
                # else:
                table_set = Table.objects.filter(game=game).exclude(booking__in=Booking.objects.filter(start__date=start_date.date(), start__time__lt=end_time.time(), end__time__gt=start_time.time()))
                # table_set = Table.objects.filter(game=game).exclude(booking__in=Booking.objects.filter( Q(start__date=start_date.date(), start__time__lt=end_time.time(), end__time__gt=start_time.time()) | Q(start__date=start_date.date(), start__time__lt=end_time.time(), end__time__gt=start_time.time()) ))
                # table_set = Table.objects.filter(game=game).exclude(booking__in=Booking.objects.filter( Q(start__time__lt=end_datetime.time(), end__time__gt=end_datetime.time()) | Q(start__time__lt=start_datetime.time(), end__time__gt=start_datetime.time()) ))
                # table_set = Table.objects.filter(game=game).exclude(booking__start__date=start_date.date(), booking__start__time__range=(start_time.time(), end_time.time()), booking__end__time__range=(start_time.time(), end_time.time()))
                # table_set = Table.objects.filter(game=game).exclude(booking__start__date=start_date.date(), booking__start__time__range=start_time.time())
                # table_set = Table.objects.filter(game=game).exclude(booking__start__date=start_date.date()).exclude(booking__start__time__range=(start_time.time(), end_time.time()))
                start_date = self.request.GET.get('booking_date')
                next_day = self.request.GET.get('next_day')
                start_time = self.request.GET.get('start_time')
                end_time = self.request.GET.get('end_time')
                day_of_the_week = self.request.GET.get('week_day')
                context = {}
                context['table_set'] = table_set
                context['start_date'] = start_date
                context['next_day'] = next_day
                context['start_time'] = start_time
                context['end_time'] = end_time
                context['day_of_the_week'] = day_of_the_week
                return render(request, 'clubs/booking/tables.html', context)
            if self.request.GET.get('selected_table'):
                city = City.objects.get(url=self.kwargs['city'])
                club = Club.objects.filter(city=city).get(slug=self.kwargs['club_slug'])
                next_day = self.request.GET.get('next_day')
                next_day = int(next_day)
                start_date = self.request.GET.get('booking_date')
                start_date = datetime.strptime(start_date,'%Y-%m-%d') + timedelta(days=next_day)
                start_date = start_date.strftime('%Y-%m-%d')
                start_time = self.request.GET.get('start_time')
                end_time = self.request.GET.get('end_time')
                end_date = datetime.strptime(start_date,'%Y-%m-%d') + timedelta(days=1)
                end_date = end_date.date()
                end_date = end_date.strftime('%Y-%m-%d')
                start_booking = datetime.strptime(start_time,'%H:%M').time()
                end_booking = datetime.strptime(end_time,'%H:%M').time()
                if datetime.combine(date(1,1,1), start_booking) > datetime.combine(date(1,1,1), end_booking):
                    start = start_date + ' ' + start_time
                    end = end_date + ' ' + end_time
                else:
                    start = start_date + ' ' + start_time
                    end = start_date + ' ' + end_time
                start_form = datetime.strptime(start,'%Y-%m-%d %H:%M')
                end_form = datetime.strptime(end,'%Y-%m-%d %H:%M')
                table = self.request.GET.get('selected_table')
                table = Table.objects.get(pk=table)
                day_of_the_week = self.request.GET.get('week_day')
                workingtime = WorkingTime.objects.filter(club=club).get(name=day_of_the_week)
                prices = Price.objects.filter(tables=table).filter(working_times=workingtime)
                cost = 0
                cost_cur_1 = 0
                cost_cur_2 = 0
                cost_cur_3 = 0
                for price in prices:
                    print('3333333333333333333333')
                    if datetime.combine(date(1,1,1), start_booking) > datetime.combine(date(1,1,1), end_booking):
                        print('55555555555555555555555555555')
                        if datetime.combine(date(1,1,1), price.price_from) > datetime.combine(date(1,1,1), price.price_to):
                            if datetime.combine(date(1,1,1), price.price_from) <= datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,2), price.price_to) >= datetime.combine(date(1,1,2), end_booking):
                                if cost_cur_1 == 0:
                                    booking_duration = datetime.combine(date(1,1,2), end_booking) - datetime.combine(date(1,1,1), start_booking)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_1 = price.value * booking_duration
                                    cost = cost + cost_cur_1
                                    cost = cost.quantize(Decimal("1"))
                                    print('!!!!!!!!!!!!!!!!!!',cost)
                            elif datetime.combine(date(1,1,1), price.price_from) < datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,2), price.price_to) < datetime.combine(date(1,1,2), end_booking) and datetime.combine(date(1,1,2), price.price_to) > datetime.combine(date(1,1,1), start_booking):
                                if cost_cur_2 == 0:
                                    booking_duration = datetime.combine(date(1,1,2), price.price_to) - datetime.combine(date(1,1,1), start_booking)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_2 = price.value * booking_duration
                                    cost = cost + cost_cur_2
                                    cost = cost.quantize(Decimal("1"))
                                    print('?????????????????????',cost)
                            elif datetime.combine(date(1,1,1), price.price_from) > datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,2), price.price_to) > datetime.combine(date(1,1,2), end_booking) and datetime.combine(date(1,1,1), price.price_from) < datetime.combine(date(1,1,2), end_booking):
                                if cost_cur_3 == 0:
                                    booking_duration = datetime.combine(date(1,1,2), end_booking) - datetime.combine(date(1,1,1), price.price_from)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_3 = price.value * booking_duration
                                    cost = cost + cost_cur_3
                                    cost = cost.quantize(Decimal("1"))
                                    print('********************',cost)
                        else:
                            if datetime.combine(date(1,1,1), price.price_from) < datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,1), price.price_to) < datetime.combine(date(1,1,1), end_booking) and datetime.combine(date(1,1,1), price.price_to) > datetime.combine(date(1,1,1), start_booking):
                                if cost_cur_2 == 0:
                                    booking_duration = datetime.combine(date(1,1,1), price.price_to) - datetime.combine(date(1,1,1), start_booking)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_2 = price.value * booking_duration
                                    cost = cost + cost_cur_2
                                    cost = cost.quantize(Decimal("1"))
                                    print('?????????????????????',cost)
                            elif datetime.combine(date(1,1,1), price.price_from) > datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,1), price.price_to) > datetime.combine(date(1,1,1), end_booking) and datetime.combine(date(1,1,1), price.price_from) < datetime.combine(date(1,1,1), end_booking):
                                if cost_cur_3 == 0:
                                    booking_duration = datetime.combine(date(1,1,1), end_booking) - datetime.combine(date(1,1,1), price.price_from)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_3 = price.value * booking_duration
                                    cost = cost + cost_cur_3
                                    cost = cost.quantize(Decimal("1"))
                                    print('********************',cost)
                    else:
                        if datetime.combine(date(1,1,1), price.price_from) > datetime.combine(date(1,1,1), price.price_to):
                            if datetime.combine(date(1,1,1), price.price_from) > datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,1), price.price_to) >= datetime.combine(date(1,1,1), end_booking):
                                if cost_cur_1 == 0:
                                    booking_duration = datetime.combine(date(1,1,1), end_booking) - datetime.combine(date(1,1,1), start_booking)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_1 = price.value * booking_duration
                                    cost = cost + cost_cur_1
                                    cost = cost.quantize(Decimal("1"))
                                    print('!!!!!!!!!!!!!!!!!!',cost)
                            elif datetime.combine(date(1,1,1), price.price_from) > datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,1), price.price_to) < datetime.combine(date(1,1,1), end_booking) and datetime.combine(date(1,1,1), price.price_to) > datetime.combine(date(1,1,1), start_booking):
                                if cost_cur_2 == 0:
                                    booking_duration = datetime.combine(date(1,1,1), price.price_to) - datetime.combine(date(1,1,1), start_booking)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_2 = price.value * booking_duration
                                    cost = cost + cost_cur_2
                                    cost = cost.quantize(Decimal("1"))
                                    print('?????????????????????',cost)
                        else:
                            if datetime.combine(date(1,1,1), price.price_from) <= datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,1), price.price_to) >= datetime.combine(date(1,1,1), end_booking):
                                if cost_cur_1 == 0:
                                    booking_duration = datetime.combine(date(1,1,1), end_booking) - datetime.combine(date(1,1,1), start_booking)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_1 = price.value * booking_duration
                                    cost = cost + cost_cur_1
                                    cost = cost.quantize(Decimal("1"))
                                    print('!!!!!!!!!!!!!!!!!!',cost)
                            elif datetime.combine(date(1,1,1), price.price_from) < datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,1), price.price_to) < datetime.combine(date(1,1,1), end_booking) and datetime.combine(date(1,1,1), price.price_to) > datetime.combine(date(1,1,1), start_booking):
                                if cost_cur_2 == 0:
                                    booking_duration = datetime.combine(date(1,1,1), price.price_to) - datetime.combine(date(1,1,1), start_booking)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_2 = price.value * booking_duration
                                    cost = cost + cost_cur_2
                                    cost = cost.quantize(Decimal("1"))
                                    print('?????????????????????',cost)
                            elif datetime.combine(date(1,1,1), price.price_from) > datetime.combine(date(1,1,1), start_booking) and datetime.combine(date(1,1,1), price.price_to) > datetime.combine(date(1,1,1), end_booking) and datetime.combine(date(1,1,1), price.price_from) < datetime.combine(date(1,1,1), end_booking):
                                if cost_cur_3 == 0:
                                    booking_duration = datetime.combine(date(1,1,1), end_booking) - datetime.combine(date(1,1,1), price.price_from)
                                    booking_duration = booking_duration.seconds / 3600
                                    booking_duration = Decimal(booking_duration)
                                    cost_cur_3 = price.value * booking_duration
                                    cost = cost + cost_cur_3
                                    cost = cost.quantize(Decimal("1"))
                                    print('********************',cost)
                booking_form = BookingCreateForm(initial={'table': table, 'start': start, 'end': end, 'cost': cost})
                context = {}
                context['form'] = booking_form
                context['cost'] = cost
                context['start'] = start_form
                context['end'] = end_form
                context['table'] = table
                context['club'] = Club.objects.filter(city=city).get(slug=self.kwargs['club_slug'])
                return render(request, 'clubs/booking/booking_create_form.html', context)
        else:
            city = City.objects.get(url=self.kwargs['city'])
            club = Club.objects.filter(city=city).get(slug=self.kwargs['club_slug'])
            if Hall.objects.filter(club=club).count() > 1:
                hall_set = Hall.objects.filter(club=club)
                context = {}
                context['club'] = club
                context['hall_set'] = hall_set
                context['city'] = city
                return render(request, 'clubs/booking/halls.html', context)
            else:
                hall = Hall.objects.get(club=club)
                if Game.objects.filter(hall=hall).count() > 1:
                    game_set = Game.objects.filter(hall=hall)
                    context = {}
                    context['club'] = Club.objects.filter(city=city).get(slug=self.kwargs['club_slug'])
                    context['game_set'] = game_set
                    return render(request, 'clubs/booking/games_alt.html', context)
                else:
                    game = Game.objects.get(hall=hall)
                    workingtime = club.working_times.all().first()
                    start = workingtime.opening_time
                    end = workingtime.closing_time
                    duration = workingtime.duration * 2
                    duration = range(duration)
                    steps = {}
                    time = None
                    for value in duration:
                        if time != None:
                            steps[value] = time.time
                            time = time + timedelta(minutes=30)
                        else:
                            steps[value] = start
                            time = datetime.combine(date(1,1,1), start) + timedelta(minutes=30)
                    context = {}
                    context['club'] = club
                    context['duration'] = duration
                    context['steps'] = steps
                    context['start'] = start
                    context['end'] = end
                    context['game'] = game.id
                    return render(request, 'clubs/booking/datetime_alt.html', context)

class ExtranetIndexView(LoginRequiredMixin, TemplateView):
    """Display the partner's extranet."""
    template_name = 'clubs/extranet/index.html'

class ExtranetCalendarView(LoginRequiredMixin, TemplateView):
    """Display the partner's extranet."""
    template_name = 'clubs/extranet/calendar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = self.request.user.club_set.all().first()
        tables = Table.objects.filter(club=club)
        table = Table.objects.filter(club=club).first()
        bookings = Booking.objects.filter(table=table)
        context['club'] = club
        context['tables'] = tables
        context['table_id'] = table
        context['bookings'] = bookings
        return context

class ExtranetCalendarTableView(LoginRequiredMixin, TemplateView):
    template_name = 'clubs/extranet/calendar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = self.request.user.club_set.all().first()
        tables = Table.objects.filter(club=club)
        table = Table.objects.get(pk=self.kwargs['table_id'])
        bookings = Booking.objects.filter(table=table)
        context['club'] = club
        context['tables'] = tables
        context['table_id'] = table
        context['bookings'] = bookings
        return context

class ExtranetClubView(LoginRequiredMixin, TemplateView):
    """Display the partner's extranet."""
    template_name = 'clubs/extranet/club.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = self.request.user.club_set.all().first()
        prices = club.prices.all()
        if prices.exists():
            values = []
            for price in prices:
                values.append(price.value)
            price_min = min(values)
            price_max = max(values)
            price_min = price_min.quantize(Decimal('1'))
            price_max = price_max.quantize(Decimal('1'))
            context['price_min'] = price_min
            context['price_max'] = price_max
        workingtimes = club.working_times.all()
        days = {}
        opening_time = None
        closing_time = None
        name = None
        name_plus = None
        days_trans = {
            'MO': 'Пн',
            'TU': 'Вт',
            'WE': 'Ср',
            'TH': 'Чт',
            'FR': 'Пт',
            'SA': 'Сб',
            'SU': 'Вс',
        }
        for workingtime in workingtimes:
            if opening_time and closing_time:
                name_new = workingtime.name
                for key, value in days_trans.items():
                    if key == name_new:
                        name_new = value
                opening_time_new = workingtime.opening_time.strftime('%H:%M')
                closing_time_new = workingtime.closing_time.strftime('%H:%M')
                if opening_time == opening_time_new and closing_time == closing_time_new:
                    days.pop(name, None)
                    days[name +'-'+ name_new] = opening_time + ' – ' + closing_time
                else:
                    opening_time = opening_time_new
                    closing_time = closing_time_new
                    name = name_new
                    days[name_new] = opening_time + ' – ' + closing_time

            else:
                name = workingtime.name
                for key, value in days_trans.items():
                    if key == name:
                        name = value
                # if not workingtime.day_off:
                opening_time = workingtime.opening_time.strftime('%H:%M')
                closing_time = workingtime.closing_time.strftime('%H:%M')
                days[name] = opening_time + ' – ' + closing_time
                # else:
                #     days[name] = 'Выходной'

        days_key = None
        days_value = None
        for key, value in list(days.items()):
            if days_value == value:
                days.pop(days_key, None)
            days_value = value
            days_key = key
        context['days'] = days
        return context

class WorkingTimeView(LoginRequiredMixin, AjaxableResponseMixin, TemplateView):
    """Display the partner's extranet."""
    template_name = 'clubs/extranet/club/working_time_view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = Club.objects.get(pk=self.kwargs['club_id'])
        context['club'] = club
        return context

class WorkingTimeCreateView(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    """Display the club's working time creating form."""
    model = WorkingTime
    form_class = WorkingTimeForm
    template_name = 'clubs/extranet/club/working_time_create_form.html'
    context_object_name = 'working_time'
    success_url = '/'
    def form_valid(self, form):
        form.instance.club = Club.objects.get(pk=self.kwargs['club_id'])
        form.instance.name = self.kwargs['day']
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = Club.objects.get(pk=self.kwargs['club_id'])
        day = self.kwargs['day']
        context['club'] = club
        context['day'] = day
        return context

class WorkingTimeUpdateView(LoginRequiredMixin, AjaxableResponseMixin, UpdateView):
    """Display the hall updating form."""
    model = WorkingTime
    form_class = WorkingTimeForm
    template_name = 'clubs/extranet/club/working_time_update_form.html'
    success_url = '/'

class EquipmentView(LoginRequiredMixin, AjaxableResponseMixin, TemplateView):
    """Display the partner's extranet."""
    template_name = 'clubs/extranet/club/equipment.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = Club.objects.get(pk=self.kwargs['club_id'])
        context['club'] = club
        return context

class HallCreateView(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    """Display the club's hall creating form."""
    model = Hall
    form_class = HallForm
    template_name = 'clubs/extranet/club/hall_create_form.html'
    context_object_name = 'hall'
    success_url = '/'
    def form_valid(self, form):
        form.instance.club = Club.objects.get(pk=self.kwargs['club_id'])
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = Club.objects.get(pk=self.kwargs['club_id'])
        context['club'] = club
        return context

class HallUpdateView(LoginRequiredMixin, AjaxableResponseMixin, UpdateView):
    """Display the hall updating form."""
    model = Hall
    form_class = HallForm
    template_name = 'clubs/extranet/club/hall_update_form.html'
    success_url = '/'

class HallDeleteView(LoginRequiredMixin, AjaxableResponseMixin, DeleteView):
    """Display the hall delete form."""
    model = Hall
    template_name = 'clubs/extranet/club/hall_confirm_delete.html'
    success_url = '/partner/'

class GameCreateView(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    """Display the club's hall creating form."""
    model = Game
    form_class = GameForm
    template_name = 'clubs/extranet/club/game_create_form.html'
    context_object_name = 'game'
    success_url = '/'
    def form_valid(self, form):
        form.instance.hall = Hall.objects.get(pk=self.kwargs['hall_id'])
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hall = Hall.objects.get(pk=self.kwargs['hall_id'])
        context['hall'] = hall
        return context

class GameUpdateView(LoginRequiredMixin, AjaxableResponseMixin, UpdateView):
    """Display the hall updating form."""
    model = Game
    form_class = GameForm
    context_object_name = 'game'
    template_name = 'clubs/extranet/club/game_update_form.html'
    success_url = '/'

class GameDeleteView(LoginRequiredMixin, AjaxableResponseMixin, DeleteView):
    """Display the hall delete form."""
    model = Game
    template_name = 'clubs/extranet/club/game_confirm_delete.html'
    success_url = '/partner/'

class TableCreateView(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    """Display the club's hall creating form."""
    model = Table
    form_class = TableForm
    template_name = 'clubs/extranet/club/table_create_form.html'
    success_url = '/'
    def form_valid(self, form):
        form.instance.game = Game.objects.get(pk=self.kwargs['game_id'])
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = Game.objects.get(pk=self.kwargs['game_id'])
        context['game'] = game
        return context

class TableUpdateView(LoginRequiredMixin, AjaxableResponseMixin, UpdateView):
    """Display the hall updating form."""
    model = Table
    form_class = TableForm
    template_name = 'clubs/extranet/club/table_update_form.html'
    success_url = '/'

class TableDeleteView(LoginRequiredMixin, AjaxableResponseMixin, DeleteView):
    """Display the hall delete form."""
    model = Table
    template_name = 'clubs/extranet/club/table_confirm_delete.html'
    success_url = '/partner/'

class PriceCreateView(LoginRequiredMixin, FormView):
    """Display the club's table form."""
    def post(self, request, *args, **kwargs):
        form = PriceForm(request.POST)
        if form.is_valid():
            price = form.save()
            if self.request.is_ajax():
                context = {}
                club = Club.objects.get(pk=self.kwargs['club_id'])
                context['price'] = price
                context['club'] = club
                return render(request, 'clubs/extranet/club/price_create_form.html', context)
            else:
                return HttpResponseRedirect(reverse('clubs:equipment_table'))
    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            club = Club.objects.get(pk=self.kwargs['club_id'])
            data = {}
            data['club'] = club
            form = PriceForm(initial=data)
            context = {}
            context['club'] = club
            context['form'] = form
            return render(request, 'clubs/extranet/club/price_create_form.html', context)

class PriceUpdateView(LoginRequiredMixin, AjaxableResponseMixin, UpdateView):
    """Display the hall updating form."""
    model = Price
    form_class = PriceForm
    template_name = 'clubs/extranet/club/price_update_form.html'
    success_url = '/'

class PriceDeleteView(LoginRequiredMixin, AjaxableResponseMixin, DeleteView):
    """Display the hall delete form."""
    model = Price
    template_name = 'clubs/extranet/club/price_confirm_delete.html'
    success_url = '/partner/'

class PriceView(LoginRequiredMixin, AjaxableResponseMixin, TemplateView):
    """Display the partner's extranet."""
    template_name = 'clubs/extranet/club/price_view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = Club.objects.get(pk=self.kwargs['club_id'])
        prices = Price.objects.filter(club=club)
        context['club'] = club
        context['prices'] = prices
        return context

class PhotoView(LoginRequiredMixin, AjaxableResponseMixin, TemplateView):
    """Display the partner's extranet."""
    template_name = 'clubs/extranet/club/photo_view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = Club.objects.get(pk=self.kwargs['club_id'])
        context['club'] = club
        return context

class PhotoCreateView(LoginRequiredMixin, FormView):
    def post(self, request, *args, **kwargs):
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            if self.request.is_ajax():
                context = {}
                club = Club.objects.get(pk=self.kwargs['club_id'])
                context['club'] = club
                return render(request, 'clubs/extranet/club/photo_create_form.html', context)
    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            club = Club.objects.get(pk=self.kwargs['club_id'])
            data = {}
            data['club'] = club
            form = PhotoForm(initial=data)
            context = {}
            context['club'] = club
            context['form'] = form
            return render(request, 'clubs/extranet/club/photo_create_form.html', context)

class PhotoUpdateView(LoginRequiredMixin, AjaxableResponseMixin, UpdateView):
    """Display the hall updating form."""
    model = Photo
    form_class = PhotoForm
    template_name = 'clubs/extranet/club/photo_update_form.html'
    success_url = '/'

class PhotoDeleteView(LoginRequiredMixin, AjaxableResponseMixin, DeleteView):
    """Display the hall delete form."""
    model = Photo
    template_name = 'clubs/extranet/club/photo_confirm_delete.html'
    success_url = '/partner/'

class ExtranetBookingsView(LoginRequiredMixin, TemplateView):
    """Display the partner's extranet."""
    template_name = 'clubs/extranet/bookings.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = self.request.user.club_set.all().first()
        bookings = Booking.objects.filter(club=club)
        # costs = {}
        # for booking in bookings:
        #     costs
        context['bookings'] = bookings
        return context

# class UserView(LoginRequiredMixin, TemplateView):
#     """Display the user's account page."""
#     template_name = 'clubs/base_partner_index.html'

class ClubSearchListView(ListView):
    """Display a club list page filtered by the search query."""
    # model = Club
    template_name = 'clubs/search_result_list.html'
    context_object_name = 'search_result_list'
    def get_queryset(self):
        city = self.request.GET.get('city')
        clubs = Club.objects.filter(city=city)
        search_query = self.request.GET.get('q')
        if search_query:
            vector = SearchVector('name')
            query = SearchQuery(search_query)
            clubs = clubs.annotate(search=vector).filter(search=query)
            clubs = clubs.annotate(rank=SearchRank(vector, query)).order_by('-rank')
        return clubs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.request.GET.get('city')
        city = City.objects.get(pk=city)
        context['city'] = city
        return context

# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# import re
# import base64
#
# @csrf_exempt
# def club_scheme(request):
#     club_scheme_data_url = request.POST.get('clubScheme')
#     pattern = r'^data:(?P<mime_type>[^;]+);base64,(?P<image>.+)$'
#     result = re.match(pattern, club_scheme_data_url)
#     if result:
#         mime_type = result.group('mime_type')
#         image = result.group('image')
#         image = base64.b64decode(image)
#         club_scheme = open('clubs/static/clubs/images/club_scheme.png', 'wb')
#         club_scheme.write(image)
#         club_scheme.close()
#     # print(image)
#     # return render(request, 'clubs/partner.html')
#     return JsonResponse({'foo': 'bar'})

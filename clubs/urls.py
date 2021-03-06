from django.urls import path

from . import views

app_name = 'clubs'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<str:city>/clubs/', views.ClubListView.as_view(), name='club_list'),
    path('<str:city>/clubs/<slug:club_slug>/', views.ClubDetailView.as_view(), name='club_detail'),
    path('join/', views.ClubCreateView.as_view(), name='club_create'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('<str:city>/clubs/<slug:club_slug>/booking/', views.BookingCreateView.as_view(), name='booking_create'),
    path('partner/<int:pk>/booking/', views.ExtranetBookingCreateView.as_view(), name='extranet_booking_create'),
    path('partner/booking/<int:pk>/', views.ExtranetBookingUpdateView.as_view(), name='extranet_booking_update'),
    path('search/', views.ClubSearchListView.as_view(), name='search'),
    path('partner/', views.ExtranetIndexView.as_view(), name='partner'),
    path('partner/calendar/', views.ExtranetCalendarView.as_view(), name='partner_calendar'),
    path('partner/calendar/<int:table_id>/', views.ExtranetCalendarTableView.as_view(), name='partner_calendar_table'),
    path('partner/bookings/', views.ExtranetBookingsView.as_view(), name='partner_bookings'),
    path('partner/club/', views.ExtranetClubView.as_view(), name='partner_club'),
    path('partner/club/<int:pk>/', views.ClubUpdateView.as_view(), name='club_update'),
    path('partner/club/<int:club_id>/working-time/', views.WorkingTimeView.as_view(), name='working_time'),
    path('partner/club/<int:club_id>/working-time/<str:day>/create/', views.WorkingTimeCreateView.as_view(), name='working_time_create'),
    path('partner/club/working-time/<int:pk>/update/', views.WorkingTimeUpdateView.as_view(), name='working_time_update'),
    path('partner/club/<int:club_id>/hall/', views.EquipmentView.as_view(), name='equipment'),
    path('partner/club/<int:club_id>/hall/create/', views.HallCreateView.as_view(), name='hall_create'),
    path('partner/club/hall/<int:pk>/update/', views.HallUpdateView.as_view(), name='hall_update'),
    path('partner/club/hall/<int:pk>/delete/', views.HallDeleteView.as_view(), name='hall_delete'),
    path('partner/club/hall/<int:hall_id>/game/create/', views.GameCreateView.as_view(), name='game_create'),
    path('partner/club/hall/game/<int:pk>/update/', views.GameUpdateView.as_view(), name='game_update'),
    path('partner/club/hall/game/<int:pk>/delete/', views.GameDeleteView.as_view(), name='game_delete'),
    path('partner/club/hall/game/<int:game_id>/table/create/', views.TableCreateView.as_view(), name='table_create'),
    path('partner/club/hall/game/table/<int:pk>/update/', views.TableUpdateView.as_view(), name='table_update'),
    path('partner/club/hall/game/table/<int:pk>/delete/', views.TableDeleteView.as_view(), name='table_delete'),
    path('partner/club/<int:club_id>/price/', views.PriceView.as_view(), name='price'),
    path('partner/club/<int:club_id>/price/create/', views.PriceCreateView.as_view(), name='price_create'),
    path('partner/club/price/<int:pk>/update/', views.PriceUpdateView.as_view(), name='price_update'),
    path('partner/club/price/<int:pk>/delete/', views.PriceDeleteView.as_view(), name='price_delete'),
    path('partner/club/<int:club_id>/photo/', views.PhotoView.as_view(), name='photo_view'),
    path('partner/club/<int:club_id>/photo/create/', views.PhotoCreateView.as_view(), name='photo_create'),
    path('partner/club/photo/<int:pk>/update/', views.PhotoUpdateView.as_view(), name='photo_update'),
    path('partner/club/photo/<int:pk>/delete/', views.PhotoDeleteView.as_view(), name='photo_delete'),
    # path('partner/club/', views.ClubUpdateView.as_view(), name='partner_club'),
    # path('<str:city>/', views.RedirectView.as_view(url='/')),
    # path('login/', views.UserView.as_view(), name='user'),
    # path('club-scheme/', views.club_scheme, name='club_scheme'),
]

from django.urls import path
from .views import RoomListView, BookingList, BookingView, RoomDetailView

app_name = 'Hotel'

urlpatterns = [
    path('', RoomListView.as_view(), name='index'),
    path('roomList/', RoomListView.as_view(), name = 'RoomList'),
    path('bookingList/', BookingList.as_view(), name = 'BookingList'),
    path('book/', BookingView.as_view() , name = 'booking_view'),
    path('room/<str:category>/', RoomDetailView.as_view(), name='RoomDetailView'),
]
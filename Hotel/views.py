from unicodedata import category
from urllib import request as urllib_request  # Rename the import to avoid conflicts
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView, View
from .models import Room, Booking
from .forms import AvailabilityForm
from Hotel.Booking_Functions.availablity import check_availablity
from datetime import datetime
from django.urls import reverse

# Create your views here.

class RoomListView(ListView):
    model = Room
    template_name = 'room_list_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rooms = Room.objects.all()
        room_list = []

        for room in rooms:
            room_category = room.get_categories_display()
            room_url = reverse('Hotel:RoomDetailView', kwargs={'category': room.categories})
            room_list.append((room_category, room_url))

        context['room_list'] = room_list
        return context

class BookingList(ListView):
    model = Booking
    template_name = 'booking_list.html'
    
class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)  # Update 'room_categories' to 'category'
        room_list = Room.objects.filter(categories=category)
        room_category = dict(Room.room_categories).get(category, None)
        if len(room_list) > 0:
            context = {
                'room_category': room_category
            }
            return render(request, 'room_detail_view.html', context)
        else:
            return HttpResponse('Category does not exist!')
    
    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)  # Retrieve the category from URL
        room_list = Room.objects.filter(categories=category)
        data = request.POST  # Retrieve POST data

        if 'Check_In_Time' in data and 'Check_Out_Time' in data:
            check_in_time = datetime.strptime(data['Check_In_Time'], '%Y-%m-%dT%H:%M')
            check_out_time = datetime.strptime(data['Check_Out_Time'], '%Y-%m-%dT%H:%M')

            if check_availablity(room_list, check_in_time, check_out_time):
                room = room_list[0]
                booking = Booking.objects.create(
                    user=request.user,
                    room=room,
                    Check_In_Time=check_in_time,
                    Check_Out_Time=check_out_time
                )
                booking.save()
                return HttpResponse('Booking successful!')
            else:
                return HttpResponse('This category of Rooms is Booked!')
        else:
            return HttpResponse('Invalid form data. Please provide Check_In_Time and Check_Out_Time.')


        
class BookingView(FormView):
    form_class = AvailabilityForm
    template_name = 'availability_form.html'
    
    def form_valid(self, form):
        data = form.cleaned_data
        room_list = Room.objects.filter(categories=data['room_category'])
        avail_rooms_list = []
        
        for room in room_list:
            if check_availablity(room, data['Check_In_Time'], data['Check_Out_Time']):
                avail_rooms_list.append(room)

        if len(avail_rooms_list) > 0:
            room = avail_rooms_list[0]
            booking = Booking.objects.create(
                user = self.request.user,
                room = room,
                Check_In_Time = data['Check_In_Time'],
                Check_Out_Time = data['Check_Out_Time']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('This category of Rooms is Booked!')
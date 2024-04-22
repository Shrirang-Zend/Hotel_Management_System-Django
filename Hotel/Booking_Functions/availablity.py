from django.utils import timezone
from Hotel.models import Booking

def check_availablity(rooms, check_in_time, check_out_time):
    check_in_time = timezone.make_aware(check_in_time)
    check_out_time = timezone.make_aware(check_out_time)

    for room in rooms:
        bookings = Booking.objects.filter(room=room)
        for booking in bookings:
            booking_check_in_time = timezone.localtime(booking.Check_In_Time)
            booking_check_out_time = timezone.localtime(booking.Check_Out_Time)

            if booking_check_in_time > check_out_time or booking_check_out_time < check_in_time:
                continue
            else:
                return False
    return True
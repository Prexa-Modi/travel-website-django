# Register your models here.
from django.contrib import admin
from .models import Duration, category, State, city, Offer, Trip, available_dates, Hotel, tourpackage,contact,About,review, gallery,signupdata,passenger,Payment,Itinerary,Destination,Booking
# Register your models here.
from django.db import models
from django.forms import ModelChoiceField
class showDuration(admin.ModelAdmin):
   list_display = ['name', 'days', 'nights']


admin.site.register(Duration, showDuration)


class showsignupdata(admin.ModelAdmin):
   list_display = ["name", "email", "password","is_admin"]

admin.site.register(signupdata, showsignupdata)

class showcategory(admin.ModelAdmin):
   list_display = ['name']


admin.site.register(category, showcategory)

class showgallery(admin.ModelAdmin):
   list_display = ['gallery_photo',"name"]

admin.site.register(gallery,showgallery)


class showstate(admin.ModelAdmin):
   list_display = ['id', 'name']


admin.site.register(State, showstate)


class showcity(admin.ModelAdmin):
   list_display = ['id', 'name', 'state']


admin.site.register(city, showcity)


@admin.register(Offer)
class showOffer(admin.ModelAdmin):
   list_display = ['name', 'discount_percentage', 'start_date', 'end_date','status','cat']





class showpackage(admin.ModelAdmin):
   list_display = ['name', 'description', 'state','package_photo','top_des']


admin.site.register(tourpackage, showpackage)

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
   list_display = ['name', 'tour_package', 'price', 'duration', 'category','transport_mode','trip_photo','trip_video','offers']


@admin.register(available_dates)
class showavailabledates(admin.ModelAdmin):
   list_display = ['trip', 'date', 'available_slots']
   list_filter = ['trip',]


'''class showdestination(admin.ModelAdmin):
   list_display = ['trip','city','duration']
admin.site.register(Destination,showdestination)
'''


class CustomTripChoiceField(ModelChoiceField):
   def label_from_instance(self, obj):
      return f"{obj.name} ({obj.duration.days} days)"


class DestinationAdmin(admin.ModelAdmin):
   def formfield_for_foreignkey(self, db_field, request, **kwargs):
      if db_field.name == "trip":
         kwargs["queryset"] = Trip.objects.all().annotate(duration_days=models.F('duration__days'))
         kwargs["form_class"] = CustomTripChoiceField
      return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Destination, DestinationAdmin)



class HotelAdmin(admin.ModelAdmin):
   list_display = ['name', 'description','rating','city']
admin.site.register(Hotel, HotelAdmin)





class showpassenger(admin.ModelAdmin):
   list_display = ['customer', 'age', 'gender', 'first_name','last_name','aadhar_number']


admin.site.register(passenger, showpassenger)

class showpayment(admin.ModelAdmin):
   list_display = ['user', 'amount', 'payment_date','card_number','card_holder_name','expiration_date','cvv']


admin.site.register(Payment, showpayment)


@admin.register(Itinerary)
class showItinerary(admin.ModelAdmin):
   list_display = [
   'trip', 'day_number', 'activities', 'destination']  # Add other fields you want to display in the list view
   list_filter = ['trip', 'day_number',]


@admin.register(Booking)
class showbooking(admin.ModelAdmin):
   list_display = ['user','booking_date','num_passengers','is_payment_done','trip', 'dateb','status']


class showcontact(admin.ModelAdmin):
   list_display = ['firstname', 'lastname', 'email','phone','message']

admin.site.register(contact,showcontact)


class showabout(admin.ModelAdmin):
   list_display = ['subtitle','title','description']

admin.site.register(About,showabout)


class showreview(admin.ModelAdmin):
   lsit_display = ["trip","name","email","comment","rating"]

admin.site.register(review, showreview)














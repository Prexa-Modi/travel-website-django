# Create your models here.
from django.db import models
from django.utils.safestring import mark_safe
from django.core.validators import MaxValueValidator
# Create your models here.
class Duration(models.Model):
    name = models.CharField(max_length=100)
    days = models.PositiveIntegerField()
    nights = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Manage Category'
        verbose_name_plural='Manage Category'

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class city(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Offer(models.Model):
    name = models.CharField(max_length=255)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.BooleanField(default=False)
    cat = models.ForeignKey(category,on_delete=models.CASCADE,verbose_name='category')

    def __str__(self):
        return self.name




class tourpackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    state = models.ForeignKey(State, on_delete=models.CASCADE,null=True)
    pimage = models.ImageField(upload_to="photos")
    top_des=models.BooleanField(verbose_name="Top Destination",default=0)
    #video = models.FileField(upload_to="pphoto")
    # Add other fields as needed for your Package model

    def __str__(self):
        return self.name


    class Meta:
        verbose_name='Manage Tour Packages'
        verbose_name_plural='Manage Tour Packages'

    def package_photo(self):
               return mark_safe('<img src="{}" width="100"/>'.format(self.pimage.url))


    package_photo.allow_tags = True





'''
class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    imagesh= models.ImageField(upload_to="photos")
    is_partner=models.BooleanField(verbose_name='partner')

    def __str__(self):
        return self.name
    def admin_photo(self):
               return mark_safe('<img src="{}" width="100"/>'.format(self.imagesh.url))


    admin_photo.allow_tags = True
'''

class Trip(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tour_package=models.ForeignKey(tourpackage,verbose_name='package',on_delete=models.CASCADE)
    duration = models.ForeignKey('Duration', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    offers = models.ForeignKey('Offer', on_delete=models.CASCADE, null=True, blank=True)
    TRANSPORT_MODE_CHOICES = [
        ('bus', 'Bus'),
        ('train', 'Train'),
        ('flight', 'Flight'),
    ]
    transport_mode = models.CharField(max_length=10, choices=TRANSPORT_MODE_CHOICES)
    tripimage = models.ImageField(upload_to="photos",default=0)

    video = models.FileField(upload_to="photos",default=0)
    # Add other fields as needed for your Package model

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Manage Trip'
        verbose_name_plural = 'Manage Trip'

    def trip_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.tripimage.url))

    trip_photo.allow_tags = True

    def trip_video(self):
        return mark_safe('<video width="500" height="300" controls><source src="{}" type="video/mp4"></video>'.format(self.video.url))


class available_dates(models.Model):
    trip=models.ForeignKey('Trip',on_delete=models.CASCADE)
    date=models.DateField()
    available_slots=models.IntegerField()

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')


class gallery(models.Model):
    gimage = models.ImageField(upload_to='photos')
    name = models.CharField(max_length=30)


    def gallery_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.gimage.url))

    gallery_photo.allow_tags = True


class signupdata(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)
    is_admin=models.BooleanField(default=False)

    def __str__(self):
        return self.name

class passenger(models.Model):
    customer = models.ForeignKey(signupdata, on_delete=models.CASCADE)
    #booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=15)
    aadhar_number = models.PositiveIntegerField(max_length=12)
    has_booked = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        verbose_name='Manage Passenger'
        verbose_name_plural='Manage Passenger'


class Payment(models.Model):
    user = models.ForeignKey(signupdata, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    #bill_url=models.CharField(max_length=30)
    #bill = models.FileField(upload_to='bills', null=True, blank=True)  # FileField to store the uploaded bill file
    card_number = models.PositiveIntegerField()
    card_holder_name = models.CharField(max_length=25)
    expiration_date = models.DateField()
    cvv = models.PositiveIntegerField(max_length=3)


class Itinerary(models.Model):
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE, related_name='itineraries')
    day_number = models.PositiveIntegerField()
    destination=models.ForeignKey('Destination',on_delete=models.CASCADE)
    activities=models.TextField()

    def __str__(self):
     return f"{self.trip.name}"


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(limit_value=5)])
    city= models.ForeignKey(city,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"



class Destination(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    city = models.ForeignKey(city, on_delete=models.CASCADE)
    duration = models.IntegerField()
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE)
    def __str__(self):
        #return f"{self.city.name} ({self.duration} days)  {self.hotel.name}"
        #return f"{self.city.name}\nHotel Name: {self.hotel.name}"
        return f"{self.city.name}\nHotel Name: {self.hotel.name}\nRating : {self.hotel.rating}"

class Booking(models.Model):
    user = models.ForeignKey(signupdata, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    num_passengers = models.PositiveIntegerField(default=0)
    is_payment_done = models.BooleanField(default=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    dateb=models.ForeignKey(available_dates,on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    def __str__(self):
        return f"{self.user}"






class contact(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(null=True)
    phone = models.IntegerField()
    message = models.TextField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class About(models.Model):
    subtitle = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class review(models.Model):
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE, related_name='review')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    comment = models.TextField()
    RATING_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars')
    )
    rating = models.IntegerField(choices=RATING_CHOICES,null=True,blank=True)


    def __str__(self):
        return f"{self.name} ({self.email})"













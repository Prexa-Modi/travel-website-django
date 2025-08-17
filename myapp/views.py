from .models import category, Duration, State, city, Offer, available_dates, Trip, gallery, Booking, Hotel, tourpackage, About, contact, signupdata, passenger, Itinerary, Payment,Destination,review
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date, datetime
import random
from django.utils import timezone
import math
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime
from django.db.models import Count

from django.db.models import Avg

from django.http import JsonResponse



# Create your views here.

def dashboard(request):
    signupdatad = signupdata.objects.filter(is_admin=True)
    context = {
        'admindata': signupdatad
    }
    return render(request, "dashboard.html",context)


def showcategory(request):
    categorydata = category.objects.all()
    context = {"data": categorydata}
    return render(request, "main-category.html", context)


def aboutpage(request):
    return render(request, 'about.html')


def destinationtrip(request):
    getdesdata = Trip.objects.all()

    # Round down the price to the nearest whole number
    for trip in getdesdata:
        trip.price = int(trip.price)

    context = {
        'getdesdata': getdesdata
    }
    return render(request, 'destination.html', context)


def filtercat(request, id):
    # If a category ID is provided, filter based on the provided ID
    if id:
        filtered_data = category.objects.filter(id=id)
    else:
        # If no category ID is provided, return all categories
        filtered_data = category.objects.all()

    # Pass filtered_data to the template
    context = {
        'data': filtered_data
    }
    return render(request, 'main-category.html', context)


def fetchcatdata(request):
    name = request.POST.get("cname")

    insertdata = category(name=name)
    insertdata.save()

    return HttpResponseRedirect("/category")
    # return render(request,template_name="main-category.html")


def updatecat(request, id):
    name = request.POST.get("cname")
    updatedata = category(id=id, name=name)
    updatedata.save()
    return HttpResponseRedirect("/category")


def deletecat(request, id):
    deldata = category.objects.filter(id=id)
    deldata.delete()

    return HttpResponseRedirect("/category")


def showDuration(request):
    ddata = Duration.objects.all()
    context = {"durationdata": ddata}
    return render(request, "duration.html", context)


def fetchdurationdata(request):
    name = request.POST.get("dname")
    days = request.POST.get("days")
    nights = request.POST.get("nights")

    insertduration = Duration(name=name, days=days, nights=nights)
    insertduration.save()
    return HttpResponseRedirect("/Duration")


def updateduration(request, id):
    name = request.POST.get("dname")
    days = request.POST.get("days")
    nights = request.POST.get("nights")
    updatedata = Duration(id=id, name=name, days=days, nights=nights)
    updatedata.save()
    return HttpResponseRedirect("/Duration")


def deleteduration(request, id):
    delduration = Duration.objects.filter(id=id)
    delduration.delete()

    return HttpResponseRedirect("/Duration")


def statepage(request):
    getstatedata = State.objects.all()
    context = {
        "statedata": getstatedata
    }
    return render(request, "State.html", context)


def fetchstatedata(request):
    name = request.POST.get("sname")
    insertdata = State(name=name)
    insertdata.save()
    return redirect("/stateurl")


def updatestate(request, id):
    name = request.POST.get("sname")
    updatedata = State(id=id, name=name)
    updatedata.save()
    return redirect("/stateurl")


def deletestate(request, id):
    deletedata = State.objects.filter(id=id)
    deletedata.delete()

    return redirect("/stateurl")


def citypage(request):
    getcitydata = city.objects.all()
    getstatedata = State.objects.all()
    context = {
        "statedata": getstatedata,
        "citydata": getcitydata
    }
    return render(request, "City.html", context)


def fetchcitydata(request):
    name = request.POST.get("cname")
    stateid = request.POST.get("selectedstate")

    insertcity = city(name=name, state=State(id=stateid))
    insertcity.save()

    return redirect("/cityurl")


def couponpage(request):
    getofferdata = Offer.objects.all()
    context = {
        "getoffer": getofferdata
    }
    return render(request, "coupon.html", context)


def addcouponpage(request):
    getofferdata = Offer.objects.all()
    getcatdata = category.objects.all()
    context = {
        "getoffer": getofferdata,
        "getcatdata": getcatdata
    }
    return render(request, "addcoupon.html", context)


def updateco(request, id):
    getofferid = Offer.objects.get(id=id)
    # getofferid=gofferid.id
    getcatdata = category.objects.all()
    context = {
        "offerid": getofferid,
        "getcatdata": getcatdata
    }
    return render(request, "updatecoup.html", context)


def updateoffer(request, id):
    name = request.POST.get("name")
    startdate = request.POST.get("startdate")
    enddate = request.POST.get("enddate")
    perc = request.POST.get("discount")
    cate = request.POST.get("category")
    # is_partner=request.POST.get("his_partner")

    # Check if 'his_partner' key is present in the form data
    is_active = request.POST.get('status', False)

    # Convert the string value to a boolean
    is_active = is_active == 'on'

    # Do something with the value, for example, save it to the database
    # hoteldata.is_partner = is_partner_value

    updatedata = Offer(id=id, name=name, start_date=startdate, end_date=enddate, discount_percentage=perc,
                       status=is_active, cat=category(id=cate))
    updatedata.save()
    return HttpResponseRedirect("/Coupon")


def deleteoffer(request, id):
    deloffer = Offer.objects.filter(id=id)
    deloffer.delete()
    return HttpResponseRedirect("/Coupon")


def gallerypage(request):
    return render(request, "gallery.html")


'''
def updategallery(request,id):
    name=request.POST.get("name")
    image=request.FILES['image']
    updatedata=gallery(id=id,name=name,gimage=image)
    updatedata.save()
    return redirect('/galleryl')
'''


def updategallery(request, id):
    gallery_instance = get_object_or_404(gallery, id=id)

    if request.method == 'POST':
        name = request.POST.get('name')  # Get the updated name
        image_file = request.FILES.get('gimage')  # Get the uploaded image file

        if image_file:
            gallery_instance.gimage = image_file  # Update the image if provided

        gallery_instance.name = name  # Update the name

        gallery_instance.save()  # Save the changes

        return redirect('/galleryl', id=gallery_instance.id)

    return render(request, 'gallerylist.html', {'gallery_instance': gallery_instance})


def gallerylpage(request):
    getgallerydata = gallery.objects.all()
    context = {
        'gallerydata': getgallerydata
    }
    return render(request, "gallerylist.html", context)


def fetchgallery(request):
    image = request.FILES['image']
    name = request.POST.get("name")
    insertimage = gallery(name=name, gimage=image)
    insertimage.save()
    return redirect('/galleryl')


def deletegallery(request, id):
    delgallery = gallery.objects.filter(id=id)
    delgallery.delete()

    return HttpResponseRedirect("/galleryl")


def galleryindex(request):
    data = gallery.objects.all()
    context = {
        "gdata": data
    }
    return render(request, "gallery1.html", context)


def fetchofferdata(request):
    name = request.POST.get("name")
    discount = request.POST.get("discount")
    startdate = request.POST.get("startdate")
    enddate = request.POST.get("enddate")
    cat = request.POST.get("category")
    # is_partner=request.POST.get("his_partner")

    # Check if 'his_partner' key is present in the form data
    is_active = request.POST.get('status', False)

    # Convert the string value to a boolean
    is_active = is_active == 'on'

    # Do something with the value, for example, save it to the database
    # hoteldata.is_partner = is_partner_value

    insertoffer = Offer(name=name, discount_percentage=discount, start_date=startdate, end_date=enddate,
                        status=is_active, cat=category(id=cat))
    insertoffer.save()
    return HttpResponseRedirect("/Coupon")


def adatepage(request):
    getasdata = available_dates.objects.all()
    gettripdata = Trip.objects.all()
    context = {
        'asdata': getasdata,
        'tripdata': gettripdata
    }
    return render(request, "adate.html", context)


def fetchasdata(request):
    tripn = request.POST.get("selecttrip")
    dates = request.POST.get("date")
    nslots = request.POST.get("slotsnumber")

    insertdata = available_dates(trip=Trip(id=tripn), date=dates, available_slots=nslots)
    insertdata.save()
    return redirect("/adate")


def updateadate(request, id):
    tripname = request.POST.get("selecttrip")
    dates = request.POST.get("availabled")
    nslots = request.POST.get("slotnumber")
    updatedata = available_dates(id=id, trip=Trip(id=tripname), date=dates, available_slots=nslots)
    updatedata.save()
    return redirect("/adate")


def deleteas(request, id):
    delas = available_dates.objects.filter(id=id)
    delas.delete()

    return HttpResponseRedirect("/adate")


def eventspage(request):
    getpackage = tourpackage.objects.all()
    context = {
        'package': getpackage
    }
    return render(request, "events.html", context)


def addeventspage(request):
    getstatedata = State.objects.all()
    getcitydata = city.objects.all()
    context = {
        'statedata': getstatedata,
        'citydata': getcitydata
    }
    return render(request, "addevents.html", context)


def fetchpackagedata(request):
    name = request.POST.get("name")
    description = request.POST.get("description")
    state = request.POST.get("selectedstate")
    image = request.FILES["image"]
    istop_des = request.POST.get("top_des", False)

    istop_des = istop_des == 'on'

    insertdata = tourpackage(name=name, description=description, state=State(id=state),
                             pimage=image, top_des=istop_des)
    insertdata.save()

    return redirect("/events")


def trippage(request):
    gettripdata = Trip.objects.all()
    getpackagedata = tourpackage.objects.all()
    getdurationdata = Duration.objects.all()
    getcategory = category.objects.all()
    getoffersdata = Offer.objects.all()
    getstatedata=State.objects.all()
    context = {
        'package': getpackagedata,
        'duration': getdurationdata,
        'category': getcategory,
        'offer': getoffersdata,
        'trip': gettripdata,
        'state':getstatedata
    }
    return render(request, "triplist.html", context)


def addtrippage(request):
    getpackagedata = tourpackage.objects.all()
    getdurationdata = Duration.objects.all()
    getcategory = category.objects.all()
    getoffersdata = Offer.objects.all()
    gethotel=Hotel.objects.all()
    context = {
        'package':getpackagedata,
        'duration':getdurationdata,
        'category':getcategory,
        'offer':getoffersdata
    }
    return render(request, "addtrip.html",context)


def updatetrip(request,id):
    tname=request.POST.get("name")
    desc=request.POST.get("description")
    pr=request.POST.get("price")
    pack=request.POST.get("selectpackage")
    if pack is None:
        pack=request.POST.get("tp")
    dur=request.POST.get("selectduration")
    if dur is None:
        dur=request.POST.get("duration")
    cat=request.POST.get("selectcategory")
    if cat is None:
        cat=request.POST.get("cat")
    offe=request.POST.get("selectoffers")
    if offe is None:
        offe=request.POST.get("offer")
    vid = request.FILES.get("video")
    if vid is None:
        vid=request.POST.get("videot")
    trans=request.POST.get("selecttrans")
    if trans is None:
        trans=request.POST.get("tm")
    img = request.FILES.get("image")
    if img is None:
        img = request.POST.get("imaget")
    updatedata=Trip(id=id,name=tname,description=desc,price=pr,tour_package=tourpackage(id=pack),duration=Duration(id=dur),category=category(id=cat),offers=Offer(id=offe),transport_mode=trans,tripimage=img,video=vid)
    updatedata.save()
    return HttpResponseRedirect("/trip")





def fetchtripdata(request):
    name = request.POST.get("name")
    description = request.POST.get("description")
    price = request.POST.get("price")
    tour_package_id = request.POST.get("selectpackage")
    duration_id = request.POST.get("selectduration")
    category_id = request.POST.get("selectcategory")
    hotel_id = request.POST.get("selecthotel")
    offer_id = request.POST.get("selectoffers")
    transport_mode = request.POST.get("selectmodeoftrans")
    tripimage = request.FILES['image']
    tripvideo = request.FILES['video']

    # Assuming Trip, TourPackage, Duration, Category, Hotel, Offer are model classes
    tour_package = tourpackage.objects.get(id=tour_package_id)
    duration = Duration.objects.get(id=duration_id)
    Category = category.objects.get(id=category_id)

    # Create Trip instance
    insertdata = Trip(
        name=name,
        description=description,
        price=price,
        tour_package=tour_package,
        duration=duration,
        category=Category,
        offers=Offer(id=offer_id),
        transport_mode=transport_mode,
        tripimage=tripimage,
        video=tripvideo
    )
    insertdata.save()
    return redirect('/trip')


def searchcat(request):
    query = request.GET.get('query')
    categories = category.objects.filter(name=query)
    context = {
        'categories': categories
    }
    return render(request, 'main-category.html', context)


def passengerlpage(request):
    getpassengerdetails = passenger.objects.all()
    context = {
        'passenger': getpassengerdetails
    }
    return render(request, "passengerl.html", context)


def addpassengerpage(request):
    return render(request, "addpassenger.html")


def login(request):
    return render(request, "login.html")


def gallerypage(request):
    data = gallery.objects.all()
    context = {
        "gdata": data
    }
    return render(request, "gallery1.html", context)


def addgallerypage(request):
    return render(request, "addgallery.html")


def fetchsignupdata(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        insertdata = signupdata(name=username, email=email, password=password, is_admin=False)
        insertdata.save()
        messages.success(request, 'Registration successfull !!')
        return redirect('/')
    else:
        return render(request, "index.html")


def checklogin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        checkuser = signupdata.objects.get(email=email, password=password)
        request.session['logid'] = checkuser.id
        request.session['logname'] = checkuser.name
        request.session['logemail'] = checkuser.email
        request.session['logadmin'] = checkuser.is_admin
    except:
        checkuser = None

    if checkuser is not None:
        if checkuser.is_admin is False:
            return redirect('/')
        else:
            return redirect('/dash')

    else:
        messages.error(request, "INVALID EMAIL OR PASSWORD. PLEASE TRY AGAIN")
        return redirect('/')

    messages.success(request, 'Login successfull !!')
    return render(request, "index.html")


def logoutpage(request):
    try:
        del request.session['logid']
        del request.session['logname']
        del request.session['logemail']
    except:
        pass
    return redirect('/')


def indexpage(request):
    data = tourpackage.objects.filter(top_des=True)
    getoffersdata = Offer.objects.all()
    offerids = [offer.id for offer in getoffersdata]  # Collecting all offer IDs
    tripalldata = Trip.objects.filter(offers__id__in=offerids)
    # gettripdata=tripalldata.objects.filter(offers=getoffersdata)
    for trip in tripalldata:
        trip.offers.discount_percentage_integer = int(trip.offers.discount_percentage)
    for trip in tripalldata:
        aggregate_rating = review.objects.filter(trip=trip).aggregate(avg_rating=Avg('rating'))
        trip.aggregate_rating = int(aggregate_rating['avg_rating'] or 0)
        trip.star_range = range(trip.aggregate_rating)

    context = {
        "data": data,
        "offersdata": getoffersdata,
        "tripoffer": tripalldata
    }

    return render(request, "index.html", context)




def bookingpage(request):
    return render(request, "package.html")







def bookingtwo(request):
    logid=request.session['logid']
    uuser=signupdata.objects.get(id=logid)
    trip_id = request.GET.get('tripid')
    #fdate=request.POST.get('slots')
    #fetchdate = available_dates.objects.filter(id=fdate)
    selected_date_id = request.session.get('selected_date_id')

    booktrip = Trip.objects.get(id=trip_id)


    total_amount = calculatepaypage(request, trip_id)
    getallpassdata = passenger.objects.all()
    passengers = passenger.objects.filter(customer=uuser,has_booked=False)
    num_passengers = passengers.count()


    # Add booktrip to the context
    context = {
        'getpassdata': getallpassdata,
        'total_amount': total_amount,
        'booktrip': booktrip,
        'passcount':num_passengers,
        'selected_date_id':selected_date_id
        #'fetchdate':fetchdate
    }

    # Render the template with the context
    return render(request, 'booking2.html', context)



def fetchpassenger(request, tripid):
    if 'logid' in request.session:
        logid = request.session['logid']
        user = signupdata.objects.get(id=logid)
        firstname = request.POST.get("fname")
        lastname = request.POST.get("lname")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        aadharno = request.POST.get("aadhar")
        fetchtrips = Trip.objects.get(id=tripid)
        tripid = fetchtrips.id
        total_amount = calculatepaypage(request, tripid)


        insertdata = passenger(customer=user, first_name=firstname, last_name=lastname, age=age, gender=gender,
                               aadhar_number=aadharno)
        insertdata.save()

        # Redirect back to the booking2 page with updated total_amount
        return HttpResponseRedirect(reverse('bookingtwo') + f'?tripid={tripid}&total_amount={total_amount}')

    else:
        return redirect('/bookingtwo')








def tourlist(request, pid):
    # Get the tour package based on the provided pid
    tour_package = get_object_or_404(tourpackage, pk=pid)

    # Get all trips associated with the tour package
    tour_package_trips = Trip.objects.filter(tour_package=tour_package)
    #getcatdata = category.objects.all()
    getcatdata = category.objects.filter(trip__tour_package=pid).annotate(count=Count('trip')).all()
    trip_destinations = []

    # Fetch destination data for each trip and store in the list
    for trip in tour_package_trips:
        destinations = Destination.objects.filter(trip=trip)
        trip_destinations.append((trip.id, destinations))

    # Calculate offer deducted price for each trip
    for trip in tour_package_trips:
        if trip.offers:
            offer = trip.offers
            # Check if the offer is active
            if offer.status and offer.start_date <= date.today() <= offer.end_date:
                # Calculate offer deducted price based on discount percentage
                discount_percentage = offer.discount_percentage
                offer_deducted_price = trip.price * (1 - discount_percentage / 100)
                trip.offer_deducted_price = math.ceil(offer_deducted_price)  # Round up to nearest integer
                trip.discount_percentage_integer = int(discount_percentage)
                trip.offer_deducted_price_integer = int(math.ceil(offer_deducted_price))
            else:
                # Offer is not active, so no discount applied
                trip.offer_deducted_price = trip.price
                trip.offer_deducted_price_integer = int(trip.price)


        else:
            # No offer available, so price remains the same
            trip.offer_deducted_price = trip.price
            trip.offer_deducted_price_integer = int(trip.price)
            trip.price_integer = int(trip.price)


    for trip in tour_package_trips:
        aggregate_rating = review.objects.filter(trip=trip).aggregate(avg_rating=Avg('rating'))
        trip.aggregate_rating = int(aggregate_rating['avg_rating'] or 0)
        # Calculate star range based on aggregate rating
        trip.star_range = range(int(trip.aggregate_rating))

    tour_packages_with_trips = tourpackage.objects.filter(trip__isnull=False).exclude(pk=pid).distinct()
    related_packages = random.sample(list(tour_packages_with_trips), min(3, len(tour_packages_with_trips)))
    for package in related_packages:
        package.total_trips = Trip.objects.filter(tour_package=package).count()

    context = {
        'tour_package': tour_package,  # Add tour package to context
        'data3': tour_package_trips,  # All trips associated with the tour package
        'rpack': related_packages,
        'getcatdata': getcatdata,
        'pid': pid,
        'trip_destinations': trip_destinations,
    }

    return render(request, "tourlist1.html", context)






def catpage(request,pid,cid):
    getcatdata=Trip.objects.filter(tour_package=pid,category=cid)
    context={
        'getcatdata':getcatdata
    }
    return render(request,"tourlist1.html",context)

def load_packages(request):
    category_id = request.GET.get('category_id')

    if not category_id:
        return HttpResponse('Category ID is missing', status=400)


    # Retrieve packages related to the selected category
    trips = Trip.objects.filter(category=category)

    # Generate HTML content for the packages
    html_content = '<div class="destination-list">'
    for trip in trips:
        html_content += f'''
            <div class="trend-full bg-white rounded box-shadow overflow-hidden p-4 mb-4">
                <div class="row">
                    <div class="col-lg-4 col-md-3">
                        <div class="trend-item2 rounded">
                            <a href="tour-single.html" style="background-image: url(../media/{trip.tripimage});"></a>
                            <div class="color-overlay"></div>
                        </div>
                        <br><br><br><br>
                    </div>
                    <div class="col-lg-5 col-md-6">
                        <div class="trend-content position-relative text-md-start text-center">
                            <small>{trip.duration}</small>
                            <h3 class="mb-1"><a href="tour-single.html">{trip.name}</a></h3>
                            <h6 class="theme mb-0"><i class="icon-location-pin">{trip.tour_package}</i></h6>
                            <p class="mt-4 mb-0">Taking Safety Measures <br><a href="#"><span class="theme"> Free cancellation</span></a></p>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-3">
                        <div class="trend-content text-md-end text-center">
                            <div class="rating">
                                <span class="fa fa-star checked"></span>
                                <span class="fa fa-star checked"></span>
                                <span class="fa fa-star checked"></span>
                                <span class="fa fa-star checked"></span>
                                <span class="fa fa-star checked"></span>
                            </div>
                            <small>200 Reviews</small>
                            <div class="trend-price my-2">
                                <span class="mb-0"></span>
                                <h3 class="mb-0">{trip.price}</h3>
                                <small>Per Adult</small>
                            </div>
                            <a href="/toursingle/{trip.id}" class="nir-btn">View Detail</a>
                        </div>
                    </div>
                    <br><br>
                </div>
            </div>
        '''
    html_content += '</div>'

    return HttpResponse(html_content)






def toursingle(request, pid):
    # Get the single Trip object based on the provided pid
    trip = get_object_or_404(Trip, id=pid)
    tripid = trip.id

    today = date.today()
    desdata = Destination.objects.filter(trip=tripid)
    avdata = available_dates.objects.filter(trip=tripid, date__gt=today)
    itinerary = Itinerary.objects.filter(trip=tripid)
    hdata = Hotel.objects.all()

    # Calculate aggregate rating for the trip
    aggregate_rating = review.objects.filter(trip=trip).aggregate(avg_rating=Avg('rating'))
    trip.aggregate_rating = int(aggregate_rating['avg_rating'] or 0)
    trip.star_range = range(trip.aggregate_rating)

    # Calculate the range of stars
    stars_range = range(trip.aggregate_rating)

    # Get a random review for the trip
    random_review = random.choice(review.objects.filter(trip=trip))

    context = {
        'data4': trip,  # Pass the single Trip object
        'data5': itinerary,  # Pass the related itinerary objects
        'avdata': avdata,
        'tripid': tripid,
        'hdata': hdata,
        'desdata': desdata,
        'stars_range': stars_range,
        'random_review': random_review  # Pass the random review to the template
    }

    return render(request, "tour-single.html", context)


def fetchavdata(request):
    gettrip = request.POST.get("tripid")
    fetchtrips = Trip.objects.get(id=gettrip)
    logid = request.session.get('logid')


    getslots = request.POST.get("slots")
    fetchdate = available_dates.objects.filter(id=getslots).first()
    request.session['selected_date_id'] = fetchdate.id if fetchdate else None
    if logid is None:
        messages.error(request, "you are not logged in, so please log in or login afer signup")
        return redirect('/')

    passengera = passenger.objects.filter(customer=logid)
    total_amount = calculatepaypage(request, gettrip)
    context = {
        #'getslots': getslots,
        'gettrip': gettrip,
        'booktrip': fetchtrips,
        'total_amount': total_amount,
        'getpassdata': passengera,
        'selected_date_id': request.session.get('selected_date_id')
        #'fetchdate':fetchdate
    }

    return render(request, 'booking2.html', context)


def tourpackagepage(request):
    gettourdata = tourpackage.objects.all()
    context = {
        'packagedata': gettourdata
    }
    return render(request, 'package.html', context)





def calculatepaypage(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip_price = trip.price
    logid = request.session.get('logid')

    # Retrieve passengers based on logid
    passengers = []
    if logid:
        passengers = passenger.objects.filter(customer=logid, has_booked=False)

    # Calculate total amount without offer
    total_amount = 0
    for i in passengers:
        # Check if passenger age is between 0 and 5
        if 0 <= i.age <= 5:
            continue  # Skip this passenger
        # Otherwise, add trip price to total amount
        total_amount += trip_price

    # Check if there's an active offer for this trip
    if trip.offers and trip.offers.status:
        today = date.today()
        if trip.offers.start_date <= today <= trip.offers.end_date:
            # Apply offer discount
            discount = trip_price * (trip.offers.discount_percentage / 100)
            total_amount -= discount

    # Format the total_amount to two decimal places
    total_amount = max(total_amount, 0)
    total_amount = round(total_amount, 2)

    return total_amount


def deletefrontpasspage(request, id, tripid):
    passengerr = passenger.objects.filter(id=id)
    passengerr.delete()
    fetchtrips = Trip.objects.get(id=tripid)
    tripid = fetchtrips.id
    total_amount = calculatepaypage(request, tripid)
    # return redirect('/bookingtwo')
    # return render(request, 'booking2.html', {'passenger': passengerr})
    return HttpResponseRedirect(reverse('bookingtwo') + f'?tripid={tripid}&total_amount={total_amount}')


def ufpasspage(request, id, bk):
    getpassdata = passenger.objects.get(id=id)
    fetchtrips = Trip.objects.get(id=bk)
    tripid = fetchtrips.id
    total_amount = calculatepaypage(request, tripid)
    context = {
        'passengerr': getpassdata,
        'tripid': tripid,
        'tm': total_amount
    }
    return render(request, 'updatepassfront.html', context)


def updatefrontpasspage(request, tripid, id):
    # Retrieve the passenger object
    logid = request.session.get('logid')
    user = signupdata.objects.get(id=logid)
    firstname = request.POST.get('fname')
    lastname = request.POST.get('lname')
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    aadhar = request.POST.get('aadhar')
    fetchtrips = Trip.objects.get(id=tripid)
    tripid = fetchtrips.id
    total_amount = calculatepaypage(request, tripid)
    updatedata = passenger(id=id, customer=user, first_name=firstname, last_name=lastname, age=age, gender=gender,
                           aadhar_number=aadhar)
    # Example: passenger.first_name = request.POST['first_name']
    updatedata.save()
    # return redirect('/bookingtwo')
    return HttpResponseRedirect(reverse('bookingtwo') + f'?tripid={tripid}&total_amount={total_amount}')







def payment_booking(request, tripid):
    if request.method == 'POST':
        logid = request.session.get('logid')
        uuser = signupdata.objects.get(id=logid)

        # Extract payment details
        cardhname = request.POST.get("name")
        cardn = request.POST.get("cardno")
        exp = request.POST.get("expiry")
        cv = request.POST.get("cvv")
        tamount = request.POST.get("tamount")

        # Extract booking details
        dateas_id = request.POST.get('dates')
        dateas = available_dates.objects.get(id=dateas_id)
        trip = Trip.objects.get(id=tripid)
        total_amount = calculatepaypage(request, tripid)
        booking_date = timezone.now()

        # Save payment details
        insert_payment = Payment(user=uuser, card_holder_name=cardhname, expiration_date=exp, card_number=cardn,
                                 cvv=cv, amount=tamount)
        insert_payment.save()

        # Count the number of passengers booked
        num_passengers = passenger.objects.filter(customer=uuser, has_booked=False).count()

        # Check if there are passengers to book
        if num_passengers == 0:
            messages.error(request, "No passengers to book.")
            #return redirect("/bookingtwo")
            return HttpResponseRedirect(reverse('bookingtwo') + f'?tripid={tripid}&total_amount={total_amount}')

        # Check if enough slots are available
        if dateas.available_slots >= num_passengers:
            # Save booking details
            insert_booking = Booking(user=uuser, num_passengers=num_passengers, trip=trip, dateb=dateas,
                                     booking_date=booking_date, is_payment_done=True)
            insert_booking.save()

            # Update available slots
            dateas.available_slots -= num_passengers
            dateas.save()

            # Mark passengers as booked (Optional)
            for p in passenger.objects.filter(customer=uuser, has_booked=False):
                p.has_booked = True
                p.save()
            del request.session['selected_date_id']
            messages.success(request, "Booking done successfully.")
            return redirect("/mbook")
        else:
            messages.error(request, "Not enough slots available for booking.")
            return redirect("/mbook")
    else:
        return HttpResponse("Method not allowed")



def fetch_passenger_data(request, trip_id):
    # Retrieve confirmed booking for the trip
    confirmed_booking = Booking.objects.filter(is_cancelled=False, trip_id=trip_id).first()

    # If there's a confirmed booking, retrieve passengers associated with it
    if confirmed_booking:
        confirmed_passengers = passenger.objects.filter(customer=request.user, has_booked=False)
    else:
        # If no confirmed booking, fetch all passengers associated with the user
        confirmed_passengers = passenger.objects.filter(customer=request.user, has_booked=False)

    return render(request, 'booking2.html', {'confirmed_passengers': confirmed_passengers})


def Contact(request):
    return render(request, "contact.html")


def contactpage(request):
    cdata = contact.objects.all()
    context = {
        "cdata": cdata
    }
    return render(request, "inquiry.html", context)


def fetchcontactdata(request):
    firstname = request.POST.get("firstname")
    lastname = request.POST.get("lastname")
    email = request.POST.get("uemail")
    phone = request.POST.get("uphone")
    message = request.POST.get("ucomments")

    insertdata = contact(firstname=firstname, lastname=lastname, email=email, phone=phone, message=message)
    insertdata.save()

    return HttpResponseRedirect("/inquiry")


def updatecontact(request, id):
    firstname = request.POST.get("firstname")
    lastname = request.POST.get("lastname")
    email = request.POST.get("uemail")
    phone = request.POST.get("uphone")
    message = request.POST.get("ucomments")

    updatedata = contact(id=id, firstname=firstname, lastname=lastname, email=email, phone=phone, message=message)
    updatedata.save()
    return HttpResponseRedirect("/inquiry")


def deletecontact(request, id):
    delcontact = contact.objects.filter(id=id)
    delcontact.delete()

    return HttpResponseRedirect("/inquiry")


def inquiry(request):
    return render(request, "inquiry.html")


def about(request):
    aboutdata = About.objects.all()
    context = {
        "aboutdata": aboutdata
    }
    return render(request, "about.html", context)


def hotel(request):
    return render(request, "hotel.html")


def showHotel(request):
    hdata = Hotel.objects.all()
    citydata = city.objects.all()
    context = {
        "hoteldata": hdata,
        "citydata": citydata
    }
    return render(request, "hotel.html", context)


def forgotpasswordpage(request):
    return render(request, "forgotpassword.html")


def changepsswrdpage(request):
    return render(request, "changepsswrdpage.html")


def fetchchangepass(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        old_password = request.POST.get("oldpassword")
        new_password = request.POST.get("newpassword")
        confirm_password = request.POST.get("confirmpassword")

        # Check if any input field is empty
        if not email or not old_password or not new_password or not confirm_password:
            messages.error(request, "All input fields are required.")
            return redirect("/changepsswrdpage")

        # Fetch user based on email
        user = signupdata.objects.filter(email=email).first()

        # Check if user exists and old password is correct
        if user and user.password == old_password:
            # Check if new password and confirm password match
            if new_password == confirm_password:
                # Update password
                user.password = new_password
                user.save()
                messages.success(request, "Password Changed Successfully!!")
                return redirect("/")  # Redirect to some page after successful password change
            else:
                # Passwords don't match
                return render(request, 'changepsswrdpage.html', {'error': 'New passwords do not match'})
        else:
            # User does not exist or old password is incorrect
            messages.error(request, "Invalid Email or Password")
            return redirect("/changepsswrdpage")
    else:
        return render(request, 'changepsswrdpage.html')


def newforgotpassword(request):
    if request.method == 'POST':
        username = request.POST['email']
        try:
            user = signupdata.objects.get(email=username)

        except signupdata.DoesNotExist:
            user = None
        # if user exist then only below condition will run otherwise it will give error as described in else condition.
        if user is not None:
            #################### Password Generation ##########################
            import random
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                       'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

            nr_letters = 6
            nr_symbols = 1
            nr_numbers = 3
            password_list = []

            for char in range(1, nr_letters + 1):
                password_list.append(random.choice(letters))

            for char in range(1, nr_symbols + 1):
                password_list += random.choice(symbols)

            for char in range(1, nr_numbers + 1):
                password_list += random.choice(numbers)

            print(password_list)
            random.shuffle(password_list)
            print(password_list)

            password = ""  # we will get final password in this var.
            for char in password_list:
                password += char

            ##############################################################

            msg = "hello here it is your new password  " + password  # this variable will be passed as message in mail

            ############ code for sending mail ########################

            from django.core.mail import send_mail

            send_mail(
                'Your New Password',
                msg,
                'krushanuinfolabz@gmail.com',
                [username],
                fail_silently=False,
            )
            # NOTE: must include below details in settings.py
            # detail tutorial - https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
            # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
            # EMAIL_HOST = 'smtp.gmail.com'
            # EMAIL_USE_TLS = True
            # EMAIL_PORT = 587
            # EMAIL_HOST_USER = 'mail from which email will be sent'
            # EMAIL_HOST_PASSWORD = 'pjobvjckluqrtpkl'   #turn on 2 step verification and then generate app password which will be 16 digit code and past it here

            #############################################

            # now update the password in model
            cuser = signupdata.objects.get(email=username)
            cuser.password = password
            cuser.save(update_fields=['password'])

            print('Mail sent')
            messages.info(request, 'mail is sent')
            return redirect("/")

        else:
            messages.info(request, 'This account does not exist')
    return redirect("/")


def showHotel(request):
    hdata = Hotel.objects.all()
    citydata = city.objects.all()
    context = {
        "hoteldata": hdata,
        "citydata": citydata
    }
    return render(request, "hotel.html", context)


def fetchhoteldata(request):
    name = request.POST.get("hname")
    description = request.POST.get("hdesc")
    rating = request.POST.get("hrating")
    city_id = request.POST.get("hcity")

    inserthotel = Hotel(name=name, description=description, rating=rating, city_id=city_id)
    inserthotel.save()
    return HttpResponseRedirect("/hotel")


def updatehotel(request, id):
    name = request.POST.get("hname")
    description = request.POST.get("hdesc")
    rating = request.POST.get("hrating")
    city_id = request.POST.get("hcity")

    updatedata = Hotel(id=id, name=name, description=description, rating=rating, city=city(id=city_id))
    updatedata.save()
    return HttpResponseRedirect("/hotel")


def deletehotel(request, id):
    delhotel = Hotel.objects.filter(id=id)
    delhotel.delete()

    return HttpResponseRedirect("/hotel")


def addhotel(request):
    citydata = city.objects.all()
    context = {
        "citydata": citydata
    }
    return render(request, "addhotel.html", context)


def itinerarypage(request):
    itinerarydata = Itinerary.objects.all()
    gettripdata = Trip.objects.all()

    context = {
        "itinerarydata": itinerarydata,
        "gettripdata": gettripdata
    }
    return render(request, "itinerary.html", context)


def fetchitinerarydata(request):
    trip = request.POST.get("selecttrip")
    day_number = request.POST.get("dayno")
    destination = request.POST.get("dest")
    activities = request.POST.get("act")

    insertabout = Itinerary(trip=Trip(id=trip), day_number=day_number, destination=destination, activities=activities)
    insertabout.save()
    return HttpResponseRedirect("/itinerary")


def updateitinerary(request, id):
    trip = request.POST.get("selecttrip")
    day_number = request.POST.get("dayno")
    destination = request.POST.get("dest")
    activities = request.POST.get("act")

    updatedata = Itinerary(id=id, trip=Trip(id=trip), day_number=day_number, destination=destination,
                           activities=activities)
    updatedata.save()
    return HttpResponseRedirect("/itinerary")


def deleteitinerary(request, id):
    delitinerary = Itinerary.objects.filter(id=id)
    delitinerary.delete()

    return HttpResponseRedirect("/itinerary")


def additinerary(request):
    itinerarydata = Itinerary.objects.all()
    gettripdata = Trip.objects.all()
    context = {
        "itinerarydata": itinerarydata,
        "gettripdata": gettripdata
    }
    return render(request, "additinerary.html", context)


def aboutsecpage(request):
    aboutdata = About.objects.all()
    context = {
        "aboutdata": aboutdata
    }
    return render(request, "about-sec.html", context)


def fetchaboutdata(request):
    subtitle = request.POST.get("sub")
    title = request.POST.get("name")
    description = request.POST.get("desc")

    insertabout = About(subtitle=subtitle, title=title, description=description)
    insertabout.save()
    return HttpResponseRedirect("/about-sec")


def updateabout(request, id):
    subtitle = request.POST.get("sub")
    title = request.POST.get("name")
    description = request.POST.get("desc")

    updatedata = About(id=id, subtitle=subtitle, title=title, description=description)
    updatedata.save()
    return HttpResponseRedirect("/about-sec")


def deleteabout(request, id):
    delabout = About.objects.filter(id=id)
    delabout.delete()

    return HttpResponseRedirect("/about-sec")


def inquiry(request):
    return render(request, "inquiry.html")


def userslistpage(request):
    getuserdata = signupdata.objects.all()
    context = {
        'usersdata': getuserdata
    }
    return render(request, "userslist.html", context)


def adduserpage(request):
    return render(request, "adduser.html")


def fetchusersdata(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    insertdata = signupdata(name=username, email=email, password=password)
    insertdata.save()

    return redirect("/userslist")


def deleteuser(request, id):
    name = request.POST.get("username")
    deletedata = signupdata(id=id, name=name)
    deletedata.delete()

    return redirect("/userslist")





def mybook(request):
    detail = Booking.objects.all()
    user=request.session.get("logid")
    userr=Booking.objects.filter(user=user)
    context={
        'bdetail':detail,
        'user':userr
    }
    return render(request,"mybooking.html",context)



def cancelb(request, id):
    # Get the booking object or return a 404 if not found
    booking = get_object_or_404(Booking, id=id)

    # Check if the booking is not already cancelled
    if booking.status != 'cancelled':
        # Mark the booking as cancelled
        booking.status = 'cancelled'
        booking.save()

        # Increment the available slots
        dateb = booking.dateb
        dateb.available_slots += booking.num_passengers
        dateb.save()

    # Redirect to the appropriate URL after cancellation
    return HttpResponseRedirect("/mbook")
def profiledash(request):
    signupdatad=signupdata.objects.filter(is_admin=True)
    context={
        'admindata':signupdatad
    }
    return render(request,"profile.html",context)

def updateprofile(request):
    #logidd = request.session.get('logid')
    #user = signupdata.objects.get(id=logidd)
    user=request.POST.get("adminid")
    name=request.POST.get("name")
    email=request.POST.get("email")
    password=request.POST.get("password")
    updatedata=signupdata(id=user,name=name,password=password,email=email,is_admin=True)
    updatedata.save()
    messages.success(request, 'Profile Updated successfully !!')
    return redirect('/dash')


def updatepackagepage(request,id):
    getpackage = tourpackage.objects.get(id=id)
    selected_state_id = getpackage.state  # Extract the ID of the associated state
    statedata = State.objects.all()  # Get all states
    citydata = city.objects.all()  # Assuming you have a City model



    context = {
        'tourpackage': getpackage,
        'statedata': statedata,
        'selected_state_id': selected_state_id,  # Pass selected_state_id to the context
        'citydata': citydata,

    }
    return render(request, "updatepackage.html", context)

def deletepackage(request,id):
    deletedata = tourpackage.objects.filter(id=id)
    deletedata.delete()
    return HttpResponseRedirect("/events")






def updatepackagefinalpage(request,id):
    name = request.POST.get("name")
    description = request.POST.get("description")
    state = request.POST.get("selectedstate")

    image = request.FILES.get("image")
    if image is None:
        image = request.POST.get("cimage")
    istop_des = request.POST.get("top_des", False)

    istop_des = istop_des == 'on'

    insertdata = tourpackage(id=id,name=name, description=description, state=State(id=state),
                             pimage=image, top_des=istop_des)
    insertdata.save()
    return redirect("/events")


def fetchreview(request):
    gettrip = request.POST.get("tripid")
    name = request.POST.get("name")
    email = request.session.get("logemail")
    comment = request.POST.get("comment")
    rating = request.POST.get("rating")


    insertreview = review(trip=Trip(id=gettrip),name=name,email=email,comment=comment,rating=rating)
    insertreview.save()
    messages.success(request , "Review Submitted!")
    return redirect('toursingle', pid=gettrip)



def userslistpage(request):
    getuserdata = signupdata.objects.all()
    context = {
        'usersdata':getuserdata
    }
    return render(request, "userslist.html",context)

def adduserpage(request):
    return render(request, "adduser.html")

def fetchusersdata(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    insertdata = signupdata(name=username,email=email,password=password)
    insertdata.save()

    return redirect("/userslist")

def deleteuser(request,id):
    name = request.POST.get("username")
    deletedata = signupdata(id=id, name=name)
    deletedata.delete()

    return redirect("/userslist")


def deletetrip(request,id):
    deldata = Trip.objects.filter(id=id)
    deldata.delete()

    return HttpResponseRedirect("/trip")


def bcrud(request):
    bdata=Booking.objects.all()

    context={
        'bdata':bdata
    }
    return render(request,"Bookingcrud.html",context)

'''def updatebooks(request,id):
    statusb=request.POST.get("status")
    user=request.POST.get("user")
    pss=request.POST.get("pss")
    trip=request.POST.get("trip")

    dateb=request.POST.get("dateb")
    updatedata = Booking(id=user, status=statusb,num_passengers=pss,trip=Trip(id=id),dateb=dateb)
    updatedata.save()
    return HttpResponseRedirect("/bcrud")
'''

def updatebooks(request,id):
    if request.method == 'POST':
        statusb = request.POST.get("statusb")
        pss = request.POST.get("pss")
        trip = request.POST.get("trip")
        tripp=Trip.objects.get(id=trip)
        datebb = request.POST.get("dat")
        datebk=available_dates.objects.filter(id=datebb)
        userb=request.POST.get("userr")
        userrb=signupdata.objects.get(id=userb)
        bookingd = request.POST.get("bookingd")

        # Convert booking date to the correct format

        # Check if dateb exists and save it if necessary


        updatedata = Booking(id=id,user=userrb,status=statusb, num_passengers=pss, trip=tripp, dateb=available_dates(id=datebb), booking_date=bookingd)
        updatedata.save()
        return HttpResponseRedirect("/bcrud")

def deletebook(request,id):
    deldata = Booking.objects.filter(id=id)
    deldata.delete()

    return HttpResponseRedirect("/bcrud")

def deletepass(request,id):
    deldata=passenger.objects.filter(id=id)
    deldata.delete()

    return HttpResponseRedirect("/passengerl")



'''def updatebooks(request, id):
    if request.method == 'POST':
        statusb = request.POST.get("statusb")
        pss = request.POST.get("pss")
        trip = request.POST.get("trip")
        datebb = request.POST.get("dateb")
        bookingd = request.POST.get("bookingd")

        # Convert booking date to the correct format


        updatedata = Booking(id=id, status=statusb, num_passengers=pss, trip=Trip(id=id), dateb=available_dates(id=datebb), booking_date=bookingd)
        updatedata.save()
        return HttpResponseRedirect("/bcrud")'''




def generate_booking_report_pdf(request):
    bookings = Booking.objects.all()

    # Prepare data to pass to the template
    context = {
        'booking_data': bookings,
        'current_datetime': datetime.datetime.now(),
        'title': 'Booking Report',  # Title for the report
    }

    # Render template
    template = get_template('booking_report.html')
    html = template.render(context)

    # Create a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="booking_report.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


def reviewpage(request):
    rdata=review.objects.all()
    context= {
        'rdata':rdata
    }
    return render(request, "review.html",context)

def deleter(request,id):
    delr = review.objects.filter(id=id)
    delr.delete()

    return HttpResponseRedirect("/review")

def generate_package_report_pdf(request):
    packages = tourpackage.objects.all()

    # Prepare data to pass to the template
    context = {
        'package_data': packages,
        'current_datetime': datetime.datetime.now(),
        'title': 'Tour Package Report',  # Title for the report
    }

    # Render template
    template = get_template('package_report.html')
    html = template.render(context)

    # Create a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="package_report.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response

def generate_offer_report_pdf(request):
    offers = Offer.objects.all()

    # Prepare data to pass to the template
    context = {
        'offer_data': offers,
        'current_datetime': datetime.datetime.now(),
        'title': 'Offer Report',  # Title for the report
    }

    # Render template
    template = get_template('offer_report.html')
    html = template.render(context)

    # Create a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="offer_report.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response

def generate_trip_report_pdf(request):
    trip = Trip.objects.all()

    # Prepare data to pass to the template
    context = {
        'trip_data': trip,
        'current_datetime': datetime.datetime.now(),
        'title': 'Trip Report',  # Title for the report
    }

    # Render template
    template = get_template('trip_report.html')
    html = template.render(context)

    # Create a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="offer_report.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response

def search_suggestions(request):
    query = request.GET.get('searchInput', '').strip()

    if query:
        destinations = Destination.objects.filter(city__name__icontains=query)

        # Convert queryset to a list of dictionaries
        results = [
            {"name": d.city.name, "url": f"/destination/{d.id}/"}  # Modify the URL as needed
            for d in destinations
        ]

        return JsonResponse(results, safe=False)

    return JsonResponse([], safe=False)


def destination_detail(request, id):
    destination = get_object_or_404(Destination, id=id)
    return render(request, "destination_detail.html", {"destination": destination})









from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from datetime import date
from .forms import BookingForm,ReviewForm
from .models import Booking, Event,Review
import logging
from django.core.mail import send_mail
from .tasks import send_booking_email
from .models import Review
from .models import Booking, Review
from .forms import ReviewForm


def login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        is_admin = request.POST.get('is_admin')  # Checkbox for admin login

        # Check if user exists with username or email
        user = None
        try:
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                user = None

        if user is not None and user.check_password(password):
            if is_admin:  # Admin checkbox selected
                if user.is_superuser:
                    auth_login(request, user)
                    messages.success(request, 'Admin login successful!')
                    return redirect('adminhome')  # Redirect to the admin home page
                else:
                    messages.error(request, "Superuser privileges required for admin login.")
            else:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('event')  # Redirect to the event page for regular users
        else:
            messages.error(request, 'Username or email or password is incorrect.')

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not email or not password or not confirm_password:
            messages.error(request, 'All fields are required.')
            return redirect('register')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email address.')
            return redirect('register')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already in use.')
            return redirect('register')

        User.objects.create_user(username=email, email=email, password=password)
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')

    return render(request, 'register.html')

def index(request):
   
    return render(request, 'index.html', )

def about(request):
    return render(request, 'about.html')





def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            total_cost = form.calculate_total_cost()
            
            # Save the booking object and keep reference to it
            booking = Booking.objects.create(
                event_name=form.cleaned_data['event_name'],
                event_place=form.cleaned_data['event_place'],
                email=form.cleaned_data['email'],
                event_date=form.cleaned_data['event_date'],
                mobile_number=form.cleaned_data['mobile_number'],
                number_of_persons=form.cleaned_data['number_of_persons'],
                description=form.cleaned_data['description']
            )

          # Send email asynchronously using Celery
            send_booking_email.delay(booking.id, booking.email, booking.event_name)  # Pass event_name if needed

            
            # Pass the booking object and total cost to the template
            return render(request, 'booking_success.html', {'booking': booking, 'total_cost': total_cost})
        else:
            messages.error(request, 'Please correct the errors below.')
            print(form.errors)  # Log form errors to console for debugging
    else:
        form = BookingForm()
    
    return render(request, 'booking.html', {'form': form})







def contact(request):
    return render(request, 'contact.html')

def event(request):
    events = Event.objects.all()
    return render(request, 'event.html', {'events': events})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def adminhome(request):
    query = request.GET.get('q')
    if query:
        booked_events = Booking.objects.filter(event_name__icontains=query)
    else:
        booked_events = Booking.objects.all()  # Fetch all booked events

    return render(request, 'adminhome.html', {
        'booked_events': booked_events,
    })






@login_required
@user_passes_test(lambda u: u.is_superuser)
def addbooking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            Booking.objects.create(
                
                event_name=form.cleaned_data['event_name'],
                event_place=form.cleaned_data['event_place'],
                email=form.cleaned_data['email'],
                event_date=form.cleaned_data['event_date'],
                mobile_number=form.cleaned_data['mobile_number'],
                number_of_persons=form.cleaned_data['number_of_persons'],
                description=form.cleaned_data['description']
            )
            messages.success(request, 'Booking added successfully!')
            return redirect('adminhome')
    else:
        form = BookingForm()
    
    return render(request, 'addbooking.html', {'form': form})






@login_required
@user_passes_test(lambda u: u.is_superuser)
def editbooking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking updated successfully!')
            return redirect('adminhome')
    else:
        form = BookingForm(instance=booking)
    
    return render(request, 'editbooking.html', {'form': form , 'booking': booking})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def deletebooking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted successfully!')
        return redirect('adminhome')
    
    return render(request, 'confirmdelete.html', {'booking': booking})

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')

def adminlogin(request):
    return redirect('adminhome')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def adminlogout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')  # Redirect to the login page or any other page you prefer



def booking_success(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            return redirect('thankyou')  # Redirect to a thank you page or another success page
    else:
        form = ReviewForm()

    return render(request, 'review.html', {'form': form, 'booking': booking})





def review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect('thankyoupage')  # Change to the actual thank you page
    else:
        form = ReviewForm()

    return render(request, 'review.html', {'form': form, 'booking': booking})


def thankyoupage(request):
    return render(request, 'thankyou.html')

def feedback_view(request):
    reviews = Review.objects.select_related('booking').all()  # Fetch all reviews along with their booking details
    return render(request, 'feedback.html', {'reviews': reviews})







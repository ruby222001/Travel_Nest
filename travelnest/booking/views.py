from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from homestay.models import HomeStay
from django.contrib.auth.decorators import login_required
from .models import Booking, Review
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone


# Create your views here.


@login_required
def book_homestay(request, homestay_id):
    homestay = get_object_or_404(HomeStay, id=homestay_id)
    user = request.user

    if user.is_authenticated:
        if user.is_host:
            # If user is a host, display error message
            messages.error(request, 'You are logged in as a host.')
            return redirect('detail', homestay_id=homestay.id)
        else:
            # User is a guest, allow booking
            if request.method == 'POST':
                # Process form submission
                check_in_date = request.POST.get('formatted_check_in_date')
                check_out_date = request.POST.get('formatted_check_out_date')
                num_guests = int(request.POST.get('num_guests'))
                totalAmount = request.POST.get('totalAmount') 
                payment_type = request.POST.get('payment_option')

                # Perform validation as needed
                if check_in_date and check_out_date and num_guests and payment_type:
                    # Convert num_guests to an integer
                    num_guests = int(num_guests)

                    # Create a new booking instance and save it
                    booking = Booking.objects.create(
                        homestay=homestay,
                        user=user,
                        check_in_date=check_in_date,
                        check_out_date=check_out_date,
                        num_guests=num_guests,
                        amount=totalAmount,
                        payment_type=payment_type
                    )
                    # Proceed with booking or display confirmation
                    messages.success(request, 'Booking successful!')

                    # # Send confirmation email to the user
                    # subject = 'Homestay Booking Confirmation'
                    # html_message = render_to_string('booking_confirmation_email.html', {'homestay': homestay, 'booking': booking})
                    # plain_message = strip_tags(html_message)
                    # send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [request.user.email], html_message=html_message)
                    return redirect('detail', homestay_id=homestay.id)
                else:
                    # Handle invalid form data
                    messages.error(request, 'Invalid form data. Please fill in all fields.')
                    return redirect('detail', homestay_id=homestay.id)
            else:
                return render(request, 'detail.html', {'homestay': homestay})
    else:
        # If user is not authenticated, display error message
        messages.error(request, 'You must be logged in to book a homestay.')
        return render(request, 'detail.html', {'homestay': homestay})
    
def add_review(request, homestay_id):
    today = timezone.now().date()
    print("Today's Date:", today)

    homestay = get_object_or_404(HomeStay, id=homestay_id)

    user_has_booked_homestay = Booking.objects.filter(
    homestay=homestay,
    user=request.user,
    check_out_date__lte=today
    ).exists()

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if request.user.is_authenticated and user_has_booked_homestay:
            Review.objects.create(
                homestay=homestay,
                user=request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, 'Review submitted successfully.')
        else:
            messages.error(request, 'Unable to submit the review.')

    reviews = Review.objects.filter(homestay=homestay).order_by('-created_at')
    # Inside the add_review view
    print("User has booked homestay:", user_has_booked_homestay)


    return render(request, 'detail.html', {'homestay': homestay, 'reviews': reviews, 'user_has_booked_homestay': user_has_booked_homestay})

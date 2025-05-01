from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from .models import Donation, Request, Donor
from .forms import (
    DonorSignupForm,
    ReceiverSignupForm,
    DonorLoginForm,
    DonationForm,
    ReceiverLoginForm,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


def home(request):
    return render(request, "home.html")


def donor_signup(request):
    if request.method == "POST":
        form = DonorSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            if User.objects.filter(username=username).exists():
                messages.error(
                    request, "Username already exists. Please choose a different one."
                )
                return redirect("donor_signup")

            form.save()
            messages.success(
                request, "Donor account created successfully! You can now login."
            )
            return redirect("donorLogin")
    else:
        form = DonorSignupForm()

    return render(request, "donor_signup.html", {"form": form})


def receiver_signup(request):
    if request.method == "POST":
        form = ReceiverSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            if User.objects.filter(username=username).exists():
                messages.error(
                    request, "Username already exists. Please choose a different one."
                )
                return redirect("receiver_signup")

            form.save()
            messages.success(
                request, "Receiver account created successfully! You can now login."
            )
            return redirect("RecieverLogin")
    else:
        form = ReceiverSignupForm()
    return render(request, "receiver_signup.html", {"form": form})


def donor_login_view(request):
    if request.method == "POST":
        form = DonorLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user and user.user_type == "donor":
                login(request, user)
                return redirect("donor_dashboard")
            else:
                form.add_error(None, "Invalid credentials or not a donor account.")
    else:
        form = DonorLoginForm()
    return render(request, "donorLogin.html", {"form": form})


def receiver_login_view(request):
    if request.method == "POST":
        form = ReceiverLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user and user.user_type == "receiver":
                login(request, user)
                print(f"Receiver login successful: {user.username}, redirecting to receiver_dashboard")
                return redirect("receiver_dashboard")
            else:
                form.add_error(None, "Invalid credentials or not a receiver account.")
    else:
        form = ReceiverLoginForm()
    return render(request, "RecieverLogin.html", {"form": form})


@login_required
def donor_dashboard(request):
    if request.user.user_type != "donor":
        return redirect("home")

    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()
            messages.success(request, "Donation posted successfully!")
            return redirect("donor_dashboard")
    else:
        form = DonationForm()

    donations = Donation.objects.filter(donor=request.user)
    requests = Request.objects.filter(donation__donor=request.user)
    return render(
        request,
        "donor_dashboard.html",
        {"form": form, "donations": donations, "requests": requests},
    )
def logout_view(request):
    logout(request)
    return redirect('home')

def edit_donation(request, id):
    donation = get_object_or_404(Donation, id=id, donor=request.user)
    if request.method == 'POST':
        form = DonationForm(request.POST, instance=donation)
        if form.is_valid():
            form.save()
            return redirect('donor_dashboard')
    else:
        form = DonationForm(instance=donation)
    return render(request, 'edit_donation.html', {'form': form})

def delete_donation(request, id):
    donation = get_object_or_404(Donation, id=id, donor=request.user)
    if request.method == 'POST':
        donation.delete()
        return redirect('donor_dashboard')
    return render(request, 'delete_donation.html', {'donation': donation})

@login_required
def receiver_dashboard(request):
    donations = Donation.objects.select_related('donor').all()
    
    for d in donations:
        d.donor_profile = Donor.objects.filter(user=d.donor).first()

    return render(request, 'receiver_dashboard.html', {'donations': donations})


@login_required
def request_food(request, id):
    donation = get_object_or_404(Donation, id=id)

    if request.user.user_type != "receiver":
        messages.error(request, "Only receivers can request food.")
        return redirect("home")

    if request.method == "POST":
        message = request.POST.get("message", "")
        Request.objects.create(
            donation=donation,
            requester=request.user,
            message=message
        )
        donation.status = "Requested"
        donation.save()

        messages.success(request, "Food request submitted successfully.")
        return redirect("receiver_dashboard")

    return redirect("home")



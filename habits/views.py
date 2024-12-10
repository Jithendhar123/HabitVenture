from django.shortcuts import render, redirect, get_object_or_404
from . forms import RegisterationForm, HabitCreation
from django.contrib import messages
from . models import Habit
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User

# Create your views here
def completed_habits_graph(request):
    completed_habits = Habit.objects.filter(author=request.user, is_completed=True).count()
    incomplete_habits = Habit.objects.filter(author=request.user, is_completed=False).count()

    labels=[
        "Completed", "Incomplete"
    ]
    data=[
        completed_habits, incomplete_habits
    ]

    fig,ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, colors=['green', 'yellow'])
    ax.axis('equal')
    plot = io.BytesIO()
    plt.savefig(plot, format='png')
    plot.seek(0)

    return HttpResponse(plot.getvalue(), content_type='image/png')

#User Registration and account features
def register(request):
    if request.method == "POST":
        form = RegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account Created {username}")
            return redirect('login')
    else:
        form = RegisterationForm()
    return render(request, 'accounts/register.html', {"form": form})

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

#Habits functionality
@login_required
def complete_habit(request, id):
    habit = get_object_or_404(Habit, id=id, author=request.user)
    habit.is_completed = True
    habit.save()
    # HabitCompletion.objects.create(habit=habit, date_completed=date.today())
    # if not HabitCompletion.objects.filter(habit=habit, user=user, completed_on=date.today()).exists():
    #     HabitCompletion.objects.create(habit=habit, user=user)
    return redirect('dashboard')

@login_required
def create_habit(request):
    print("Request Method:", request.method)
    if request.method == "POST":
        form = HabitCreation(request.POST)
        print("Form valid:", form.is_valid())
        if form.is_valid():
            habit = form.save(commit=False)
            habit.author = request.user
            habit.save()
            return redirect('dashboard')
        else:
            # form = HabitCreation()
            print("Form errors: ", form.errors)
            return render(request, 'accounts/create_habit.html', {'form':form})
    else:
        form = HabitCreation()
    return render(request, 'accounts/create_habit.html', {'form':form})

@login_required
def dashboard(request):
    habits = Habit.objects.filter(author=request.user, is_completed=False)
    return render(request, 'accounts/dashboard.html', {'habits':habits})

@login_required
def habits_list(request):
    habits = Habit.objects.filter(author=request.user)
    return render(request, 'accounts/habit_list.html', {'habits': habits})

@login_required
def update_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, author=request.user)
    if request.method=='POST':
        form = HabitCreation(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, "Habit updated successfully")
            return redirect('dashboard')
    else:
        form = HabitCreation(instance=Habit)
    return render(request,'accounts/habit_form.html', {'form':form})

@login_required
def delete_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, author=request.user)
    if request.method == 'POST':
        habit.delete()
        messages.success(request, "Habit deleted!")
        return redirect('dashboard')
    return render(request, 'accounts/habit_delete.html', {'habit': habit})


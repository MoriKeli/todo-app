from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from todo_app.forms import *
from todo_app.models import *
from datetime import datetime
from django.utils.safestring import mark_safe    # modules to display calendar
from calendar import HTMLCalendar
import calendar

def index_page(request):
    return render(request, 'users/index.html')

class UserLogin(LoginView):
    template_name = 'users/login.html'

def create_user_account(request):
    signup_form = UserSignUpForm()
    if request.method == 'POST':
        signup_form = UserSignUpForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.username = user.username
            user.save()

            messages.success(request, f'{user.username} created account successfully!')
            return redirect('edit_profile')

    return render(request, 'users/register.html', {'signup_form': signup_form})

# class CalendarView(generic.ListView):
#     model = Tasks
#     template_name = 'users/calendar.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # use today's date for the calendar
#         d = get_date(self.request.GET.get('day', None))

#         # Instantiate calendar class with today's year & date
#         cal = Calendar(d.year, d.month)
#         # call format_month method from utils.py which displays calendar as a table
#         html_cal = cal.formatmonth(withyear=True)
#         context['calendar'] = mark_safe(html_cal)
#         return context

# def get_date(req_day):
#     if req_day:
#         year, month = (int(x) for x in req_day.split('-'))
#         return date(year, month, day=1)
#     return datetime.today()


@login_required(login_url='login')
def user_homepage(request):
    scheduletask_form = ScheduleTaskForm()
    if request.method == 'POST':
        scheduletask_form = ScheduleTaskForm(request.POST)
        if scheduletask_form.is_valid():
            user = scheduletask_form.save(commit=False)
            user.rel = request.user
            user.date_due = str(user.date_due)[:19]
            user.task = str(user.task).capitalize()
            if Tasks.objects.filter(rel=user.rel, date_due=user.date_due).exists():
                messages.error(request, 'This task overlaps with an/or existing task(s). Kindly include or adjust time for this scheduled task.') 
            if str(datetime.today().strftime("%Y-%m-%d %H:%M:%S")) > str(user.date_due):
                messages.error(request, f'You have entered a past date! Current date: {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}; date_due: {user.date_due}')
            else:
                user.save()
                messages.success(request, "Task scheduled successfully")
                return redirect('homepage')

    scheduled_tasks = Tasks.objects.filter(rel=request.user, task_completed=False).all()
    current_date = datetime.today()

    # calendar
    fetch_month = list(calendar.month_name)[current_date.month]
    cal = HTMLCalendar(6).formatmonth(current_date.year, current_date.month, withyear=False)
    HTMLCalendar()

    context = {'schedule_form': scheduletask_form, 'scheduled_tasks': scheduled_tasks,
     'tasks_pending': scheduled_tasks.count(), 'tasks_completed': Tasks.objects.filter(rel=request.user, task_completed=True).count(),
     'outdated': Tasks.objects.filter(rel=request.user, date_due__lt=current_date, task_completed=False).count(),
     'today': current_date, 'calendar': mark_safe(cal),
     }
    return render(request, 'users/homepage.html', context)

@login_required(login_url='login')
def completed_tasks(request):
    c_tasks = Tasks.objects.filter(rel=request.user, task_completed=True).all()

    return render(request, 'users/completed.html', {'tasks': c_tasks})

@login_required(login_url='login')
def pending_tasks(request):
    p_tasks = Tasks.objects.filter(rel=request.user, task_completed=False).all()

    return render(request, 'users/pending.html', {'tasks': p_tasks})

@login_required(login_url='login')
def outdated_tasks(request):
    outd_tasks = Tasks.objects.filter(rel=request.user, task_completed=False, date_due__lt=datetime.today()).all()

    return render(request, 'users/outdated.html', {'outdatedTasks': outd_tasks})


@login_required(login_url='login')
def mark_as_complete(request, pk):
    obj_id = Tasks.objects.get(id=pk)
    form = MarkTaskasCompleteForm(instance=obj_id)
    if request.method == 'POST':
        form = MarkTaskasCompleteForm(request.POST, instance=obj_id)
        if form.is_valid():
            scheduled_task = form.save(commit=False)
            scheduled_task.task = scheduled_task.task
            scheduled_task.save()
            messages.success(request, f'{scheduled_task.task} marked as completed')
            return redirect('tasks_completed')
    return render(request, 'users/complete-form.html', {'form': form, 'obj': obj_id})

@login_required(login_url='login')
def user_profile_page(request):
    editprofile_form = EditProfileForm(instance=request.user)
    additionalinfo_form = EditAdditionalProfileInfo(instance=request.user.profile)
    changedp_form = ChangeDpForm(instance=request.user.profile)

    if request.method == 'POST':
        editprofile_form = EditProfileForm(request.POST, instance=request.user)
        additionalinfo_form = EditAdditionalProfileInfo(request.POST, instance=request.user.profile)
        changedp_form = ChangeDpForm(request.POST, request.FILES, instance=request.user.profile)

        if editprofile_form.is_valid() and additionalinfo_form.is_valid():
            editprofile_form.save()
            additionalinfo_form.save()
            
            messages.success(request, "Profile updated successfully!")
            return redirect('edit_profile')
    
        if changedp_form.is_valid():
            changedp_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('edit_profile')

    context = {'dp_form': changedp_form, 'profile_form': editprofile_form, 'add_info_form': additionalinfo_form}
    return render(request, 'users/profile.html', context)

@login_required(login_url='login')
def edit_scheduledTask(request, pk):
    task_id = Tasks.objects.get(id=pk)
    edit_form = ScheduleTaskForm(instance=task_id)

    if request.method == "POST":
        edit_form = ScheduleTaskForm(request.POST, instance=task_id)
        if edit_form.is_valid():
            form = edit_form.save(commit=False)
            form.rel = request.user
            form.date_due = str(form.date_due)[:19]

            if Tasks.objects.filter(rel=form.rel, date_due=form.date_due).exists():
                messages.error(request, 'This task overlaps with an/or existing task(s). Kindly include or adjust time for this scheduled task.') 
            if str(datetime.today().strftime("%Y-%m-%d %H:%M:%S")) > str(form.date_due):
                messages.error(request, f'You have entered a past date! Current date: {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}; date_due: {form.date_due}')
            else:
                edit_form.save()
                messages.info(request, "Scheduled task edited successfully!")
                return redirect('homepage')

    return render(request, 'users/edit.html', {'edit_form': edit_form, 'obj': task_id})


@login_required(login_url='login')
def delete_scheduledtask(request, pk):
    obj = Tasks.objects.get(id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('homepage')

    return render(request, 'users/delete.html', {'delete': obj})


class LogoutUser(LogoutView):
    template_name = 'users/logout.html'
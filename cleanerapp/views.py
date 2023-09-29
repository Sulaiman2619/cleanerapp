from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from .decorators import cleaner_required, staff_required
from django.http import  JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core.paginator import Paginator
from django.db.utils import IntegrityError
import json
from django.contrib import messages
from django.contrib.auth import authenticate





User = get_user_model()

# In your views or a script
#days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'พฤหัสบดี', 'Friday', 'Saturday', 'Sunday']

#current_day_of_week = datetime.now().strftime('%A')

# Check if the current day is in the list of days_of_week
#if current_day_of_week in days_of_week:
    # Do something based on the current day
    #print(f'Today is {current_day_of_week}')
#else:
    #print('Invalid day')

# Get the current day of the week as an integer (0 for Monday, 1 for Tuesday, etc.)


# Get the DayOfWeek instance for the current day
# day_instance = Work.objects.get(day=current_day_of_week)

class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            
            # Check if the user is a cleaner
            if Cleaner.objects.filter(user=user).exists():
                if user.check_password(password):
                    return user
            
            # Check if the user is a staff member
            if Staff.objects.filter(user=user).exists():
                if user.check_password(password):
                    return user

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

def login_view(request):
    if request.user.is_authenticated:
        # Check if the user is already authenticated (logged in)
        if Cleaner.objects.filter(user=request.user).exists():
            return redirect('cleaner_works')  # Redirect to the cleaner's works view
        elif Staff.objects.filter(user=request.user).exists():
            return redirect('staff_works')  # Redirect to the staff member's works view

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if Cleaner.objects.filter(user=user).exists():
                return redirect('cleaner_works')  # Redirect to the cleaner's works view
            elif Staff.objects.filter(user=user).exists():
                return redirect('staff_works')  # Redirect to the staff member's works view
        else:
            messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

    return render(request, 'login.html')

# Rest of your views and URLs


@login_required
@cleaner_required
def cleaner_works(request):
    # Assuming you have the username of the currently logged-in user
    username = request.user.username

    # Get the User object
    user = get_object_or_404(User, username=username)

    # Use the User object to get the corresponding Cleaner
    cleaner = get_object_or_404(Cleaner, user=user)
    
    current_day_of_week = datetime.now().strftime('%A')
    works_data = Work.objects.filter(day=current_day_of_week, cleaner=cleaner)
    
    building_choices = Building.objects.all()
    floor_choices = Room.objects.values_list('floor_num', flat=True).distinct().order_by('floor_num')
    room_choices = Room.objects.values_list('room_name', flat=True).distinct().order_by('room_name')
    
    building_query = request.GET.get('building')
    room_query = request.GET.get('room')
    floor_query = request.GET.get('floor')
    
    if building_query:
        works_data = works_data.filter(room__building__name=building_query)
    if room_query:
        works_data = works_data.filter(room__room_name=room_query)
    if floor_query:
        works_data = works_data.filter(room__floor_num=floor_query)
    

    if request.method == 'POST':
        work_id = request.POST.get('work_id')
        status = request.POST.get('status')

        try:
            work = Work.objects.get(pk=work_id)
            works_data, created = WorksData.objects.get_or_create(work=work, date=datetime.today())
            
            # Update the status for the work item here
            works_data.status = status
            works_data.save()

            return redirect('cleaner_works')

        except Work.DoesNotExist:
            return HttpResponse("Work not found.")

    context = {
        'works_data': works_data,
        'building_choices': building_choices,
        'floor_choices': floor_choices,
        'room_choices': room_choices
        # Include status for each workitem in the context
    }

    return render(request, 'cleaner.html', context)
    
   
@login_required
@staff_required
def staff_works(request):
    # Retrieve all works data for staff members
    current_day_of_week = datetime.now().strftime('%A')
    works_data = Work.objects.filter(day=current_day_of_week)
    building_choices = Building.objects.all()
    floor_choices = Room.objects.values_list('floor_num', flat=True).distinct().order_by('floor_num')
    room_choices = Room.objects.values_list('room_name', flat=True).distinct().order_by('room_name')
    status_choices = (
                        ('กำลังทำงาน', 'กำลังทำงาน'),
                        ('เสร็จสิ้น', 'เสร็จสิ้น'),
                        ('งานยังไม่เรียบร้อย', 'งานยังไม่เรียบร้อย'), )
    cleaner_choices = Cleaner.objects.values_list('user__first_name', flat=True).distinct().order_by('user__first_name')
    checker_choices = Checker.objects.all()
    building_query = request.GET.get('building')
    room_query = request.GET.get('room')
    floor_query = request.GET.get('floor')
    cleaner_query = request.GET.get('cleaner')
    status_query = request.GET.get('status')

    
    if building_query:
        works_data = works_data.filter(room__building__name=building_query)
    if room_query:
        works_data = works_data.filter(room__room_name=room_query)
    if floor_query:
        works_data = works_data.filter(room__floor_num=floor_query)
    if cleaner_query:
        works_data = works_data.filter(cleaner__user__first_name=cleaner_query)
    if status_query:
        works_data = works_data.filter(worksdata__status=status_query)


    context = {
        'works_data': works_data,
        'building_choices': building_choices,
        'floor_choices': floor_choices,
        'room_choices': room_choices,
        'status_choices': status_choices,
        'cleaner_choices': cleaner_choices,
        'checker_choices':checker_choices,
    }

    return render(request, 'staff.html', context)


def setting_works(request):
    works_data = Work.objects.all()
    building_choices = Building.objects.all()
    day_choices = Work.objects.values_list('day', flat=True).distinct().order_by('day')
    floor_choices = Room.objects.values_list('floor_num', flat=True).distinct().order_by('floor_num')
    room_choices = Work.objects.values_list('room__room_name', flat=True).distinct().order_by('room__room_name')
    cleaner_choices = Cleaner.objects.values_list('user__first_name', flat=True).distinct().order_by('user__first_name')
    building_query = request.GET.get('building')
    room_query = request.GET.get('room')
    floor_query = request.GET.get('floor')
    cleaner_query = request.GET.get('cleaner')
    day_query = request.GET.get('day')

    if day_query:
        works_data = works_data.filter(day=day_query)
    if building_query:
        works_data = works_data.filter(room__building__name=building_query)
    if room_query:
        works_data = works_data.filter(room__room_name=room_query)
    if floor_query:
        works_data = works_data.filter(room__floor_num=floor_query)
    if cleaner_query:
        works_data = works_data.filter(cleaner__user__first_name=cleaner_query)

        

    context ={
        'works_data': works_data,
        'building_choices': building_choices,
        'floor_choices': floor_choices,
        'room_choices': room_choices,
        'cleaner_choices': cleaner_choices,
        'day_choices' : day_choices
    }
    return render(request, 'setting.html', context)


@csrf_exempt
def update_status(request, work_id, status):
    try:
        # Retrieve the work object with the given work_id
        work = get_object_or_404(Work, pk=work_id)
        works_data, created = WorksData.objects.get_or_create(work=work, date=datetime.today())
        # Check the status parameter and update the work status accordingly
        if status == 'เสร็จสิ้น':
            works_data.status = 'เสร็จสิ้น'
        elif status == 'กำลังทำงาน':
            works_data.status = 'กำลังทำงาน'
        else:
            # Handle the case where the status parameter is not recognized
            response_data = {'message': 'Invalid status parameter'}
            return JsonResponse(response_data)

        works_data.status = status
        works_data.comment = "ยังไม่มีคอมเม้นต์ใดๆ"
        works_data.staff = "ยังไม่มีผู้ตรวจ"
        works_data.save()
        
        response_data = {'message': 'Status updated successfully', 'work_id': work.id}
        return JsonResponse(response_data)

    except Work.DoesNotExist:
        # Handle the case where the work with the given ID does not exist
        response_data = {'message': 'Work not found'}
        return JsonResponse(response_data, status=404)
    

def reset_status(request, work_id,status):
    try:
        # Retrieve the work object with the given work_id
        work = get_object_or_404(Work, pk=work_id)
        works_data, created = WorksData.objects.get_or_create(work=work, date=datetime.today())
        # Check the status parameter and update the work status accordingly
        if status == 'เสร็จสิ้น':
            works_data.status = 'เสร็จสิ้น'
        elif status == 'งานยังไม่เรียบร้อย':
            works_data.status = 'งานยังไม่เรียบร้อย'
        else:
            # Handle the case where the status parameter is not recognized
            response_data = {'message': 'Invalid status parameter'}
            return JsonResponse(response_data)

        works_data.status = status
        works_data.save()
        
        response_data = {'message': 'Status updated successfully', 'work_id': work.id}
        return JsonResponse(response_data)

    except Work.DoesNotExist:
        # Handle the case where the work with the given ID does not exist
        response_data = {'message': 'Work not found'}
        return JsonResponse(response_data, status=404)

@login_required
@staff_required   
def edit_work(request, work_id):
    # Retrieve the work item to be edited
    work = get_object_or_404(Work, pk=work_id)

    if request.method == 'POST':
        # Get the selected cleaner (user) from the form
        selected_cleaner_id = request.POST.get('cleaner')
        selected_cleaner = get_object_or_404(Cleaner, pk=selected_cleaner_id)

        # Use a transaction to handle database updates
        try:
            with transaction.atomic():
                # Check if a work item with the same combination exists
                existing_work = Work.objects.filter(
                    work_name=work.work_name,
                    cleaner=selected_cleaner,
                    room=work.room,
                    day=work.day
                ).exclude(id=work_id).first()

                if existing_work:
                    # If a work item with the same combination exists, update its cleaner
                    existing_work.cleaner = selected_cleaner
                    existing_work.save()
                else:
                    # If not, update the original work item's cleaner
                    work.cleaner = selected_cleaner
                    work.save()

            # Redirect back to the staff works view or any other appropriate page
            return redirect('setting_works')

        except IntegrityError as e:
            # Log the exception for debugging purposes
            print(f"IntegrityError: {e}")

            # Handle the error gracefully or redirect to an error page
            # You can customize this part based on your application's requirements
            return render(request, 'error.html', {'error_message': 'Database integrity error'})

    # Get all available cleaners (users)
    cleaners = Cleaner.objects.all()

    context = {
        'work': work,
        'cleaners': cleaners,
    }

    return render(request, 'edit_work.html', context)

@login_required
@staff_required
def delete_work(request, work_id):
    # Retrieve the work item to be deleted
    work = get_object_or_404(Work, pk=work_id)

    if request.method == 'POST':
        # Delete the work item
        work.delete()
        # Redirect back to the staff works view or any other appropriate page
        return redirect('setting_works')

    context = {
        'work': work,
    }

    return render(request, 'delete_work.html', context)

@login_required
@staff_required
def add_work(request):
    if request.method == 'POST':
        # Retrieve form data
        work_name = request.POST.get('work_name')
        work_cleaner_id = request.POST.get('work_cleaner')
        work_day = request.POST.get('work_day')
        # Get the selected room ID from the form
        room_id = request.POST.get('work_room')

        # Fetch the room data associated with the selected room ID
        selected_room = Room.objects.get(pk=room_id)

        # Create a new work item in the database
        new_work = Work.objects.create(
            work_name=work_name,
            cleaner_id=work_cleaner_id,
            day=work_day,
            room=selected_room,  # Assign the selected room
            # Add other fields as needed
        )

        # Redirect back to the staff works view or any other appropriate page
        return redirect('setting_works')

    # Get all available cleaners (users)
    cleaners = Cleaner.objects.all()

    # Query all rooms from the Room model
    rooms = Room.objects.all()

    context = {
        'cleaners': cleaners,
        'rooms': rooms,
    }

    return render(request, 'add_work.html', context)



@login_required
@staff_required
def get_workdata_history(request):
    # Retrieve all WorksData
    workdata_history = WorksData.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    cleaner_query = request.GET.get('cleaner')
    cleaner_choices = Cleaner.objects.values_list('user__first_name', flat=True).distinct().order_by('user__first_name')

    # Convert start_date and end_date to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
    end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None


    if start_date:
        workdata_history = workdata_history.filter(date__gte=start_date)
    
    if end_date:
        workdata_history = workdata_history.filter(date__lte=end_date)
    
    if cleaner_query:
        workdata_history = workdata_history.filter(work__cleaner__user__first_name=cleaner_query)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Number of items to display per page (you can customize this)
    items_per_page = request.GET.get('items_per_page', 10)  # Default to 10 items per page

    # Create a Paginator instance
    paginator = Paginator(workdata_history, items_per_page)

    # Get the current page's data
    page_data = paginator.get_page(page_number)

    # Pass the data to the template
    context = {
        'workdata_history': page_data,
        'cleaner_choices' : cleaner_choices,
        'start_date' : start_date,
        'end_date' : end_date,
        'items_per_page': items_per_page,
    }

    return render(request, 'work_history.html', context)





@csrf_exempt
def submit_verification(request, work_id):
    try:
        print("In submit_verification")
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))  # Ensure the request body is decoded to a string
            staff = data.get('staff')
            rating = data.get('rating')
            comment = data.get('comment')

            work = get_object_or_404(Work, pk=work_id)

            # Check if a WorksData record with the same work_id already exists
            works_data, created = WorksData.objects.get_or_create(work=work)

            # Update the existing or newly created record
            works_data.staff = staff
            works_data.status = 'ประเมินเรียบร้อย'
            works_data.rating = rating
            works_data.comment = comment
            works_data.date = datetime.today()
            works_data.save()

            print("Evaluation saved successfully")
            return redirect('staff_works')  # If you want to pass arguments, use reverse()
        else:
            print("Invalid request method")
            return JsonResponse({'message': 'Invalid request method'}, status=400)
    except Exception as e:
        print(f"An error occurred: {e}")
        return JsonResponse({'message': f'An error occurred: {e}'}, status=500)


    



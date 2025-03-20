from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser, Problem, Solution
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import logout as auth_logout
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@csrf_exempt
def contact_us(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        
        subject = f"New Contact Us Message from {name}"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        
        try:
            send_mail(subject, body, email, ["innoskill01@gmail.com"])
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, "Failed to send message. Please try again later.")
            print("Email error:", e)

        return redirect("landing_page")  # Replace with the actual name of your landing page view
    
    return render(request, "landing_page.html")



def landing_page(request):
    # template = loader.get_template('landing_page.html')
    # return HttpResponse(template.render())
    return render(request, 'landing_page.html')

def login_page(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def register_page(request):
    template = loader.get_template('register.html')
    return HttpResponse(template.render())

@csrf_exempt
def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re-password')
        profile_picture = request.FILES.get('profile_picture')
        user_type = request.POST.get('user_type')
        organization_verification = request.FILES.get('organization_verification') if user_type == 'organizer' else None

        if password != re_password:
            messages.error(request, "Passwords don't match. Please try again.")
            return render(request, 'register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return render(request, 'register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username is already registered!")
            return render(request, 'register.html')

        hashed_password = make_password(password)

        user = CustomUser(
            name=name,
            username=username,
            email=email,
            password=hashed_password,
            profile_picture=profile_picture,
            user_type=user_type,
            organization_verification=organization_verification,
            status='pending' if user_type == 'organizer' else 'approved',
        )
        user.save()

        messages.success(request, "Registration successful! Your account will be reviewed by the admin.")
        return redirect('login_page')

    return render(request, 'register.html')


from django.contrib.auth import authenticate, login

from django.contrib import messages

@csrf_exempt
def submit(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Attempting login for {username}")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(f"Session Data: {request.session.items()}")
            print(f"User {user.username} is authenticated: {user.is_authenticated}")  # Debugging print
            request.session['user_id'] = user.id  # Manually store session data

            # Redirect based on user type
            if user.user_type == 'organizer':
                return redirect('/organizer/')  # Redirect to organizer page
            else:
                return redirect('/user/')  # Redirect to user page
        else:
            print("Authentication failed!")
            messages.error(request, "Invalid credentials.")

    return render(request, 'login.html')


@login_required
def user(request):
    username = request.user.username
    user_problems = Problem.objects.filter(user__username=username)

    # Fetch problems excluding the user's own problems and prefetch solutions
    problems = Problem.objects.exclude(user__username=username).select_related('user').prefetch_related('solutions')

    print(f"User in session: {request.user}, Authenticated: {request.user.is_authenticated}")

    return render(request, 'user.html', {
        'username': username,
        'problems': problems,
    })



@login_required
def organizer_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated
    
    if request.user.user_type != 'organizer':
        return redirect('user_dashboard')  # Redirect normal users to their page
    
    problems = Problem.objects.all().order_by('-created_at')  # Fetch all problems, sorted by latest
    return render(request, 'organizer.html', {'problems': problems})

@csrf_exempt
def post(request):
    if not request.user.is_authenticated:  # Ensure user is logged in
        return JsonResponse({'status': 'error', 'message': 'User not authenticated. Please log in again.'}, status=401)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        post = Problem(user=request.user, title=title, description=description, created_at=timezone.now())
        post.save()

        messages.success(request, "Problem posted successfully!")
        return redirect('user')

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def logout(request):
    request.session.flush()
    messages.success(request, "Logged out successfully!")
    return redirect('login_page')

from django.contrib.auth.decorators import login_required

@login_required
def my_problems(request):
    if request.user.is_authenticated:
        # Fetch problems created by the authenticated user
        user_problems = Problem.objects.filter(user=request.user).prefetch_related('solutions')

        # Create a dictionary mapping each problem to its solutions
        problems_with_solutions = []
        for problem in user_problems:
            problems_with_solutions.append({
                'problem': problem,
                'solutions': problem.solutions.all()
            })

        return render(request, 'my_problems.html', {'problems_with_solutions': problems_with_solutions})
    else:
        return redirect('login') # Ensure 'login' is the name of your login page URL


@login_required
def edit_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)

    if request.user != problem.user:
        return HttpResponse("You are not authorized to edit this problem.", status=403)

    if request.method == "POST":
        problem.title = request.POST.get("title")
        problem.description = request.POST.get("description")
        problem.status = request.POST.get("status")
        problem.save()
        return redirect("my_problems")

    return render(request, "edit_problem.html", {"problem": problem})


@login_required
def delete_problem(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id, user=request.user)
    problem.delete()
    return redirect('my_problems')

@login_required
def submit_solution(request):
    if request.user.user_type == 'organizer':  # Only allow organizers
        if request.method == 'POST':
            problem_id = request.POST.get('problem_id')
            solution_text = request.POST.get('solution')

            problem = Problem.objects.get(id=problem_id)
            solution = Solution.objects.create(
                solution_text=solution_text,
                problem=problem,
                organizer=request.user
            )
            return redirect('organizer_dashboard')  # Redirect to the organizer dashboard or wherever you want
    else:
        return redirect('login')  # Redirect non-organizers to the login page




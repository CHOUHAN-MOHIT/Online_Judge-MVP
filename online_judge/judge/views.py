from time import sleep
from django.http import HttpResponse, HttpResponseRedirect , JsonResponse
from django.contrib.auth import authenticate , login , logout
from django.shortcuts import get_object_or_404, render
from judge.models import Problem, Solution, Test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files import File
from . import helper
import json
import subprocess

# Create your views here.
def index(request):
    return render(request , 'index.html')

def problems(request):
    problems = Problem.objects.all()
    return render(request , 'problems.html' , { 'problems' : problems})

def problem(request , problem_id):
    if request.user.is_authenticated :
        problem = get_object_or_404(Problem , pk=problem_id)
        context = {
            'problemId':problem_id,
            'problem':problem
        }
        return render(request, 'problem.html', context)
    else:
        messages.success(request , "Please login to solve problems!!", extra_tags='alert alert-info')
        return HttpResponseRedirect('/login')
    

def submit(request , pid):
    problem = Problem.objects.get(pk=pid)
    test = Test.objects.get(problem__problem_name=problem.problem_name)
    if request.method == 'POST':
        # Get the data from the POST request
        data = json.loads(request.body)
        usercode = data['code']

        # Process the data
        byte_content = usercode.encode()
        with open('temp.cpp' , 'wb+') as temp_code:
            temp_code.write(byte_content)
        temp_code.close()
        expout = open('exp_out.txt' , 'w')
        output = open('output.txt' , 'w')
        expout.write(test.test_output)
        input = bytes(test.test_input , 'utf-8')
        verdict = helper.runcode(input, output)
        expout.close()
        verdict = helper.get_verdict()


        # Send the result back to the client
        response_data = {'result': verdict}
        return HttpResponse(json.dumps(response_data), content_type='application/json')

    



def result(request , status):
    context = {
        'status':status
    }
    return render(request ,'submit.html' , context)

def submissions(request):
    submissions = Solution.objects.all().order_by('-id')[:10]
    return render(request,'submissions.html' , {'submissions' : submissions})



def register_request(request):
    return render(request , 'register.html')


def register_verify(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            username = request.POST['username']
            firstname = request.POST['firstname']
            password = request.POST['password1']
            email = request.POST['email']

            new_user = User.objects.create_user(username , email, password)
            new_user.first_name = firstname
            new_user.save()
            messages.success(request , "Registration Successful", extra_tags='alert alert-success')
            return HttpResponseRedirect('/register/')
        else:
            messages.succes(request , "Both passsword should be same.", extra_tags='alert alert-danger')
            return HttpResponseRedirect('/register/')
    else:
        return HttpResponse("Usage: Post method is not used.")
        
def login_request(request):
    return render(request , 'login.html')

def login_check(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request , "Logged in successfully.", extra_tags='alert alert-success')
            return HttpResponseRedirect('/')
        else:
            messages.success(request , "Log in failed!! check username or password.", extra_tags='alert alert-danger')
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponse("Usage: Method used is not POST.")

def log_out(request):
    logout(request)
    messages.success(request , "Logout succesfully.", extra_tags='alert alert-success')
    return HttpResponseRedirect('/')
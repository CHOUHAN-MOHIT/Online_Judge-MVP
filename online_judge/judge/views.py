from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate , login , logout
from django.shortcuts import get_object_or_404, render
from judge.models import Problem, Solution, Test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files import File
from . import helper
import subprocess
import filecmp

# Create your views here.
def index(request):
    return render(request , 'index.html')

def problems(request):
    if request.user.is_authenticated :
        problems = Problem.objects.all()
        return render(request , 'problems.html' , { 'problems' : problems})
    else:
        messages.success(request , "Please login to solve problems!!", extra_tags='alert alert-info')
        return HttpResponseRedirect('/login')

def problem(request , problem_id):
    if request.user.is_authenticated :
        problem = get_object_or_404(Problem , pk=problem_id)
        context = {
            'problem':problem
        }
        return render(request, 'problem.html', context)
    else:
        messages.success(request , "Please login to solve problems!!", extra_tags='alert alert-info')
        return HttpResponseRedirect('/login')
    

def submit(request , pid):
    # fetch problem object using pid and then test with problem_name
    problem = Problem.objects.get(pk=pid)
    test = Test.objects.get(problem__problem_name=problem.problem_name)
    # checking method
    if request.method == 'POST':
        # fetching file and code submitted by user
        user_codefile = request.FILES.get('codeFile', False)
        codeInEditor = request.POST.get('codeEditor', False)
        if user_codefile:
            codefile_content = user_codefile.read()
            with open('temp.cpp' , 'wb+') as temp_code:
                temp_code.write(codefile_content)
            temp_code.close()
            # inputfile = 'media/' + test.test_input.url
            out_container = open('mohit.txt' , 'w')
            testout = 'media/' + test.test_output.url
            helper.get_verdict('temp.cpp' , test.test_input)
            # subprocess.call(["g++","temp.cpp","-o","temp.exe"],shell=True)
            # k = subprocess.call(['temp.exe'],stdin=test.test_input ,stdout=out_container,shell=True)
            out_container.close()
            if k:
                return HttpResponse(k.stdout)
            else:
                result = filecmp.cmp('mohit.txt', testout, shallow=False)
                if result:
                    file =  open('temp.cpp')
                    myfile = File(file)
                    sol = Solution(
                        user = request.user,
                        problem=problem,
                        language=request.POST['language'],
                        code_file=myfile,
                        verdict='AC'
                    )
                    sol.save()
                    file.close()
                    return HttpResponseRedirect("/submit/correct_ans/")
                else:
                    file =  open('temp.cpp')
                    myfile = File(file)
                    sol = Solution(
                        user = request.user,
                        problem=problem,
                        language=request.POST['language'],
                        code_file=myfile,
                        verdict='WA'
                    )
                    sol.save()
                    file.close()
                    return HttpResponseRedirect("/submit/wrong_ans/")
        elif codeInEditor:
            
            byte_content = codeInEditor.encode()
            with open('temp.cpp' , 'wb+') as temp_code:
                temp_code.write(byte_content)
            temp_code.close()
            # inputfile = 'media/' + test.test_input.url
            out_container = open('mohit.txt' , 'w')
            testout = 'media/' + test.test_output.url
            k = helper.get_verdict('temp.cpp' , test.test_input.url)
            # subprocess.call(["g++","temp.cpp","-o","temp.exe"],shell=True)
            # k = subprocess.call(['temp.exe'],stdin=test.test_input ,stdout=out_container , stderr=out_container,shell=True)
            out_container.close()
            result = filecmp.cmp('output.txt', testout, shallow=False)
            print(result)
            if k :
                return HttpResponse('Internal error occur!!')
            else:
                result = filecmp.cmp('mohit.txt', testout, shallow=False)
                if result:
                    file =  open('temp.cpp')
                    myfile = File(file)
                    sol = Solution(
                        user = request.user,
                        problem=problem,
                        language=request.POST['language'],
                        code_file=myfile,
                        verdict='AC'
                    )
                    sol.save()
                    file.close()
                    return HttpResponseRedirect("/submit/correct_ans/")
                else:
                    file =  open('temp.cpp')
                    myfile = File(file)
                    sol = Solution(
                        user = request.user,
                        problem=problem,
                        language=request.POST['language'],
                        code_file=myfile,
                        verdict='WA'
                    )
                    sol.save()
                    file.close()
                    return HttpResponseRedirect("/submit/wrong_ans/")
            # return HttpResponse('Yep! I got your code')
        else:
            return HttpResponse('No code file uploaded!!')
    else:
        return HttpResponse('Usage: Post method is not used.')



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
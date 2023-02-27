from django.shortcuts import render , HttpResponse
from datetime import datetime
from .models import Contest , ContestProblem
import pytz
import json 
from django.core.files import File
from judge import helper
from judge.models import Test , Solution


# Create your views here.

def index(request):
    contests = Contest.objects.all()
    context = {
        'contests' : contests
    }
    return render(request, 'contestApp/index.html' , context)

def contest(request , contestId):
    contest = Contest.objects.get(pk=contestId)
    now = datetime.utcnow()
    now = pytz.UTC.localize(now)

    if now < contest.start_time:
        # Contest has not started yet
        return render(request, 'contestApp/contest_wait.html')
    elif now > contest.end_time:
        # Contest has ended
        return render(request, 'contestApp/contest_ended.html')
    else:
        # Contest is currently running
        contest = Contest.objects.get(id=contestId)
        problems = ContestProblem.objects.filter(contest=contest)
        context = {
            'contest':contest,
            'problems':problems
        }
        return render(request, 'contestApp/contest_running.html', context)
    
def contestSubmission(request , problemid):
    problem = ContestProblem.objects.get(pk=problemid)
    test = Test.objects.get(problem__problem_name=problem.problem_name)
    if request.method == 'POST':
        # Get the data from the POST request
        data = json.loads(request.body)
        usercode = data['code']

        # Process the usercode
        # copying the code to file
        byte_content = usercode.encode()
        with open('temp.cpp' , 'wb+') as temp_code:
            temp_code.write(byte_content)
        temp_code.close()
        # copying the input and output to file
        expout = open('exp_out.txt' , 'w')
        output = open('output.txt' , 'w')
        expout.write(test.test_output)
        input = bytes(test.test_input , 'utf-8')
        # getting verdict
        helper.runcode(input, output)
        expout.close()
        verdict = helper.get_verdict()

        sol = Solution(
            user = request.user,
            problem=problem,
            language="cpp",
            code_file=usercode,
            verdict=verdict
        )

        sol.save()



        # Send the result back to the client
        response_data = {'result': verdict}
        return HttpResponse(json.dumps(response_data), content_type='application/json')
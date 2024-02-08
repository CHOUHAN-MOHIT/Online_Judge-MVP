from django.shortcuts import render , HttpResponse
from datetime import datetime
from .models import Contest , ContestProblem , Scorecard
import pytz
import json 
from django.core.files import File
from judge import helper
import requests
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

    status = ''

    if now < contest.start_time:
        # Contest has not started yet
        status = 'not started'
        # return render(request, 'contestApp/contest_wait.html')
    elif now > contest.end_time:
        # Contest has ended
        status = 'ended'
        # return render(request, 'contestApp/contest_ended.html')
    else:
        # Contest is currently running
        status = 'running'
    contest = Contest.objects.get(id=contestId)
    problems = ContestProblem.objects.filter(contest=contest)
    context = {
        'status':status,
        'contest':contest,
        'problems':problems
    }
    return render(request, 'contestApp/contest_running.html', context)
    
def contestSubmission(request , problemid):
    if request.method == 'POST':
        problem = ContestProblem.objects.get(pk=problemid)
        test = Test.objects.get(problem__problem_name=problem.problem_name)
        # Get the data from the POST request
        data = json.loads(request.body)
        usercode = data['code']


        # code = '#include<bits/stdc++.h>\nusing namespace std;\nint main(){\ncout<<"hello world";\nreturn 0;}'
        url = "https://cpp-17-code-compiler.p.rapidapi.com/"

        payload = {
            'code': usercode,
            "version": "latest",
            'input': test.test_input,
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "3436a53daemsh72098474fa00240p1b912ajsn554169aa1c13",
            "X-RapidAPI-Host": "cpp-17-code-compiler.p.rapidapi.com"
        }
        response = requests.post(url, json=payload, headers=headers)

        verdict = ""
                            
        if response.status_code == 200:
            data = response.json()
            if not data['cpuTime']:
                verdict = 'CE'
        else:
            verdict = 'EX'

        if verdict == 'CE' or verdict == 'EX':
            response_data = {'result': verdict}
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        elif data['output'] == test.test_output:
            verdict = 'AC'
        else:
            verdict = 'WA'

        if verdict == 'AC':
            prevSol = Solution.objects.filter(user = request.user , problem = problem , verdict = 'AC')
            # print(prevSol)
            if not prevSol.exists():
                updatescore(request.user, problem)

        sol = Solution(
            user = request.user,
            problem=problem,
            language="c++",
            code_file=usercode,
            verdict=verdict
        )

        sol.save()

        # Send the result back to the client
        response_data = {'result': verdict}
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    
def updatescore(user, problem):
    obj = Scorecard.objects.filter(user = user)

    if obj.exists():
        toUpdate = Scorecard.objects.get(user = user)
        toUpdate.score = toUpdate.score+problem.points
        toUpdate.save()
        # print("final score:" , toUpdate.score , " + " , problem.points)
    else:
        scorecard = Scorecard(  
            user = user,
            score = problem.points
        )
        scorecard.save()
        # print("initial score:" , scorecard.score)

def leaderboard(request):
    leaderboard_list = Scorecard.objects.all().order_by("-score")
    # print(leaderboard_list)

    context = {
        'leaderboard_list':leaderboard_list
    }
    return render(request , 'contestApp/leaderboard.html' , context)
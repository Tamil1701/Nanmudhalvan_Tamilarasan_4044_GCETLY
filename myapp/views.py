
from django.shortcuts import render, get_object_or_404
from .models import Question, Option, Poll
from django.utils import timezone
from datetime import datetime

from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from datetime import datetime
import pytz
from pytz import timezone as timenewzone
def index(request):
    return render(request,'home.html')
def home(request):
    data={}
    data['questions']=Question.objects.all()
    for q in data['questions']:
        q.options=Option.objects.filter(question_id=q.question_id)
    return render(request,'home.html',data)
def create(request):
    data={}
    return render(request,'create.html')
def login(request):
    return render(request,'login.html')
def register(request):
    if request.method=='POST':
        ob=Userdetail()
        ob.username=request.POST['name']
        ob.email=request.POST['email']
        ob.password=request.POST['password']
        ob.save()
        return render(request,'login.html')
    return render(request,'register.html')
def vote(request,question_id):
    data={}
    data['question']=Question.objects.get(question_id=question_id)
    data['options']=Option.objects.filter(question_id=question_id)
    data['questionid']=question_id
    return render(request,'vote.html',data)
def result(request,question_id):
    totcnt=0
    winnerpoint=0
    winner=''
    data={}
    ques=Question.objects.get(question_id=question_id)
    result_date=ques.result_date
    ind_time = datetime.now(timenewzone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
    cur_date = datetime.strptime(ind_time, '%Y-%m-%d %H:%M:%S.%f')
    data['isShowResult']=False
    current_date = timezone.make_aware(cur_date, timezone.get_current_timezone())
    # cur_date = datetime(2024, 4, 11, 10, 27, 30)
    # current_date = pytz.utc.localize(cur_date)

    if current_date>result_date:
        data['isShowResult']=False
    else:
        data['result_date']=result_date
        data['isShowResult']=True
    data['question']=ques
    data['options']=Option.objects.filter(question_id=question_id)

    for i in data['options']:
        votecnt=Poll.objects.filter(question_id=question_id,option_id=i.option_id)
        optioncnt=len(votecnt)
        if winnerpoint<optioncnt:
            winnerpoint=optioncnt
            winner=i.option
        totcnt+=optioncnt
        i.cnt=optioncnt
    data['questionid']=question_id
    data['totalcount']=totcnt
    data['winner']=winner
    return render(request,'result.html',data)
# def result(request, question_id):
#     data = {}
#     try:
#         # Retrieve the question object based on question_id
#         ques = get_object_or_404(Question, question_id=question_id)

#         # Retrieve the result date from the question object
#         result_date = ques.result_date

#         # Get the current time in UTC (timezone-aware)
#         current_date = timezone.now()

#         # Check if the current time is before or on the result date
#         is_show_result = current_date <= result_date

#         # Populate data dictionary with necessary information
#         data['isShowResult'] = is_show_result
#         data['result_date'] = result_date
#         data['question'] = ques
#         data['options'] = Option.objects.filter(question_id=question_id)

#         # Calculate total counts and determine the winner
#         totcnt = 0
#         winnerpoint = 0
#         winner = ''

#         for option in data['options']:
#             votecnt = Poll.objects.filter(question_id=question_id, option_id=option.option_id).count()
#             option.cnt = votecnt
#             totcnt += votecnt

#             if votecnt > winnerpoint:
#                 winnerpoint = votecnt
#                 winner = option.option

#         data['questionid'] = question_id
#         data['totalcount'] = totcnt
#         data['winner'] = winner

#     except Question.DoesNotExist:
#         # Handle case where question_id does not exist
#         data['error_message'] = f"Question with ID {question_id} does not exist."

#     return render(request, 'result.html', data)
@csrf_exempt 
def saveuser(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            email=data['email']
            password=data['password']
            user=Userdetail.objects.get(email=email,password=password)
            return JsonResponse({'user_id':user.user_id})
        except Exception as e:
            return JsonResponse({'error':'error'})
        return JsonResponse({'msg':'Hello'})
    return JsonResponse({'msg':'Hello'})
@csrf_exempt 
def createpoll(request):
    if request.method=='POST':
        try:
            data=json.loads(request.body)
            question=data['question']
            options=data['options']
            dateTime=data['datetime']
            print(dateTime)
            datetime_obj = datetime.strptime(dateTime, '%Y-%m-%dT%H:%M')
            result_datetime= timezone.make_aware(datetime_obj, timezone.get_current_timezone())
            questionob=Question()
            questionob.question=question
            questionob.result_date=result_datetime
            questionob.save()
            quID=questionob.pk
            for i in options:
                if i!='':
                    optionob=Option()
                    optionob.option=i
                    optionob.question_id=questionob
                    optionob.save()
        except Exception as e:
            print('err',e)   
    return JsonResponse({'created':True})

@csrf_exempt 
def createpoll1(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question_text = data['question']
            options = data['options']
            datetime_str = data['datetime']
            print(type(datetime))
            # Parse datetime string to datetime object
            datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
            # result_datetime = timezone.make_aware(datetime_obj, timezone.utc)
            # question = Question.objects.create(question=question_text, result_date=result_datetime)
            # for option_text in options:
            #     if option_text.strip(): 
            #         Option.objects.create(option=option_text, question_id=question)
            
            return JsonResponse({'created': True})
        except Exception as e:
            print('Error:', e)
            return JsonResponse({'created': False, 'error': str(e)}, status=500)
    return JsonResponse({'created': False, 'error': 'Invalid request method'}, status=405)

@csrf_exempt 
def savevote(request):
    if request.method=='POST':
        try:
            data=json.loads(request.body)
            userid=int(data['user_id'])
            option=data['option']
            questionid=int(data['question'])
            existvote=Poll.objects.filter(question_id=questionid,user_id=userid)
            ques=Question.objects.get(question_id=questionid)
            result_date=ques.result_date
            ind_time = datetime.now(timenewzone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
            cur_date = datetime.strptime(ind_time, '%Y-%m-%d %H:%M:%S.%f')
            current_date = timezone.make_aware(cur_date, timezone.get_current_timezone())
            print(current_date,result_date)
            if current_date>result_date:
                return JsonResponse({'status':2})
            isAlreadyVote=False
            if len(existvote)!=0:
                isAlreadyVote=True
                return JsonResponse({'status':0})
            pollob=Poll()
            optionob=Option.objects.get(option_id=option)
            user=Userdetail.objects.get(user_id=userid)
            questionob=Question.objects.get(question_id=questionid)
            pollob.option_id=optionob
            pollob.user_id=user
            pollob.question_id=questionob
            pollob.save()
            return JsonResponse({'status':1})
        except Exception as e:
            print('err',e)
    return JsonResponse({'status':0})
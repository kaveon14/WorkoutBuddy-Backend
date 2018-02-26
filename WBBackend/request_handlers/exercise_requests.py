from django.http import JsonResponse
from django.http import HttpResponse
from WBBackend.models import DefaultExercise,CustomExercise,Profile
from django.views.decorators.csrf import csrf_exempt
import WBBackend.management.commands.populate_db as db
import json as json_module

# CSRF exemption is only temporary

@csrf_exempt
def getDefaultExercises(request):#need to check the request
    if request.method == 'GET':
        ex_arr = []
        ex_list = DefaultExercise.objects.order_by('exercise_name')
        for ex in ex_list:
            e = {'id':ex.id,'exercise_name':ex.exercise_name,
                 'exercise_description':ex.exercise_description,'exercise_image':ex.exercise_image.__str__()
                 ,'default_exercise': True}
            ex_arr.append(e)

        json = {'error':False,'message':'Request successfully completed',
                'RequestResponse':ex_arr}
        return JsonResponse(json)
    json = {'error':True,'message':'The http request needs to be "GET" not "POST" ','RequestResponse':None}
    return JsonResponse(json)

@csrf_exempt
def getDefaultExercise(request):
    if request.method == 'GET':
        ex = DefaultExercise.objects.get(id=request.GET['id'])
        e = {'id':ex.id,'exercise_name':ex.exercise_name,'exercise_description':ex.exercise_description,
             'exercise_image':ex.exercise_image.__str__(),'default_exercise': True}
        json = {'error':False,'message':'Request successfully completed','RequestResponse':e}
        return JsonResponse(json)
    json = {'error':True,'message':'The http request needs to be "GET" not "POST" ','RequestResponse':None}
    return JsonResponse(json)

@csrf_exempt
def getCustomExercise(request):
    if request.method == 'GET':
        ex = CustomExercise.objects.get(id=request.GET['id'])
        e = {'id':ex.id,'exercise_name':ex.exercise_name,'exercise_description':ex.exercise_description}
        i = ex.exercise_image.__str__()
        if i == 'static/WorkoutBuddy/ExerciseImages/default_exercise_image.png':
            e['exercise_image'] = ex.exercise_image.__str__()
        else:
            e['exercise_image'] = 'media/'+i
        json = {'error':False,'message':'Request successfully completed','RequestResponse':e}
        return JsonResponse(json)
    json = {'error':True,'message':'The http request needs to be "GET" not "POST" ','RequestResponse':None}
    return JsonResponse(json)

@csrf_exempt
def getCustomExercises(request):
    if request.method == 'POST':
        profileId = request.POST['profileId']
        user_profile = Profile.objects.get(id=profileId)
        ex_list = CustomExercise.objects.filter(user_profile=user_profile).order_by('exercise_name')
        ex_arr = []
        for ex in ex_list:
            e = {'id':ex.id,'exercise_name':ex.exercise_name,
                 'exercise_description':ex.exercise_description,'exercise_image':ex.exercise_image.__str__()}
            ex_arr.append(e)
        json = {'error':False,'message':'Request successfully completed','RequestResponse':ex_arr}
        return JsonResponse(json)
    json = {'error':True,'message':'The http request needs to be "GET" not "POST" ','RequestResponse':None}
    return JsonResponse(json)

@csrf_exempt
def getAllExercises(request):
    print(request.GET)
    if request.method == 'POST':
        defaultEx_list =  DefaultExercise.objects.order_by('exercise_name')
        profileId = request.POST['profileId']
        user_profile = Profile.objects.get(id=profileId)
        customEx_list =  CustomExercise.objects.filter(user_profile=user_profile).order_by('exercise_name')
        ex_arr = []
        for ex in defaultEx_list:
            e = {'id':ex.id,'exercise_name':ex.exercise_name,
                 'exercise_description':ex.exercise_description,'exercise_image':ex.exercise_image.__str__(),
                 'default_exercise':True}
            ex_arr.append(e)
        for ex in customEx_list:
            e = {'id':ex.id,'exercise_name':ex.exercise_name,
                 'exercise_description':ex.exercise_description,'exercise_image':ex.exercise_image.__str__(),
                 'default_exercise':False}
            ex_arr.append(e)
        json = {'error':False,'message':'Request successfully completed','RequestResponse':ex_arr}
        return JsonResponse(json)

    json = {'error':True,'message':'The http request needs to be "POST not "GET" ','RequestResponse':None}
    return JsonResponse(json)

@csrf_exempt
def createCustomExercise(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        json_data = json_module.loads(data)

        profile_id = json_data['profileId']
        user_profile = Profile.objects.get(id=profile_id) 
        exercise_name = json_data['exercise_name']
        exercise_description = json_data['exercise_description']
        custom_exercise = CustomExercise(user_profile=user_profile)
        custom_exercise.save()
        custom_exercise.exercise_name = exercise_name
        custom_exercise.exercise_description = exercise_description
        custom_exercise.exercise_image = db.getDefaultImagePath()
        custom_exercise.save()
        user_profile.custom_exercises.add(custom_exercise)
        user_profile.save()
        json = {'error':False,'message':'Request successfully completed','id':custom_exercise.id}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" '
        ,'RequestResponse':None}
    return JsonResponse(json)

@csrf_exempt
def updateCustomExercise(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        json_data = json_module.loads(data)
        exercise_name = json_data['exercise_name']
        exercise_description = json_data['exercise_description']
        custom_exercise = CustomExercise.objects.get(id=json_data['id'])
        custom_exercise.save()
        custom_exercise.exercise_name = exercise_name
        custom_exercise.exercise_description = exercise_description
        custom_exercise.save()
        json = {'error':False,'message':'Request successfully completed'
            ,'RequestResponse':None}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" '}
    return JsonResponse(json)

@csrf_exempt
def setCustomExerciseImage(request):
    if request.method == 'POST':
        if request.FILES != {}:
            custom_exercise = CustomExercise.objects.get(id=request.POST['id'])
            custom_exercise.exercise_image = request.FILES['file']
            custom_exercise.save()
            json = {'error':False,'message':'Request successfully completed','RequestResponse':'Custom Exercise Image Set!'}
            return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)

@csrf_exempt
def updateCustomExerciseImage(request):
    if request.method == 'POST':
        if request.FILES != {}:
            file = request.FILES['file']
            custom_exercise = CustomExercise.objects.get(id=request.POST['id'])
            user = custom_exercise.user_profile.user
            custom_exercise.exercise_image = file
            custom_exercise.save()
        else:# nothing gauranteed to work down there
            print('NO')
            file_path = request.POST['file_path']
            custom_exercise = CustomExercise.objects.get(id=request.POST['customExerciseId'])
            custom_exercise.exercise_image = file_path
            custom_exercise.save()

        json = {'error':False,'message':'Request successfully completed','RequestResponse':'Custom Exercise Image Changed!'}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)

@csrf_exempt#make sure to delete local image
def deleteCustomExercise(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        json_data = json_module.loads(data)
        profile_id = json_data['profileId']
        user_profile = Profile.objects.get(id=profile_id)
        custom_exercise = CustomExercise.objects.get(id=json_data['id'])
        custom_exercise.delete(keep_parents=False)
        user_profile.custom_exercises.remove(custom_exercise)
        user_profile.save()
        custom_exercise = None
        json = {'error':False,'message':'Request successfully completed','RequestResponse':None}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)

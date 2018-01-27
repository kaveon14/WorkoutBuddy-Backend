from django.http import JsonResponse
from django.http import HttpResponse
from WBBackend.models import DefaultExercise,CustomExercise,Profile

# IMAGES SHOULD BE LOADED FROM DIR
#use post if sending userID or profileID

def getDefaultExercises():#need to check the request
    if request.method == 'GET':
        ex_arr = []
        ex_list = DefaultExercise.objects.order_by('exercise_name')
        for ex in ex_list:
        e = {'id':ex.id,'exercise_name':ex.exercise_name,
             'exercise_description':ex.exercise_description,'exercise_image':ex.exercise_image.url}
        ex_arr.append(e)

        json = {'error':False,'message':'Request successfully completed',
                'RequestResponse':ex_arr}
        return JsonResponse(json)
    json = {'error':True,'message':'The http request needs to be "GET" not "POST" ','RequestResponse':None}
    return JsonResponse(json)

# should these below be GET ?
def getCustomExercises(request):
    if request.method == 'GET':
        user_profile = Profile.objects.get(user=request.user)#not going to work
        ex_list = CustomExercise.objects.filter(user_profile=user_profile).order_by('exercise_name')
        ex_arr = []
        for ex in ex_list:
            e = {'id':ex.id,'exercise_name':ex.exercise_name,
                 'exercise_description':ex.exercise_description,'exercise_image':ex.local_exercise_image.url}
            ex_arr.append(e)
        json = {'error':False,'message':'Request successfully completed','RequestResponse':ex_arr}
        return JsonResponse(json)
    json = {'error':True,'message':'The http request needs to be "GET" not "POST" ','RequestResponse':None}
    return JsonResponse(json)

def getAllExercises(request):
    if request.method == 'GET':
        defaultEx_list =  DefaultExercise.objects.order_by('exercise_name')
        user_profile = Profile.objects.get(user=request.user)#not going to work
        customEx_list =  CustomExercise.objects.filter(user_profile=user_profile).order_by('exercise_name')
        ex_arr = []
        for ex in defaultEx_list:
            e = {'id':ex.id,'exercise_name':ex.exercise_name,
                 'exercise_description':ex.exercise_description,'exercise_image':ex.exercise_image.url}
            ex_arr.append(e)
        for ex in customEx_list:
            e = {'id':ex.id,'exercise_name':ex.exercise_name,
                 'exercise_description':ex.exercise_description,'exercise_image':ex.local_exercise_image.url}
            ex_arr.append(e)
        json = {'error':False,'message':'Request successfully completed','RequestResponse':ex_arr}
        return JsonResponse(json)

    json = {'error':True,'message':'The http request needs to be "GET" not "POST" ','RequestResponse':None}
    return JsonResponse(json)

def createCustomExercise(request):
    if request.method == 'POST':
        profile_id = request['profile_id']
        user_profile = Profile.objects.get(id=Profile_id) 
        exercise_name = request['exercise_name']
        exercise_description = request['exercise_description']
        custom_exercise = CustomExercise(user_profile=user_profile)
        custom_exercise.save()
        custom_exercise.exercise_name = exercise_name
        custom_exercise.exercise_description = exercise_description
        custom_exercise.save()
        json = {'error':False,'message':'Request successfully completed','RequestResponse':None}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)

def updateCustomExercise(request):
    if request.method == 'POST':
        exercise_name = request['exercise_name']
        exercise_description = request['exercise_description'])
        custom_exercise = CustomExercise.objects.get(id=request['customExerciserId'])
        custom_exercise.save()
        custom_exercise.exercise_name = exercise_name
        custom_exercise.exercise_description = exercise_description
        custom_exercise.save()
        json = {'error':False,'message':'Request successfully completed','RequestResponse':None}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)

def updateCustomExerciseImage(request):#change, send the ce id
    if request.method == 'POST':
        custom_exercise = CustomExercise.objects.get(id=request['customExerciserId'])
        custom_exercise.exercise_image = request['file']
        custom_exercise.local_exercise_image = request['file']
        custom_exercise.save()
        json = {'error':False,'message':'Request successfully completed','RequestResponse':None}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)

def deleteCustomExercise(request):
    if request.method == 'POST':
        custom_exercise = CustomExercise.objects.get(id=request['customExerciserId'])
        custom_exercise.delete(using=DEFAULT_DB_ALIAS, keep_parents=False)
        custom_exercise = None
        json = {'error':False,'message':'Request successfully completed','RequestResponse':None}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)

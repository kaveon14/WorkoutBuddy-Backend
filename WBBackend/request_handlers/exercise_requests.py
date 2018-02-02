from django.http import JsonResponse
from django.http import HttpResponse
from WBBackend.models import DefaultExercise,CustomExercise,Profile
from django.views.decorators.csrf import csrf_exempt
import WBBackend.management.commands.populate_db as db
# CSRF exemption is only temporary
# create much better, dynamic error handling

# IMAGES SHOULD BE LOADED FROM DIR
#use post if sending userID or profileID

def getDefaultExercises(request):#need to check the request
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

@csrf_exempt
def getCustomExercises(request):
    if request.method == 'POST':
        profileId = request.POST['profileId']
        user_profile = Profile.objects.get(id=profileId)
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

@csrf_exempt
def getAllExercises(request):
    if request.method == 'POST':
        defaultEx_list =  DefaultExercise.objects.order_by('exercise_name')
        profileId = request.POST['profileId']
        user_profile = Profile.objects.get(id=profileId)
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

    json = {'error':True,'message':'The http request needs to be "POST not "GET" ','RequestResponse':None}
    return JsonResponse(json)

@csrf_exempt
def createCustomExercise(request):# need to set image to the default
    if request.method == 'POST':
        profile_id = request.POST['profileId']
        user_profile = Profile.objects.get(id=profile_id) 
        exercise_name = request.POST['exercise_name']
        exercise_description = request.POST['exercise_description']
        custom_exercise = CustomExercise(user_profile=user_profile)
        custom_exercise.save()
        custom_exercise.exercise_name = exercise_name
        custom_exercise.exercise_description = exercise_description
        custom_exercise.local_exercise_image = db.getDefaultImagePath()
        custom_exercise.save()
        user_profile.custom_exercises.add(custom_exercise)
        user_profile.save()
        json = {'error':False,'message':'Request successfully completed','RequestResponse':None}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)

@csrf_exempt
def updateCustomExercise(request):
    if request.method == 'POST':
        exercise_name = request.POST['exercise_name']
        exercise_description = request.POST['exercise_description']
        custom_exercise = CustomExercise.objects.get(id=request.POST['customExerciseId'])
        custom_exercise.save()
        custom_exercise.exercise_name = exercise_name
        custom_exercise.exercise_description = exercise_description
        custom_exercise.save()
        json = {'error':False,'message':'Request successfully completed','RequestResponse':None}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)

@csrf_exempt
def updateCustomExerciseImage(request):#must recreate whole exercise
    if request.method == 'POST':
        print(request.FILES)
        if request.FILES != {}:
            file_name = request.GET['file_name']
            custom_exercise = CustomExercise.objects.get(id=request.GET['customExerciseId'])
            custom_exercise.local_exercise_image = request.FILES[file_name]
            custom_exercise.save()
        else:
            file_path = request.POST['file_path']
            custom_exercise = CustomExercise.objects.get(id=request.POST['customExerciseId'])
            custom_exercise.local_exercise_image = file_path
            custom_exercise.save()

        json = {'error':False,'message':'Request successfully completed','RequestResponse':'Custom Exercise Image Changed!'}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)

@csrf_exempt
def deleteCustomExercise(request):
    if request.method == 'POST':
        profile_id = request.POST['profileId']
        user_profile = Profile.objects.get(id=profile_id)
        custom_exercise = CustomExercise.objects.get(id=request.POST['customExerciseId'])
        custom_exercise.delete(keep_parents=False)
        user_profile.custom_exercises.remove(custom_exercise)
        user_profile.save()
        custom_exercise = None
        json = {'error':False,'message':'Request successfully completed','RequestResponse':None}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)

from django.http import JsonResponse
from WBBackend.models import DefaultExercise,CustomExercise,Profile
from rest_framework.decorators import api_view

def getDefaultExercises(request):
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

def getDefaultExercise(request):
    if request.method == 'GET':
        ex = DefaultExercise.objects.get(id=request.GET['id'])
        e = {'id':ex.id,'exercise_name':ex.exercise_name,'exercise_description':ex.exercise_description,
             'exercise_image':ex.exercise_image.__str__(),'default_exercise': True}
        json = {'error':False,'message':'Request successfully completed','RequestResponse':e}
        return JsonResponse(json)
    json = {'error':True,'message':'The http request needs to be "GET" not "POST" ','RequestResponse':None}
    return JsonResponse(json)

@api_view(['GET'])
def getCustomExercise(request):
    ex = CustomExercise.objects.get(id=request.GET['id'])
    e = {'id':ex.id,'exercise_name':ex.exercise_name,'exercise_description':ex.exercise_description}
    i = ex.exercise_image.__str__()
    if i == 'static/WorkoutBuddy/ExerciseImages/default_exercise_image.png':
        e['exercise_image'] = ex.exercise_image.__str__()
    else:
        e['exercise_image'] = 'media/'+i

    json = {'error':False,'message':'Request successfully completed','RequestResponse':e}
    return JsonResponse(json)


@api_view(['GET'])
def getCustomExercises(request):
    user_profile = Profile.objects.get(user=request.user)
    ex_list = CustomExercise.objects.filter(user_profile=user_profile).order_by('exercise_name')
    ex_arr = []
    for ex in ex_list:
        e = {'id':ex.id,'exercise_name':ex.exercise_name,
             'exercise_description':ex.exercise_description,'exercise_image':ex.exercise_image.__str__()}
        ex_arr.append(e)

    json = {'error':False,'message':'Request successfully completed','RequestResponse':ex_arr}
    return JsonResponse(json)

@api_view(['GET'])
def getAllExercises(request):
    defaultEx_list =  DefaultExercise.objects.order_by('exercise_name')
    user_profile = Profile.objects.get(user=request.user)
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


@api_view(['POST'])
def createCustomExercise(request):
    user_profile = Profile.objects.get(user=request.user)
    exercise_name = request.POST.get('exercise_name')
    exercise_description = request.POST.get('exercise_description')
    custom_exercise = CustomExercise(user_profile=user_profile)
    custom_exercise.save()
    custom_exercise.exercise_name = exercise_name
    custom_exercise.exercise_description = exercise_description
    if request.FILES != {}:
        custom_exercise.exercise_image = request.FILES['file']
    custom_exercise.save()
    user_profile.custom_exercises.add(custom_exercise)
    user_profile.save()
    json = {'error':False,'message':'Request successfully completed','id':custom_exercise.id}
    return JsonResponse(json)


@api_view(['POST'])
def updateCustomExercise(request):
    exercise_name = request.POST.get('exercise_name')
    exercise_description = request.POST.get('exercise_description')
    custom_exercise = CustomExercise.objects.get(id=request.POST.get('id'))
    custom_exercise.exercise_name = exercise_name
    custom_exercise.exercise_description = exercise_description
    if request.FILES != {}:
        custom_exercise.exercise_image = request.FILES['file']
    custom_exercise.save()
    json = {'error':False,'message':'Request successfully completed'
        ,'RequestResponse':None}
    return JsonResponse(json)

@api_view(['POST'])#make sure to delete local image
def deleteCustomExercise(request):
    user_profile = Profile.objects.get(user=request.user)
    custom_exercise = CustomExercise.objects.get(id=request.POST.get('id'))
    custom_exercise.delete(keep_parents=False)
    user_profile.custom_exercises.remove(custom_exercise)
    user_profile.save()
    json = {'error':False,'message':'Request successfully completed','RequestResponse':None}
    return JsonResponse(json)


#only returns the exerciese names and ids
from django.http import JsonResponse
from WBBackend.models import DefaultExercise,CustomExercise

def getDefaultExercises():
    ex_arr = []
    ex_list = DefaultExercise.objects.order_by('exercise_name')
    for ex in ex_list:
        e = {'id':ex.id,'exercise_name':ex.exercise_name,'exercise_description':ex.exercise_description}
        ex_arr.append(e)

    json = {'error':False,'message':'Request successfully completed',
        'RequestResponse':ex_arr}
    return JsonResponse(json)

def getCustomExercises(request):
    if request.method == 'POST':
        user_profile = Profile.objects.get(user=request.user)
        ex_list = CustomExercise.objects.filter(user_profile=user_profile).order_by('exercise_name')
        ex_arr = []
        for ex in ex_list:
            e = {'id':ex.id,'exercise_name':ex.exercise_name,'exercise_description':ex.exercise_description}
            ex_arr.append(e)
        json = {'error':False,'message':'Request successfully completed','RequestResponse':ex_arr}
        return JsonResponse(json)

def getAllExercises(request):
    if request.method == 'POST':
        defaultEx_list =  DefaultExercise.objects.order_by('exercise_name')
        customEx_list =  CustomExercise.objects.filter(user_profile=user_profile).order_by('exercise_name')
        ex_arr = []
        for ex in defaultEx_list:
            e = {'id':ex.id,'exercise_name':ex.exercise_name,'exercise_description':ex.exercise_description}
            ex_arr.append(e)
        for ex in customEx_list:
            e = {'id':ex.id,'exercise_name':ex.exercise_name,'exercise_description':ex.exercise_description}
            ex_arr.append(e)
        json = {'error':False,'message':'Request successfully completed','RequestResponse':ex_arr}
        return JsonResponse(json)
        
    
def getDefaultExerciseImage(request):
    ex_id = request['id']
    ex = DefaultExercise.objects.get(id=ex_id)
    json = {'error':,False,'message':'Request successfully completed'}
    file = open(ex.exercise_image)#not sure if this is th file path
    #need to use try : catch block to return image file

def getCustomExerciseImage(request):
    ex_id = request['id']
    ex = CustomExercise.objects.get(id=ex_id)
    json = {'error':,False,'message':'Request successfully completed'}
    file = open(ex.exercise_image)#not sure if this is th file path
    #need to use try : catch block to return image file

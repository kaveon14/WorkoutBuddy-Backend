from WBBackend.models import MainWorkout, SubWorkout, Profile, ExerciseGoals,Workout,WorkoutExercise,Set,CustomExercise,DefaultExercise
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
#add function for completeing an workout
@csrf_exempt
def getMainWorkouts(request):
    if request.method == 'POST':
        profileId = request.POST['profileId']
        user_profile = Profile.objects.get(id=profileId)
        mw_list = MainWorkout.objects.filter(user_profile=user_profile)
        mw_arr = []
        for mw in mw_list:
            w = {'id':mw.id,'main_workout_name':mw.main_workout_name}
            mw_arr.append(w)
        json = {'error':False,'message':'Request successfully completed','RequestResponse':mw_arr}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "GET" not "POST" ','RequestResponse':None}
    return JsonResponse(json)

@csrf_exempt
def getSubWorkouts(request):     
    if request.method == 'POST':
        mw_id = request.POST['mainWorkoutId']
        mw = MainWorkout.objects.get(id=mw_id)
        sw_list = SubWorkout.objects.filter(mainworkout=mw)
        sw_arr = []
        for sw in sw_list:
            s = {'id':sw.id,'sub_workout_name':sw.sub_workout_name}
            sw_arr.append(s)
        json = {'error':False,'message':'Request successfully completed','RequestResponse':sw_arr}
        return JsonResponse(json)
     
    json = {'error':True,'message':'The http request needs to be "GET" not "POST" ','RequestResponse':None}
    return JsonResponse(json)

@csrf_exempt
def getSubWorkoutExercises(request):
    if request.method == 'GET':
        sw_id = request.GET['subWorkoutId']
        sw = SubWorkout.objects.get(id=sw_id)
        ex_list =  ExerciseGoals.objects.filter(sub_workout=sw)
        ex_arr = []

        for ex in ex_list:
            e = {'id':ex.id,'goal_sets':ex.goal_sets,'goal_reps':ex.goal_reps}
            if ex.default_exercise is None:
                e['exercise_name'] = ex.custom_exercise.exercise_name
            else:
                e['exercise_name'] = ex.default_exercise.exercise_name
            ex_arr.append(e)
        json = {'error':False,'message':'Request successfully completed','RequestResponse':ex_arr}
        return JsonResponse(json)

    json = {'error':True,'message':'The http request needs to be "GET" not "POST" ','RequestResponse':None}
    return JsonResponse(json)

#clean this up
@csrf_exempt
def getCompletedWorkouts(request):
    if request.method == 'GET':
        profileId = request['profile_id']
        profile = Profile.objects.get(id=profileId)
        wk_list = Workout.objects.filter(user_profile=profile)
        #for workout ex list need to do it in a loop
        
        # this is just a rought fucking draft, JESUS CHRIST!!!!
        #now do the json shit
        print(wk_list)
        we_arr = []
        for wk in wk_list:
            we_list = wk.completed_exercises.all()
            print(we_list)
            dict = {'id':wk.id,'date':wk.date,'subworkout_name':wk.subworkout_name}
            ex_list = []
            ex_arr = []
            
            for we in we_list:
                
                e = {'id':we.id,'exercise_name':we.exercise_name}
                set_list = we.completed_sets.all()
                set_arr = []
                print('yes1')

                for set in set_list:
                    s = {'id':set.id,'set':set.set,'reps':set.reps,
                         'weight':set.weight,'unit':set.unit}
                    set_arr.append(s)
                    print('yes2')
                    
                e['sets'] = set_arr
                ex_arr.append(e)

            dict['completed_exercises'] = ex_arr
            we_arr.append(dict)

        json = {'error':False,'message':'Request successfully completed','RequestResponse':we_arr}
        return JsonResponse(json)
    json = {'error':True,'message':'The http request needs to be "GET" not "POST" ','RequestResponse':None}
    return JsonResponse(json)

#create sub workouts differently
@csrf_exempt#not right
def createMainWorkout(request):
    if request.method == 'POST':
        profile_id = request.POST['profileId']
        user_profile = Profile.objects.get(id=profile_id)
        main_workout_name = request.POST['main_workout_name']
        main_workout = MainWorkout(main_workout_name=main_workout_name)
        main_workout.save()
        main_workout.user_profile = user_profile
        main_workout.save()
        user_profile.custom_main_workouts.add(main_workout)
        user_profile.save()
        print(main_workout.main_workout_name)
        json = {'error':False,'message':'Request successfully completed','RequestResponse':None}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)

@csrf_exempt
def createSubWorkout(request):
    if request.method == 'POST':
        profile_id = request.POST['profileId']
        user_profile = Profile.objects.get(id=profile_id)
        main_workout = MainWorkout.objects.get(id=request.POST['mainorkoutId'])
        sub_workout_name = request.POST['sub_workout_name']
        sub_workout = SubWorkout(main_workout=main_workout,sub_workout_name=sub_workout_name)
        json_list = request.POST['exercise_list']
        default_ex_list = []
        custom_ex_list = []
        for map in json_list:
            if map['custom_exercise'] is True:
                ex = CustomExercise.objects.get(id=map['id'])
                custom_ex_list.append(ex)                                
            else: 
            ex = DefaultExercise.objects.get(id=map['id'])
            default_ex_list.append(ex)

        sub_workout.save()
        main_workout.sub_workouts.add(sub_workout)
        sub_workout.default_exercises.add(*default_ex_list)
        sub_workout.custom_exercises.add(*custom_ex_list)
        sub_workout.save()
        sub_workout.user_profile = user_profile
        sub_workout.save()
        user_profile.custom_sub_workouts.add(sub_workout)
        json = {'error':False,'message':'Request successfully completed','RequestResponse':None}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)


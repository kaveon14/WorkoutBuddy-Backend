from WBBackend.models import MainWorkout, SubWorkout, Profile, ExerciseGoals,Workout,WorkoutExercise,Set,CustomExercise,DefaultExercise
from django.http import JsonResponse
import json

def getMainWorkouts(request):
    if request.method == 'GET':
        profileId = request['profileId']
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

def getSubWorkouts(request):     
    if request.method == 'GET':
        mw_id = request['mainWorkoutId']
        mw = MainWorkoutId.objects.get(id=mw_id)
        sw_list = SubWorkout.objects.filter(mainworkout=mw)
        sw_arr = []
        for sw in sw_list:
            s = {'id':sw.id,'sub_workout_name':sw.sub_workout_name}
            sw_arr.apped(s)
        json = {'error':False,'message':'Request successfully completed','RequestResponse':sw_arr}
        return JsonResponse(json)
     
    json = {'error':True,'message':'The http request needs to be "GET" not "POST" ','RequestResponse':None}
    return JsonResponse(json)
     
def getSubWorkoutExercises(request):
    if request.method == 'GET':
        sw_id = request['subWorkoutId']
        sw = SubWorkout.objects.get(id=sw_id)
        ex_list =  ExerciseGoals.objects.filter(SubWorkout=sw)
        ex_arr = []

        for ex in ex_list:
            e = {'id':ez.id,'goal_sets':ex.goal_sets,'goal_reps':ex.goal_reps}
            if ex.default_exercise is None:
                e['exercise_name'] = ex.custom_exercise.exercise_name
            else:
                e['exercise_name'] = ex.default_exercise.exercise_name
            ex_arr.append(e)
        json = {'error':False,'message':'Request successfully completed','RequestResponse':ex_arr}
        return JsonResponse(json)

    json = {'error':True,'message':'The http request needs to be "GET" not "POST" ','RequestResponse':None}
    return JsonResponse(json)

#works as expected
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
def createMainWorkout(request):
    if request.method == 'POST':
        profile_id = request['profile_id']
        user_profile = Profile.objects.get(id=Profile_id)
        main_workout_name = request['main_workout_name']
        main_workout = MainWorkout(user_profile=user_profile,main_workout_name=main_workout_name)
        main_workout.save()
        json = {'error':False,'message':'Request successfully completed','RequestResponse':None}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)


def createSubWorkout(request):
    if request.method == 'POST':
        profile_id = request['profile_id']
        user_profile = Profile.objects.get(id=profile_id)
        main_workout = MainWorkout.objects.get(id=request['mainworkoutId'])
        sub_workout_name = request['sub_workout_name']
        sub_workout = SubWorkout(main_workout=main_workout,sub_workout_name=sub_workout_name)
        json_list = request['exercise_list']
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
        json = {'error':False,'message':'Request successfully completed','RequestResponse':None}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)


from WBBackend.models import MainWorkout, SubWorkout, Profile, ExerciseGoals,Workout,WorkoutExercise,Set,CustomExercise,DefaultExercise
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def getMainWorkouts(request):
    user_profile = Profile.objects.get(user=request.user)
    mw_list = MainWorkout.objects.filter(user_profile=user_profile)
    default_mw = MainWorkout.objects.get(id=1)
    mw_arr = []
    w = {'id':default_mw.id,'main_workout_name':default_mw.main_workout_name}
    mw_arr.append(w)
    for mw in mw_list:
        w = {'id':mw.id,'main_workout_name':mw.main_workout_name}
        mw_arr.append(w)
    json = {'error':False,'message':'Request successfully completed','RequestResponse':mw_arr}
    return JsonResponse(json)

@api_view(['GET'])
def getSubWorkout(request):
    sub_workout = SubWorkout.objects.get(id=request.GET['id'])
    sw = {'id':sub_workout.id,'sub_workout_name':sub_workout.sub_workout_name}
    json = {'error':False,'message':'Request successfully completed','RequestResponse':sw}
    return JsonResponse(json)

@api_view(['GET'])
def getSubWorkouts(request):
    mw_id = request.GET['mainWorkoutId']
    mw = MainWorkout.objects.get(id=mw_id)
    sw_list = SubWorkout.objects.filter(mainworkout=mw)
    sw_arr = []
    for sw in sw_list:
        s = {'id':sw.id,'sub_workout_name':sw.sub_workout_name}
        sw_arr.append(s)
    json = {'error':False,'message':'Request successfully completed','RequestResponse':sw_arr}
    return JsonResponse(json)

@api_view(['GET'])
def getSubWorkoutExerciseGoals(request):#reps and sets are all the same with no ranges
    #sw_id = request.GET['subWorkoutId']
    #print(sw_id)
    sw = SubWorkout.objects.get(id=request.GET['subWorkoutId'])
    ex_list =  ExerciseGoals.objects.filter(sub_workout=sw)
    ex_arr = []
    for ex in ex_list:
        e = {'id':ex.id,'goal_sets':ex.goal_sets,'goal_reps':ex.goal_reps}
        if ex.default_exercise is None:
            e['exercise_name'] = ex.custom_exercise.exercise_name
            e['exercise_id'] =  ex.custom_exercise.id
            e['default_exercise'] = False
        else:
            e['exercise_name'] = ex.default_exercise.exercise_name
            e['exercise_id'] =  ex.default_exercise.id
            e['default_exercise'] = True
        ex_arr.append(e)

    json = {'error':False,'message':'Request successfully completed','RequestResponse':ex_arr}
    return JsonResponse(json)

@api_view(['GET'])
def getSubWorkoutExerciseGoal(request):
    ex_goal = ExerciseGoals.objects.get(id=request.GET['exGoalId'])
    e = {'id':ex_goal.id,'goal_sets':ex_goal.goal_sets,'goal_reps':ex_goal.goal_reps}
    if ex_goal.default_exercise is None:
        e['exercise_name'] = ex_goal.custom_exercise.exercise_name
        e['exercise_id'] = ex_goal.custom_exercise.id
        e['default_exercise'] = False
    else:
        e['exercise_name'] = ex_goal.default_exercise.exercise_name
        e['exercise_id'] = ex_goal.default_exercise.id
        e['default_exercise'] = True
    json = {'error': False, 'message': 'Request successfully completed', 'RequestResponse': e}
    return JsonResponse(json)


@api_view(['GET'])
def getCompletedWorkouts(request):
    user_profile = Profile.objects.get(user=request.user)
    wk_list = Workout.objects.filter(user_profile=user_profile)
    we_arr = []

    for wk in wk_list:
        we_list = wk.completed_exercises.all()
        dict = {'id':wk.id,'date':wk.date,'main_workout_name':wk.main_workout_name,'sub_workout_name':wk.sub_workout_name}
        ex_arr = []

        for we in we_list:
            e = {'id':we.id,'exercise_name':we.exercise_name}
            set_list = we.completed_sets.all()
            set_arr = []
            for set in set_list:
                s = {'id':set.id,'set':set.set,'reps':set.reps,
                     'weight':set.weight,'unit':set.unit}
                set_arr.append(s)

            e['sets'] = set_arr
            ex_arr.append(e)
            dict['completed_exercises'] = ex_arr
            we_arr.append(dict)

        json = {'error':False,'message':'Request successfully completed','RequestResponse':we_arr}
        return JsonResponse(json)

@api_view(['POST'])
def createMainWorkout(request):
    user_profile = Profile.objects.get(user=request.user)
    main_workout_name =  request.POST.get('main_workout_name')
    main_workout = MainWorkout(main_workout_name=main_workout_name)
    main_workout.save()
    main_workout.user_profile = user_profile
    main_workout.save()
    user_profile.custom_main_workouts.add(main_workout)
    user_profile.save()

    json = {'error':False,'message':'Request successfully completed','RequestResponse':{'id':main_workout.id}}
    return JsonResponse(json)

@api_view(['POST'])
def createSubWorkout(request):
    user_profile = Profile.objects.get(user=request.user)
    main_workout = MainWorkout.objects.get(id=request.POST.get('mainWorkoutId'))
    sub_workout_name = request.POST.get('sub_workout_name')
    sub_workout = SubWorkout(main_workout=main_workout,sub_workout_name=sub_workout_name)
    sub_workout.save()
    main_workout.sub_workouts.add(sub_workout)
        
    sub_workout.user_profile = user_profile
    sub_workout.save()
    user_profile.custom_sub_workouts.add(sub_workout)
    user_profile.save()
    json = {'error':False,'message':'Request successfully completed','RequestResponse':{'id':sub_workout.id}}
    return JsonResponse(json)


@api_view(['POST'])
def setSubWorkoutExercises(request):#has this been tested
    sub_workout_id = request.POST.get('subWorkoutId')
    sub_workout = SubWorkout.objects.get(id=sub_workout_id)

    json_list = request.POST.get('exercise_list')
    default_ex_list = []
    custom_ex_list = []
    for map in json_list:
        if map['default_exercise'] is False:
            ex = CustomExercise.objects.get(id=map['id'])
            custom_ex_list.append(ex)
        else:
            ex = DefaultExercise.objects.get(id=map['id'])
            default_ex_list.append(ex)

    sub_workout.default_exercises.add(*default_ex_list)
    sub_workout.custom_exercises.add(*custom_ex_list)
    sub_workout.save()

    json = {'error':False,'message':'Request successfully completed','RequestResponse':None}
    return JsonResponse(json)

@api_view(['POST'])
def deleteMainWorkout(request):
    user_profile = Profile.objects.get(user=request.user)
    main_workout = MainWorkout.objects.get(id=request.POST.get('id'))
    main_workout.delete(keep_parents=False)
    user_profile.remove(main_workout)
    user_profile.save()
    main_workout = None
    json = {'error':False,'message':'Request successfully completed','RequestResponse':None}
    return JsonResponse(json)

@api_view(['POST'])
def deleteSubWorkout(request):#need to delete the exercise goals as well
    sub_workout = SubWorkout.objects.get(id=request.POST.get('id'))
    sub_workout.delete(keep_parents=False)
    sub_workout = None
    json = {'error':False,'message':'Request successfully completed','RequestResponse':None}
    return JsonResponse(json)

@api_view(['POST'])
def updateMainWorkoutName(request):
    main_workout = MainWorkout.objects.get(id=request.POST.get('id'))
    main_workout.main_workout_name = request.POST.get('main_workout_name')
    main_workout.save()
    json = {'error': False, 'message': 'Request successfully completed', 'RequestResponse': None}
    return JsonResponse(json)

@api_view(['POST'])
def updateSubWorkoutName(request):
    sub_workout = SubWorkout.objects.get(id=request.POST.get('id'))
    sub_workout.sub_workout_name = request.POST.get('sub_workout_name')
    sub_workout.save()
    json = {'error': False, 'message': 'Request successfully completed', 'RequestResponse': None}
    return JsonResponse(json)

@api_view(['POST'])
def addSubWorkoutExerciseGoals(request):#need to add to workout or something
    ex_goal = ExerciseGoals(goal_sets=request.POST.get('goal_sets'))
    ex_goal.goal_reps = request.POST.get('goal_reps')
    ex_goal.save()
    sub_workout = SubWorkout.objects.get(id=request.POST.get('subWorkoutId'))
    ex_goal.sub_workout = sub_workout
    if request.POST.get('default_exercise'):
        ex = DefaultExercise.objects.get(id=request.POST.get('exercise_id'))
        ex_goal.default_exercise = ex
    else:
        ex = CustomExercise.objects.get(id=request.POST.get('exercise_id'))
        ex_goal.custom_exercise = ex
    ex_goal.save()
    json = {'error': False, 'message': 'Request successfully completed', 'RequestResponse': None}
    return JsonResponse(json)

@api_view(['POST'])
def updateExerciseGoal(request):#gotta convert to that jsoon shit
    ex_goal = ExerciseGoals.objects.get(id=request.POST.get('id'))
    if request.POST.get('default_exercise'):
        ex_goal.default_exercise = DefaultExercise.objects.get(id=request.POST.get('exercise_id'))
    else:
        ex_goal.custom_exercise = CustomExercise.objects.get(id=request.POST.get('exercise_id'))
    ex_goal.goal_sets = request.POST.get('goal_sets')
    ex_goal.goal_reps = request.POST.get('goal_reps')
    ex_goal.save()
    json = {'error': False, 'message': 'Request successfully completed', 'RequestResponse': None}
    return JsonResponse(json)


@api_view(['POST'])
def deleteSubWorkoutExerciseGoals(request):
    ex_goal = ExerciseGoals.objects.get(id=request.POST.get('id'))
    ex_goal.delete()
    ex_goal = None
    json = {'error': False, 'message': 'Request successfully completed', 'RequestResponse': None}
    return JsonResponse(json)
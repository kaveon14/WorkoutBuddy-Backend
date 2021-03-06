from django.core.management.base import BaseCommand
from WBBackend.models import DefaultExercise,MainWorkout,SubWorkout,ExerciseGoals

'''Need to add sets and reps to sub workouts'''

#need to change this slightly
def getDefaultImagePath():
    default_image_path = 'WorkoutBuddy/ExerciseImages/default_exercise_image.png'
    return default_image_path
    
def get_exercise_image_path( exercise_name):#check for both png and jpg
    image_png = None
    try:
        image_png = open('WorkoutBuddy/ExerciseImages/'+exercise_name+'.png')
    except FileNotFoundError:
        print('File Not Found!!')
    if image_png != None:
        return image_png.name


    image_jpg = None
    try:
        image_jpg = open('WorkoutBuddy/ExerciseImages/'+exercise_name+'.jpg')
    except FileNotFoundError:
        print('File Not Found!!')
    if image_jpg != None:
        return image_jpg.name

    return getDefaultImagePath()

def create_exercises():
    exercise_content_file = open('WBBackend/default_data/default_exercise_content.txt','r+')
    exercise_list = exercise_content_file.read().split('\n')
    exercise_file_lines = ''
    ex_name = exercise_list[0]

    i = 0
    while i < len(exercise_list)-1:
        if exercise_list[i] == '@//':
            exercise = DefaultExercise(exercise_name=ex_name,exercise_description=exercise_file_lines)
            exercise.exercise_image = get_exercise_image_path(exercise_name=ex_name)
            exercise.save()
            exercise_file_lines = ''
            ex_name = exercise_list[i+1]
            i += 2
        else:
            exercise_file_lines += (exercise_list[i] + '\n')
            i += 1
        
    exercise = DefaultExercise(exercise_name=ex_name, exercise_description=exercise_file_lines)
    exercise.exercise_image = get_exercise_image_path(exercise_name=ex_name)
    exercise.save()


def create_default_main_workout():
    main_workout = MainWorkout(main_workout_name='Default Workouts')
    main_workout.save()

def create_default_sub_workouts():#need to also set sub workout id for the data added
    main_workout = MainWorkout(main_workout_name='Default Workouts')
    main_workout.save()

    sub_workout_content_file = open('WBBackend/default_data/default_sub_workouts.txt','r+')
    file_lines = sub_workout_content_file.read().split('\n')

    i = 1
    sub_name = file_lines[0]#main workout name is wrong
    sub_workout = SubWorkout(main_workout=main_workout,sub_workout_name=sub_name)
    sub_workout.save()
    main_workout.sub_workouts.add(sub_workout)

    while i < len(file_lines)-3:#gets all exercises,reps and sets
        if file_lines[i] == '@//':
            sub_workout.save()
            sub_name = file_lines[i+1]
            sub_workout = SubWorkout(main_workout=main_workout, sub_workout_name=sub_name)
            sub_workout.save()
            main_workout.sub_workouts.add(sub_workout)
            i += 2
        else:
            ex_name = file_lines[i]
            ex_sets = file_lines[i + 1]
            ex_reps = file_lines[i + 2]
            exercise = DefaultExercise.objects.get(exercise_name=ex_name)
            sub = SubWorkout.objects.get(sub_workout_name=sub_name)
            exercise_goals = ExerciseGoals(default_exercise=exercise,goal_reps=ex_reps.strip(),sub_workout=sub)
            exercise_goals.goal_sets = ex_sets
            exercise_goals.save()
            sub_workout.default_exercises.add(exercise)
            i += 3
    main_workout.save()

'''Need to add sets and reps to sub workouts'''
class Command(BaseCommand):
    args = 'None'
    help = 'Help string test'
    def handle(self,*args,**options):
        create_exercises()
        create_default_sub_workouts()

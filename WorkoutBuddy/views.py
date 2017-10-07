from django.shortcuts import render
from WorkoutBuddy.models import MainWorkout,SubWorkout,DefaultExercise
from django.views import generic
# Create your views here.

class ViewDefaultExercises(generic.ListView):
    template_name = 'WorkoutBuddy/exercise_list.html'
    model = DefaultExercise
    context_object_name = 'exercise_list'
    fields = ['exercise_name']

class ExerciseDescription(generic.DetailView):
    model = DefaultExercise
    context_object_name = 'exercise'
    template_name = 'WorkoutBuddy/exercise_description.html'

class CreateMainWorkout(generic.CreateView):
    template_name = 'WorkoutBuddy/create_mainworkout.html'
    model = MainWorkout
    fields = ['main_workout_name']

class CreateSubWorkout(generic.CreateView):
    template_name = 'WorkoutBuddy/create_subworkout.html'
    model = SubWorkout
    fields = ['main_workout','sub_workout_name']
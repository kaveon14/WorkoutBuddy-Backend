from WorkoutBuddy.models import MainWorkout,SubWorkout,DefaultExercise,CustomExercise,Profile,ExerciseGoals,ProgressPhoto
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.
from .forms import CreateExerciseForm,CreateMainWorkoutForm

@login_required(login_url='/login/')
def createExercise(request):#edit this
    if request.method == 'POST':
        form = CreateExerciseForm(request.POST, request.FILES)

        if form.is_valid():
            ex_image = form.cleaned_data.get('exercise_image')
            ex_name = form.cleaned_data.get('exercise_name')
            ex_description = form.cleaned_data.get('exercise_description')
            ce = CustomExercise(exercise_name=ex_name, exercise_description=ex_description)
            ce.save()
            user = request.user
            ce.exercise_image = ex_image
            ce.local_exercise_image \
                = ce.user_local_directory_exercise_image_path(filename=ex_image.name)
            ce.user = user
            ce.save()
            return HttpResponseRedirect('/exercises/')
    else:
        form = CreateExerciseForm()
    return render(request, 'WorkoutBuddy/create_exercise.html', {'form': form})

@login_required(login_url='/login/')
def createMainWorkout(request):
    if request.method == 'POST':

        form = CreateMainWorkoutForm(request.POST)
        if form.is_valid():
           main_workout_name = form.cleaned_data.get('main_workout_name')
           main_workout = MainWorkout(main_workout_name=main_workout_name)
           main_workout.save()
           user = request.user
           main_workout.user_profile = Profile.objects.get(user=user)
           main_workout.save()
           return HttpResponseRedirect('/subworkouts/')
    else:
        form = CreateMainWorkoutForm()
    return render(request, 'WorkoutBuddy/create_mainworkout.html', {'form': form})

class ViewDefaultExercises(generic.ListView):#base add exercise goals off of this
    template_name = 'WorkoutBuddy/exercise_list.html'
    model = DefaultExercise
    context_object_name = 'exercise_list'

    def get_context_data(self, **kwargs):#needs editing
        context = super(ViewDefaultExercises,self).get_context_data(**kwargs)
        context['ce_list'] = CustomExercise.objects.order_by('exercise_name')
        return context

class ExerciseDescription(generic.DetailView):
    model = DefaultExercise
    context_object_name = 'exercise'
    template_name = 'WorkoutBuddy/exercise_description.html'

class CustomExerciseDescription(generic.DetailView):
    model = CustomExercise
    context_object_name = 'exercise'
    template_name = 'WorkoutBuddy/custom_exercise_description.html'

class CreateSubWorkout(generic.CreateView):#on save go to page too add exercise goals
    template_name = 'WorkoutBuddy/create_subworkout.html'
    model = SubWorkout
    fields = ['main_workout','sub_workout_name']

class SubWorkoutList(generic.ListView):
    template_name = 'WorkoutBuddy/subworkout_list.html'
    model = SubWorkout#includde link to page with all exercises and goals with links to ex descriptions
    context_object_name = 'subworkout_list'

class MainWorkoutList(generic.ListView):
    template_name = 'WorkoutBuddy/mainworkout_list.html'
    model = MainWorkout#include link to page with sub workouts
    context_object_name = 'mainworkout_list'

class ViewExerciseGoals(generic.ListView):
    template_name = 'WorkoutBuddy/exercise_goals.html'
    model = ExerciseGoals
    context_object_name = 'exercise_list'

    def get_context_data(self, **kwargs):
        context = super(ViewExerciseGoals, self).get_context_data(**kwargs)
        id = self.kwargs['pk']
        subworkout = SubWorkout.objects.get(id=id)
        context['exercise_list'] = ExerciseGoals.objects.filter(sub_workout=subworkout)
        return context

class ViewProgressPhotos(generic.DetailView):#need to have list to get to this
    template_name = ''
    model = ProgressPhoto
    fields = ['date_time','photo']
    context_object_name = 'progress_photo'

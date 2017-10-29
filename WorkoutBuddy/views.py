from WorkoutBuddy.models import MainWorkout,SubWorkout,DefaultExercise,CustomExercise
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.
from .forms import CreateExerciseForm

@login_required(login_url='/login/')
def CreateExercise(request):
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


class ViewDefaultExercises(generic.ListView):
    template_name = 'WorkoutBuddy/exercise_list.html'
    model = DefaultExercise
    context_object_name = 'exercise_list'

    def get_context_data(self, **kwargs):
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

class CreateMainWorkout(generic.CreateView):
    template_name = 'WorkoutBuddy/create_mainworkout.html'
    model = MainWorkout
    fields = ['main_workout_name']

class CreateSubWorkout(generic.CreateView):
    template_name = 'WorkoutBuddy/create_subworkout.html'
    model = SubWorkout
    fields = ['main_workout','sub_workout_name']


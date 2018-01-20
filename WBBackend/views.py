from WBBackend.models import MainWorkout,SubWorkout,DefaultExercise,CustomExercise,Profile,ExerciseGoals,ProgressPhoto,user_local_directory_image_path
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.
import datetime
from .forms import CreateExerciseForm,CreateMainWorkoutForm,CreateProgressPhotoForm

@login_required(login_url='/login/')
def createProgressPhoto(request):
    if request.method == 'POST':
        form = CreateProgressPhotoForm(request.POST, request.FILES)

        if form.is_valid():
            photo = form.cleaned_data.get('photo')
            i = datetime.datetime.now()
            date_time = '%s-%s-%s %s:%s:%s' % (i.year, i.month, i.day, i.hour, i.minute, i.second)
            progress_photo = ProgressPhoto(date_time=date_time)
            progress_photo.save()
            user = request.user
            progress_photo.user = user
            progress_photo.photo = photo
            user_profile = Profile.objects.get(user=user)
            local_path = user_local_directory_image_path(photo.name)
            progress_photo. local_photo = local_path
            progress_photo.user_profile = user_profile
            progress_photo.save()
            return HttpResponseRedirect('/exercises/progressphotos/')
    else:
        form = CreateProgressPhotoForm()
    return render(request, 'WBBackend/create_progress_photo.html', {'form': form})

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
    return render(request, 'WBBackend/create_exercise.html', {'form': form})

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
    return render(request, 'WBBackend/create_mainworkout.html', {'form': form})

class ViewDefaultExercises(generic.ListView):#base add exercise goals off of this
    template_name = 'WBBackend/exercise_list.html'
    model = DefaultExercise
    context_object_name = 'exercise_list'

    def get_context_data(self, **kwargs):#needs editing
        context = super(ViewDefaultExercises,self).get_context_data(**kwargs)
        context['ce_list'] = CustomExercise.objects.order_by('exercise_name')
        return context

class ExerciseDescription(generic.DetailView):
    model = DefaultExercise
    context_object_name = 'exercise'
    template_name = 'WBBackend/exercise_description.html'

class CustomExerciseDescription(generic.DetailView):
    model = CustomExercise
    context_object_name = 'exercise'
    template_name = 'WBBackend/custom_exercise_description.html'

class CreateSubWorkout(generic.CreateView):#on save go to page too add exercise goals
    template_name = 'WBBackend/create_subworkout.html'
    model = SubWorkout
    fields = ['main_workout','sub_workout_name']

class SubWorkoutList(generic.ListView):
    template_name = 'WBBackend/subworkout_list.html'
    model = SubWorkout#includde link to page with all exercises and goals with links to ex descriptions
    context_object_name = 'subworkout_list'

class MainWorkoutList(generic.ListView):
    template_name = 'WBBackend/mainworkout_list.html'
    model = MainWorkout#include link to page with sub workouts
    context_object_name = 'mainworkout_list'

class ViewExerciseGoals(generic.ListView):
    template_name = 'WBBackend/exercise_goals.html'
    model = ExerciseGoals
    context_object_name = 'exercise_list'

    def get_context_data(self, **kwargs):
        context = super(ViewExerciseGoals, self).get_context_data(**kwargs)
        id = self.kwargs['pk']
        subworkout = SubWorkout.objects.get(id=id)
        context['exercise_list'] = ExerciseGoals.objects.filter(sub_workout=subworkout)
        return context

class CreateProgressPhoto(generic.CreateView):#use form
    template_name = 'WBBackend/'
    model = ProgressPhoto
    context_object_name = 'progress_photo'


class ProgressPhotosList(generic.ListView):
    template_name = 'WBBackend/progress_photo_list.html'
    model = ProgressPhoto
    context_object_name = 'progress_photos'

    def get_queryset(self):
        user_profile = Profile.objects.get(user=self.request.user)
        return ProgressPhoto.objects.filter(user_profile=user_profile).order_by('date_time')

class ViewProgressPhotos(generic.DetailView):#need to have list to get to this
    template_name = 'WBBackend/progress_photo.html'
    model = ProgressPhoto
    fields = ['date_time','photo']
    context_object_name = 'progress_photo'
from django import forms
from WorkoutBuddy.models import CustomExercise,MainWorkout,ExerciseGoals,ProgressPhoto

class CreateExerciseForm(forms.ModelForm):#Edit this
    exercise_image = forms.ImageField(label="Exercise Image")
    class Meta:
        model = CustomExercise
        fields = ['exercise_name','exercise_description']

class CreateMainWorkoutForm(forms.ModelForm):
    class Meta:
        model = MainWorkout
        fields = ['main_workout_name']

class CreateProgressPhotoForm(forms.ModelForm):
    class Meta:
        model = ProgressPhoto
        fields = ['photo']

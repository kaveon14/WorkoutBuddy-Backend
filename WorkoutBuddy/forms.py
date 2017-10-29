from django import forms
from WorkoutBuddy.models import CustomExercise


class CreateExerciseForm(forms.ModelForm):
    exercise_image = forms.ImageField(label="Exercise Image")
    class Meta:
        model = CustomExercise
        fields = ['exercise_name','exercise_description']


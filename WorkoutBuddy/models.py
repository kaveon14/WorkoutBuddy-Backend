from django.db import models
from django.contrib.auth.models import User

# may use validators
def user_directory_profile_image(instance, filename):
    d = 'ProfileImage/' + filename
    return 'user_{0}/{1}'.format(instance.user.id, d)

def user_directory_progress_photo__path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    d = 'ProgressPhotos/' + filename
    return 'user_{0}/{1}'.format(instance.user.id, d)

def user_directory_exercise_image_path(instance, filename):
    d = 'CustomExerciseImages/' + filename
    return 'user_{0}/{1}'.format(instance.user.id, d)
#use these in a view or template
def user_local_directory_profile_image_path(filename):
    path = '/data/user/0/com.example.WorkoutBuddy.workoutbuddy/files/ProfileImage/'
    return path + filename

def user_local_directory_progress_photo_path(filename):
    path = '/data/user/0/com.example.WorkoutBuddy.workoutbuddy/files/ProgressPhotos/'
    return path + filename

def user_local_directory_exercise_image_path(filename):
    path = '/data/user/0/com.example.WorkoutBuddy.workoutbuddy/files/CustomExerciseImages/'
    return path + filename

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    profile_picture = models.ImageField(upload_to=user_directory_profile_image,null=True)
    local_profile_picture = models.ImageField(null=True)

    max_bench = models.OneToOneField('MaxBench',null=True)
    max_squat = models.OneToOneField('MaxSquat',null=True)
    max_dead_lift = models.OneToOneField('MaxDeadLift',null=True)

    custom_main_workouts = models.ManyToManyField('MainWorkout')
    custom_sub_workouts = models.ManyToManyField('SubWorkout')

    custom_exercises = models.ManyToManyField('CustomExercise')
    progress_photos = models.ManyToManyField('ProgressPhoto')
    workout_stats = models.ManyToManyField('Workout')

    def __str__(self):
        return self.user.username


class MaxSquat(models.Model):
    max_squat = models.IntegerField(default=0)
    UNIT_CHOICES = (
        ('kg', 'kilograms'),
        ('lbs', 'pounds'),
    )
    unit = models.CharField(max_length=3, choices=UNIT_CHOICES, default='lbs')

class MaxBench(models.Model):
    max_bench = models.IntegerField(default=0)
    UNIT_CHOICES = (
        ('kg', 'kilograms'),
        ('lbs', 'pounds'),
    )
    unit = models.CharField(max_length=3, choices=UNIT_CHOICES, default='lbs')

class MaxDeadLift(models.Model):
    max_dead_lift = models.IntegerField(default=0)
    UNIT_CHOICES = (
        ('kg', 'kilograms'),
        ('lbs', 'pounds'),
    )
    unit = models.CharField(max_length=3, choices=UNIT_CHOICES, default='lbs')


class Body(models.Model):
    UNIT_CHOICES = (
        ('kg', 'kilograms'),
        ('lbs', 'pounds'),
    )
    profile = models.ForeignKey(Profile, null=True)
    date = models.DateField(help_text="MM-DD-YYYY")
    weight = models.DecimalField(max_digits=3, decimal_places=1, default=0.0,help_text="Weight in lbs or kgs")  # possibly add choice box
    unit = models.CharField(max_length=3, choices=UNIT_CHOICES, default='lbs')
    chest_size = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, help_text="Enter chest size")
    back_size = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, help_text="Enter back size")
    arm_size = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, help_text="Enter arm size")
    forearm_size = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, help_text="Enter forearm size")
    waist_size = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, help_text="Enter waist size")
    quad_size = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, help_text="Enter quad size")
    calf_size = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, help_text="Enter calf size")

    def __str__(self):
        return self.date

class DefaultExercise(models.Model):
    exercise_name = models.CharField(max_length=100)
    exercise_description = models.TextField(max_length=2000)
    exercise_image = models.ImageField(null=True)

class CustomExercise(models.Model):
    user_profile = models.ForeignKey(Profile,null=True)
    exercise_name = models.CharField(max_length=100)
    exercise_description = models.TextField(max_length=2000)

class CustomExerciseImage(models.Model):
    user = User
    exercise = models.OneToOneField(CustomExercise, on_delete=models.CASCADE)
    exercise_image = models.ImageField(upload_to=user_directory_exercise_image_path,null=True)#define image path user/custom_exercise_images/
    local_exercise_image = models.ImageField(null=True)

class ExerciseGoals(models.Model):
    SET_CHOICES = zip(range(1, 16), range(1, 16))
    goal_sets = models.IntegerField(default=1,choices=SET_CHOICES)
    goal_reps = models.CharField(max_length=10)
    default_exercise = models.ForeignKey(DefaultExercise,null=True)
    custom_exercise = models.ForeignKey(CustomExercise,null=True)
    sub_workout = models.ForeignKey('SubWorkout',on_delete=models.CASCADE,null=True);

class ProfileImage(models.Model):
    user = User
    user_profile = models.ForeignKey(Profile, null=True)
    profile_image = models.ImageField(upload_to=user_directory_profile_image)#define user/profile_image/
    local_profile_image = models.ImageField(null=True)
    date = models.DateField(help_text="MM-DD-YYYY")

class ProgressPhoto(models.Model):
    user = User
    user_profile = models.ForeignKey(Profile, null=True)
    photo = models.ImageField(upload_to=user_directory_profile_image)
    local_photo = models.ImageField(null=True)
    date_time = models.DateTimeField(help_text="MM-DD-YYYY HH:MM:SS")

class MainWorkout(models.Model):
    user_profile = models.ForeignKey(Profile,null=True)
    main_workout_name = models.CharField(max_length=100,help_text="Enter a name for your MainWorkout")
    sub_workouts = models.ManyToManyField('SubWorkout')

class SubWorkout(models.Model):
    user_profile = models.ForeignKey(Profile,null=True)
    main_workout = models.ForeignKey(MainWorkout,on_delete=models.CASCADE)
    sub_workout_name = models.CharField(max_length=100,help_text="Enter a name for your SubWorkout")
    default_exercises = models.ManyToManyField(DefaultExercise)#these should be workout exercises with reps,sets,ad weight
    custom_exercises = models.ManyToManyField(CustomExercise)

class Set(models.Model):
    workout_exercise = models.ForeignKey('WorkoutExercise')
    SET_CHOICES = zip(range(1, 16), range(1, 16))
    set = models.IntegerField(default=1, choices=SET_CHOICES)
    reps = models.IntegerField(default=1)
    weight = models.IntegerField(default=0)
    UNIT_CHOICES = (
        ('kg', 'kilograms'),
        ('lbs', 'pounds'),
    )
    unit = models.CharField(max_length=3, choices=UNIT_CHOICES, default='lbs')

class WorkoutExercise(models.Model):
    workout_tag = models.ForeignKey('Workout')
    exercise_name = models.CharField(max_length=100)  # change to char set and only use name
    completed_sets = models.ManyToManyField(Set)
    SET_CHOICES = zip(range(1, 16), range(1, 16))
    sets = models.IntegerField(default=1, choices=SET_CHOICES)
    rep_range = models.CharField(max_length=100)
    weight = models.IntegerField(default=0)
    UNIT_CHOICES = (
        ('kg', 'kilograms'),
        ('lbs', 'pounds'),
    )
    unit = models.CharField(max_length=3, choices=UNIT_CHOICES, default='lbs')

class Workout(models.Model):
    user_profile = models.ForeignKey(Profile, null=True)
    date = models.DateField(help_text="MM-DD-YYYY")
    completed_exercises = models.ManyToManyField(WorkoutExercise)
    total_sets = models.IntegerField(default=0)
    total_reps = models.IntegerField(default=0)
    total_weight = models.IntegerField(default=0)
    UNIT_CHOICES = (
        ('kg', 'kilograms'),
        ('lbs', 'pounds'),
    )
    unit = models.CharField(max_length=3, choices=UNIT_CHOICES, default='lbs')
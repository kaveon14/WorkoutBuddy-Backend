from WBBackend.models import Profile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# do not get rest of profile shit
#setting max lifts should be an internal service

@csrf_exempt
def getProfileImage(request):
    if request.method == 'POST':
        profileId = request.POST['profileId']
        profile = Profile.objects.get(id=profileId)
        profile_image_path = profile.profile_picture.url
        json = {'id':profile.id,'profile_picture':profile_image_path}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)
3
#internalally updated, will be tested later
@csrf_exempt
def getMaxLifts(request):
    if request.method == 'POST':
        profileId = request.POST['profileId']
        profile = Profile.objects.get(id=profileId)

        max_lifts = []
        max_bench = {'exercise_name':'Bench Press','max_lift':profile.max_bench.max_bench,'unit':profile.max_bench.unit}
        max_squat = {'exercise_name':'Squat','max_lift':profile.max_squat.max_squat,'unit':profile.max_squat.unit}
        max_dead_lift = {'exercise_name':'Dead-Lift','max_lift':profile.max_squat.max_dead_lift,'unit':profile.max_dead_lift.unit}
        max_lifts.append(max_bench)
        max_lifts.append(max_squat)
        max_lifts.append(max_dead_lift)

        json = {'error':False,'message':'Request successfully completed','RequestResponse':max_lifts}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)

@csrf_exempt
def updateProfileImage(request):
    if request.method == 'POST':
        if request.FILES != {}:#path is not right,define path in model with a func
            file_name = request.GET['file_name']
            profileId = request.GET['profileId']
            user_profile = Profile.objects.get(id=profileId)
            user_profile.profile_picture = request.FILES[file_name]
            user_profile.save()
        else:
            file_path = request.POST['file_path']
            profileId = request.POST['profileId']
            user_profile = Profile.objects.get(id=profileId)
            user_profile.profile_picture = file_path
            user_profile.save()

        json = {'error':False,'message':'Request successfully completed','RequestResponse':'Profile Image Changed!'}
        return JsonResponse(json)
    
    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)

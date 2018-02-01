from WBBackend.models import Profile
# do not get rest of profile shit
def getProfileImage(request):
    if request.method == 'GET':
        profileId = request['profileId']
        user_profile = Profile.objects.get(id=profileId)
        profile_image_path = profile.Profile_picture.url
        json = {'id':user_profile.id,'profile_picture':profile_image_path}
        return JsonResponse(json)

def getMaxLifts(request):
    if request.method == 'GET':
        profileId = request['profileId']
        user_profile = Profile.objects.get(id=profileId)

        max_lifts = []
        max_bench = {'exercise_name':'Bench Press','max_lift':user_profile.max_bench.max_bench,'unit':user_profile.max_bench.unit}
        max_squat = {'exercise_name':'Squat','max_lift':user_profile.max_squat.max_squat,'unit':user_profile.max_squat.unit}
        max_dead_lift = {'exercise_name':'Dead-Lift','max_lift':user_profile.max_squat.max_dead_lift,'unit':user_profile.max_dead_lift.unit}
        max_lifts.append(max_bench)
        max_lifts.append(max_squat)
        max_lifts.append(max_dead_lift)

        json = {'error':False,'message':'Request successfully completed','RequestResponse':max_lifts}
        return JsonResponse(json)
        

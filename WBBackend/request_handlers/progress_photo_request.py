from WBBackend.models import ProgressPhoto,Profile_image_path

def getProgressPhotos(request):
    if request.method == 'POST':
        profile_id = request['profileId']
        profile = Profile.objects.get(id=profile_id)
        # pp = Progress Photo
        pp_list = ProgressPhoto.objects.filter(user=user).order_by('-created_date')

        pp_arr = []
        for pp in pp_list:
            p = {'id':p.id,'date_time':p.date_time,'photo':p.photo.url}
            pp_arr.append(p)

        json = {'error':False,'message':'Request successfully completed',
                'RequestResponse':pp_arr}
        return JsonResponse(json)

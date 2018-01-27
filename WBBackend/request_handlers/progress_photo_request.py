from WBBackend.models import ProgressPhoto
#gonna have import error where user is located
def getProgressPhotos(request):
    if request.method == 'POST':
        user_id = request['user_id']
        user = User.objects.get(id=user_id)
        # pp = Progress Photo
        pp_list = ProgressPhoto.objects.filter(user=user).order_by('-created_date')

        pp_arr = []
        for pp in pp_list:
            p = {'id':p.id,'date_time':p.date_time,'photo':p.photo.url}
            pp_arr.append(p)

        json = {'error':False,'message':'Request successfully completed',
                'RequestResponse':pp_arr}
        return JsonResponse(json)

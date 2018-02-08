from WBBackend.models import ProgressPhoto,Profile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import arrow
#will add more methods in the future for getting progrss photos

@csrf_exempt
def getProgressPhotos(request):
    if request.method == 'POST':
        profile_id = request.POST['profileId']
        profile = Profile.objects.get(id=profile_id)
        pp_list = ProgressPhoto.objects.filter(user_profile=profile).order_by('date_time')#-created_date
        pp_arr = []
        for pp in pp_list:
            p = {'id':pp.id,'date_time':pp.date_time,'photo':pp.photo.url}
            pp_arr.append(p)

        json = {'error':False,'message':'Request successfully completed',
                'RequestResponse':pp_arr}
        return JsonResponse(json)
    json = {'error':True,'message':'The http request needs to be "POST" not "GETT" ','RequestResponse':None}
    return JsonResponse(json)


@csrf_exempt
def addProgressPhoto(request):
    if request.method == 'POST':
        if request.FILES != {}:
            user_profile = Profile.objects.get(id=request.GET['profileId'])
            file_name = request.GET['file_name']
            date_time = arrow.now().format('YYYY-MM-DD')
            progress_photo = ProgressPhoto(date_time=date_time)
            progress_photo.save()
            progress_photo.user_profile = user_profile#this is way too long
            #the instane will not be right as it needs the user id
            progress_photo.photo = request.FILES[file_name]
            progress_photo.save()
            json = {'error':False,'message':'Request successfully completed','RequestResponse':None}
            return JsonResponse(json)
        else:
            json = {'error':True,'message':'No File Recueved/Sent','RequestResponse':None}

    json = {'error':True,'message':'The http request needs to be "POST" not "GET" ','RequestResponse':None}
    return JsonResponse(json)
            
            
        

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.template import loader


def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


 @login_required(login_url='/admin/')
def admin(request):
     user = User.objects.get(username='admin')
     if user != request.user:
         return JsonResponse({'error': 'user is not "admin". only admin can visit this page.'}, status=403)



    template = loader.get_template('admin.html')
    context = {}
    return HttpResponse(template.render(context, request))


 @login_required(login_url='/admin/')
def alice(request):
     user = User.objects.get(username='alice')
     if user != request.user:
         return JsonResponse({'error': 'user is not "alice". only alice can visit this page.'}, status=403)



    template = loader.get_template('alice.html')
    context = {}
    return HttpResponse(template.render(context, request))


 @login_required(login_url='/admin/')
def bob(request):
     user = User.objects.get(username='bob')
     if user != request.user:
         return JsonResponse({'error': 'user is not "bob". only bob can visit this page.'}, status=403)



    template = loader.get_template('bob.html')
    context = {}
    return HttpResponse(template.render(context, request))


def init_eth(request):
    if request.method == 'POST':
        pass



def init_bsc(request):
    if request.method == 'POST':
        pass



def transfer_eth(request):
    if request.method == 'POST':
        form_data = request.POST
        return JsonResponse({})


def transfer_bsc(request):
    if request.method == 'POST':
        form_data = request.POST
        return JsonResponse({})


def alice_burn(request):
    form_data = request.POST
    return JsonResponse({})

from django.http import JsonResponse, HttpResponseNotFound
from django.views import View
from .models import *
from .forms import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class Posts(View):

    def get(self, request, *args, **kwargs):

        posts = Post.objects.all()

        if not posts.exists():
            return JsonResponse({"message": "no blog is avalilable."}, status = 404)
        
        return JsonResponse(list(posts.values()), safe=False)
    
    def post(self, request, *args, **kwargs):

        try:
             data = json.loads(request.body)
        except:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        form = PostsForm(data=data)

        if form.is_valid():
            post = form.save()
            response_data = {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
            }
            return JsonResponse(response_data, status=201)  
        
        else:
            return JsonResponse(form.errors, status=400)
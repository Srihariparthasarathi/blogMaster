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

        posts = Post.objects.all().values("id","title","content")

        if not posts.exists():
            return JsonResponse({"message": "no blog is avalilable."}, status = 404)
        
        return JsonResponse(list(posts), safe=False)
    
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
        


@method_decorator(csrf_exempt, name='dispatch')
class IndividualPost(View):
    def get(self, request, *args, **kwargs):
        post_id = kwargs['id']
       
        try:
             post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"message": f"no blog is avalilable with id: {post_id}."}, status = 404)
            
        post = {
            "id": post.id,
            "title": post.title,
            "contect": post.content
        }

        return JsonResponse(post, safe=False)
    
    def put(self, request, *args, **kwargs):

        post_id = kwargs['id']
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'post not found'}, status = 404)


        try:
             data = json.loads(request.body)
        except:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        

        post.content = data.get("content", post.content)
        post.title = data.get("title", post.title)
        post.save()

        response_data = {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'updated_at': post.updated_at
            }
        
        return JsonResponse(response_data, status=201)  
        

    def delete(self, request, *args, **kwargs):

        post_id = kwargs['id']
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)
        

        post.delete()
        return JsonResponse({'status': 'success', 'message': 'Item deleted successfully.'})
        

@method_decorator(csrf_exempt, name='dispatch')
class CommentPost(View):

    def get(self, request, *args, **kwargs):
        post_id = request.GET.get('post_id')

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)
        

        comments = Comment.objects.filter(post = post).values()
        if not comments.exists():
            return JsonResponse({"message": "no blog is avalilable."}, status = 404)
        
        return JsonResponse(list(comments), safe=False)
    


    def post(self, request, *args, **kwargs):
        
        try:
             data = json.loads(request.body)
        except:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)


        form = CommentForm(data=data)
        if form.is_valid():
            comment = form.save()
            print(comment.post.id)
            data = {
                'id': comment.id,
                'post_id': comment.post.id,
                'comment': comment.content,
                'created_at': comment.created_at,
            }
            return JsonResponse({"data": data}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)        



@method_decorator(csrf_exempt, name='dispatch')
class IndividualComment(View):

    def get(self, request, *args, **kwargs):
        comment_id = kwargs['id']
       
        try:
             comment = Comment.objects.get(id=comment_id)
        except Post.DoesNotExist:
            return JsonResponse({"message": f"no comment is avalilable with id: {comment_id}."}, status = 404)
            
        data = {
            "id": comment.id,
            "post_id": comment.post.id,
            "comment": comment.content
        }

        return JsonResponse(data, safe=False)
    

    def put(self, request, *args, **kwargs):

        comment_id = kwargs['id']
        try:
            comment = Comment.objects.get(id=comment_id)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'comment not found'}, status = 404)


        try:
             data = json.loads(request.body)
        except:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        

        comment.content = data.get("content", comment.content)
        comment.save()

        data = {
            "id": comment.id,
            "post_id": comment.post.id,
            "comment": comment.content
        }
        
        return JsonResponse({"data": data, "message": "comment updated successfully"}, status=201)

    def delete(self, request, *args, **kwargs):

        comment_id = kwargs['id']
        try:
            comment = Comment.objects.get(id=comment_id)
            print(comment)
        except comment.DoesNotExist:
            return JsonResponse({'error': 'comment not found'}, status=404)
        

        comment.delete()
        return JsonResponse({'status': 'success', 'message': 'comment deleted successfully.'})
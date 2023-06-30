from django.shortcuts import render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.db import IntegrityError
from django.shortcuts import HttpResponse
from .models import BlogPost, Profile, Comment
import traceback
from .serializers import BlogPostSerializer, CommentSerializer


# Create your views here.
@api_view(['post'])
@csrf_exempt 
def signupuser(request):
    first_name = request.data['first_name']
    last_name = request.data['last_name']
    username = request.data['username']
    email = request.data['email']
    password = request.data['password']
    bio = request.data['bio']
    
    try:
        user = User.objects.create_user(first_name= first_name, last_name = last_name,username=username, email=email, password=password)
        user.save()
        profile = Profile.objects.create(owner = user, bio = bio)
        profile.save()
        token = Token.objects.create(user = user)
        login(request, user)
        res = {
            "code": 201,
            "token": token.key,
            'message': "registration successful"
        }
        return JsonResponse(res, status = 201, safe=False)
    except IntegrityError:
        res = {
            "code": 403,
            "message": "Are you fucking blind",
        }
        return JsonResponse (res, status = 403, safe=False)
    except:
        print(traceback.print_exc())
        return HttpResponse("Error")
    
    
@api_view(['post'])
@csrf_exempt
def login_user(request): 
    email = request.data['email']
    password = request.data['password']
    
    get_user = User.objects.get(email=email)
    user = authenticate(username=get_user.username, password=password)
    
    if user is not None:
        token = Token.objects.get(user=user)
        res = {
            'token' : token.key,
            'message' : 'User logged in successfully'
        }
        return JsonResponse(res, status = 201, safe=False)
        
    
@api_view(['post'])
@csrf_exempt 
def createPost(request):
    if request.user.is_authenticated:
        user = request.user
        title = request.data['title']
        content = request.data['content']
        post = BlogPost.objects.create(owner = user, title = title, content = content)
        post.save()
        res = {
            'status': 200,
            'message': 'Post created'
        }
        
        return JsonResponse(res, status = 200, safe=False)
    

@api_view(['get'])
def getMyPost(request):
    if request.user.is_authenticated:
        user = request.user
        posts = BlogPost.objects.filter(owner = user)
        serializer = BlogPostSerializer(posts, many = True)
        res = {
            'status': 200,
            'message': 'post retrieved',
            'data': serializer.data
        }
        return JsonResponse(res, status = 200, safe=False)
    else: 
        res = {
            'status': 401,
            'message': 'user not authenticated'
        }
        return JsonResponse(res, status = 401, safe=False)
    
    
@api_view(['get'])
def getAllPost(request):
    if request.user.is_authenticated:
        user = request.user
        posts = BlogPost.objects.all()
        serializer = BlogPostSerializer(posts, many = True)
        res = {
            'status': 200,
            'message': serializer.data
        }
        return JsonResponse(res, status = 200, safe=False)
    else: 
        res = {
            'status': 401,
            'message': 'user not authenticated'
        }
        return JsonResponse(res, status = 401, safe=False)
    
@api_view(['post'])
def likeAPost(request):
    if request.user.is_authenticated: 
        user = request.user
        id = request.data['id']
        post = BlogPost.objects.get(id=int(id))
        post.likes = post.likes + 1
        post.save()
        res = {
            'status': 200,
            'message': 'post liked 👍'
            }
        return JsonResponse(res, status = 200, safe=False)
    else:
        res = {
            'status': 401,
            'message': 'user not authenticated'
        }
        return JsonResponse(res, status = 401, safe=False)

@api_view(['post'])
def commentOnPost(request):
    if request.user.is_authenticated:
        id = request.data['id']
        comment = request.data['comment']
        commenterName = request.data['commenterName']
        blogPostId = BlogPost.objects.get(id = id)
        commentModel = Comment.objects.create(post=blogPostId, comment=comment, commenterName=commenterName)
        commentModel.save()
        res = {
        'status': 200,
        'message': 'Comment posted 👍'
        }
        return JsonResponse(res, status = 200, safe=False)
    else:
        res = {
            'status': 401,
            'massage': 'user not authenticated'
        }
        return JsonResponse(res, status = 401, safe=False)
    
@api_view(['get'])
def getPostComment(request,id):
    if request.user.is_authenticated:
        blogPostId = BlogPost.objects.get(id = id)
        blogComments = Comment.objects.filter(post = blogPostId)
        serializer = CommentSerializer(blogComments, many = True)
        res = {
        'status': 200,
        'message': 'Comment fetched 👍',
        'data': serializer.data
        }
        return JsonResponse(res, status = 200, safe=False)
    else:
        res = {
            'status': 401,
            'message': 'user not authenticated'
        }
        return JsonResponse(res, status = 401, safe=False)
        
        
        
    
    



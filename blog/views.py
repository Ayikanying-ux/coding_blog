from django.http.response import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from .models import Contact,Blog, IpModel,Python,Feedback,BlogComment,Projects
from blog.templatetags import extras
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout

from django.core.paginator import Paginator

import PIL
from PIL import Image
from allauth.socialaccount.models import SocialAccount


def home(request):
    posts = Blog.objects.filter().order_by('-timeStamp')[0:2]
    projects=Projects.objects.filter().order_by('-timeStamp')[0:3]
    print(posts)
    print(projects)
    context={'posts':posts,'projects':projects}
    return render(request,'index.html',context)

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message =request.POST['message']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(message)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, message=message)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request, "contact.html")



def about(request):
    return render(request,'about.html')


def bloghome(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs,2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    return render(request, 'bloghome.html', {'page_obj': page_obj})






def blogpost(request,slug):
    post= Blog.objects.filter(slug=slug)[0]
    comments= BlogComment.objects.filter(post=post, parent=None)
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    ip=get_client_ip(request)
    print(ip)
    if IpModel.objects.filter(ip=ip).exists():
        post.views.add(IpModel.objects.get(ip=ip))
    else:
        IpModel.objects.create(ip=ip)
        post.views.add(IpModel.objects.get(ip=ip))
    context={'post':post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    print(replyDict)
    return render(request,'blogpost.html',context)

def search(request):
    query1=request.POST.get('query')
    if len(query1)>78:
        allPosts=Blog.objects.none()
    else:
        allPostsname= Blog.objects.filter(name__icontains=query1)
        allPostscat= Blog.objects.filter(category__icontains=query1)
        allPosts=  allPostsname.union(allPostscat)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query1}
    return render(request, 'search.html', params)




def get_client_ip(request):
    x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip=x_forwarded_for.split(',')[0]
    else:
        ip=request.META.get('REMOTE_ADDR')
    return ip



def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Blog.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            print("comment aai hai")
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            print("abki baar bhi reply aai hai")
            messages.success(request, "Your reply has been posted successfully")

    return redirect(f"/blogpost/{post.slug}")


def likepost(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = request.POST.get('postid')
        post = get_object_or_404(Blog, sno=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()

        return JsonResponse({'result': result, })







def pythonhome(request):
    allposts=Python.objects.all()
    context={'allposts':allposts}
    return render(request,'pythonhome.html',context)

def pythonpost(request,slug):
    post=Python.objects.filter(slug=slug)[0]
    context={'post':post}
    return render(request,'pythonpost.html',context)




def likeproject(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = request.POST.get('postid')
        project= get_object_or_404(Projects, sno=id)
        if project.likes.filter(id=request.user.id).exists():
            project.likes.remove(request.user)
            project.like_count -= 1
            result = project.like_count
            project.save()
        else:
            project.likes.add(request.user)
            project.like_count += 1
            result = project.like_count
            project.save()

        return JsonResponse({'result': result, })


def projects(request):
    paginator = Paginator(Projects.objects.all(),2)
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    print(projects)
    return render(request, 'projects.html', {'projects': projects})



def project(request,slug):
    project= Projects.objects.filter(slug=slug)[0]
    ip=get_client_ip(request)
    print(ip)
    if IpModel.objects.filter(ip=ip).exists():
        project.views.add(IpModel.objects.get(ip=ip))
    else:
        IpModel.objects.create(ip=ip)
        project.views.add(IpModel.objects.get(ip=ip))
    context={'project':project}
    return render(request,'project.html',context)




def codebook(request):
    return render(request,'codebook.html')
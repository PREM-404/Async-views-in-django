from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from asgiref.sync import sync_to_async
import asyncio
from .models import Subscriber, Article


#helper function
async def async_send_mail(subject, msg, email_list):
    print('Sending mail ...')
    a_send_mail = sync_to_async(send_mail, thread_sensitive=False)
    await a_send_mail(subject, msg, settings.EMAIL_HOST_USER,email_list, fail_silently=False)
    print('Mail sent successfully!')

async def home(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        await sync_to_async(Subscriber.objects.create)(email=email)
        sub = 'Subscription successful!'
        msg = f'Hello {email}, Thanks for subscribing us. Now you will get email notification after we upload article.'
        a_send_mail = sync_to_async(send_mail)
        asyncio.create_task(async_send_mail(sub, msg, [email]))
        return redirect('home')

    elif request.method == 'GET':
        context = {}
        return render(request, 'home.html', context)


async def create_article(request):
    if request.method  == 'GET':
        context = {}
        return render(request, 'article_create.html', context)
    else:
        title = request.POST.get('title')
        description = request.POST.get('description')
        await sync_to_async(Article.objects.create)(title=title, description=description)
        subject = 'New Article Uploaded'
        message = f"New article with title \'{title}\' is just uploaded. Please visit website https://premtamang.com to read it."
        subscribers = await sync_to_async(list)(Subscriber.objects.all())
        email_list = [subscriber.email for subscriber in subscribers]
        asyncio.create_task(async_send_mail(subject, message, email_list))
        return redirect('home')
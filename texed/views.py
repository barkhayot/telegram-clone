from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Chat
from .models import Message
from django.db.models import Q
import re
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def getUsers(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'chat/users.html', context)

def startChat(request, pk):
    r_user = User.objects.get(pk=pk)
    if request.method == 'GET':
        chat = Chat.objects.filter(Q(user_1=request.user, user_2=r_user) | Q(user_2=request.user, user_1=r_user))
        # data = str(chat[0])
        # temp = (re.findall('\d+', data ))
        # chat_id = temp[0]
        if len(chat) == 0:
            chat = Chat.objects.create(
                user_1 = request.user,
                user_2 = r_user
            )
            return redirect('getChat', chat.id)
        else:
            for i in chat:
                chat_id = i.id
                #print(chat_id)
            return redirect('getChat', chat_id) 
    context = {
        'user':r_user
    }
    return render (request, 'chat/startChat.html', context)


def getChats(request):
    search_user = request.GET.get('searchText')
    if search_user:
        users = User.objects.filter(Q(username__contains=search_user)).distinct()
        context = {
            "users": users,
            "search":search_user
        }
        print(users)
        return render(request, 'chat/search.html', context)
    chats = Chat.objects.filter(Q(user_1=request.user) | Q(user_2=request.user))
    context = {
        'chats': chats
    }
    print(chats)
    return render (request, 'chat/getChats.html', context)


def getChat(request, pk):
    search_user = request.GET.get('searchText')
    if search_user:
        users = User.objects.filter(Q(username__contains=search_user)).distinct()
        context = {
            "users": users,
            "search":search_user
        }
        print(users)
        return render(request, 'chat/search.html', context)
    chats = Chat.objects.filter(Q(user_1=request.user) | Q(user_2=request.user))
    chat = get_object_or_404(Chat, pk=pk)
    num = chat.id
    user = request.user.id
    messages = Message.objects.filter(chat_id=chat)
    # if request.method == 'POST':
    #     text = request.POST.get('message')
    #     message = Message.objects.create(
    #         sender = request.user,
    #         chat_id=chat,
    #         message=text
    #     )
    #     return redirect('getChat',num)
    context = {
        'chat':chat,
        'chats':chats,
        'user':user,
        'messages':messages
    }
    return render (request, 'chat/getChat.html', context)

@csrf_exempt
def messageApi(request, pk):
    chat = get_object_or_404(Chat, pk=pk)
    messages = Message.objects.filter(chat_id=chat.id)
    user = request.user.username
    new = request.user
    data = []
    for i in messages:
        vals = {}
        vals['chat_id'] =i.chat_id.id
        vals['id'] = i.id
        vals['user'] = user
        vals['sender'] = i.sender.username
        vals['message'] = i.message
        vals['created_at'] = i.created_at
        data.append(vals)
        huh = str(i.created_at)
        
    if request.method == 'POST':
        post_body = json.loads(request.body) 
        text = post_body['message']
        message = Message.objects.create(
            sender = new,
            chat_id=chat,
            message=text
        )
    return JsonResponse(data, safe=False)

from operator import itemgetter
from django.db.models import Max


def chatApi(request):
    hottest_cakes = Chat.objects.filter(Q(user_1=request.user) | Q(user_2=request.user)).annotate(most_recent=Max('chat__created_at')).order_by('-most_recent')
    print(hottest_cakes)
    chats = Chat.objects.filter(Q(user_1=request.user) | Q(user_2=request.user)).annotate(most_recent=Max('chat__created_at')).order_by('-most_recent')
    #Chat.objects.filter(Q(user_1=request.user) | Q(user_2=request.user))
    #.annotate(Max('chat__created_at'))
    #order_by('-chat__created_at').distinct('chat__id')
    #chats.distinct()
    user = request.user.username
    data = []
    for i in chats:
        message_count = Message.objects.filter(chat_id=i.id).order_by('created_at')
        vals = {}
        vals['id'] = i.id
        vals['user'] = user
        vals['user_1'] = i.user_1.username
        vals['user_2'] = i.user_2.username
        vals['count'] = len(message_count)
        data.append(vals)
        # 
    #newlist = sorted(data, key=itemgetter('count'), reverse=True)
    # print(data)

    return JsonResponse(data, safe=False)


def test(request):
    return render(request, 'chat/search.html')


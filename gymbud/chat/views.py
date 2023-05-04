# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView,

)
from .models import (
    MessageModel,
    DialogsModel,
    UploadedFile
)
from user_mgmt.models import Profile, User
from .serializers import serialize_message_model, serialize_dialog_model, serialize_file_model
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status, viewsets
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.paginator import Page, Paginator
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.urls import reverse_lazy
from django.forms import ModelForm
import json
from user_mgmt.models import Matches
from user_mgmt.serializers import DisplayMatchedUsers
from rest_framework.permissions import IsAuthenticated
from .permissions import DisplayMatchesPermission, MessagePermission
from rest_framework.views import APIView

class UsersListView(viewsets.ModelViewSet):
    #permission_classes = [DisplayMatchesPermission]
    serializer_class = DisplayMatchedUsers
    
    def get_queryset(self):
        return Matches.objects.filter(user__id=self.request.user.id)



class MessagesModelList(ListView):

    #permission_classes = [MessagePermission]
    http_method_names = ['get', ]
    paginate_by = getattr(settings, 'MESSAGES_PAGINATION', 500)
    
    def get_queryset(self):
        
        instance = User.objects.get(id=self.request.user.id)
        

        if self.kwargs.get('dialog_with'):
            
            qs = MessageModel.objects \
                .filter(Q(recipient=instance, sender=self.kwargs['dialog_with']) |
                        Q(sender=instance, recipient=self.kwargs['dialog_with'])) \
                .select_related('sender', 'recipient')
        else:
            qs = MessageModel.objects.filter(Q(recipient=instance) |
                                             Q(sender=instance)).prefetch_related('sender', 'recipient', 'file')

        return qs.order_by('-created')

    def render_to_response(self, context, **response_kwargs):
        user_pk = self.request.user.id
      
        data = [serialize_message_model(i, user_pk) for i in context['object_list']]
        page: Page = context.pop('page_obj')
        paginator: Paginator = context.pop('paginator')
        return_data = {
            'page': page.number,
            'pages': paginator.num_pages,
            'data': data
        }
        return JsonResponse(return_data, **response_kwargs)


class DialogsModelList(ListView):

    #permission_classes = [MessagePermission]
    http_method_names = ['get', ]
    paginate_by = getattr(settings, 'DIALOGS_PAGINATION', 20)

    def get_queryset(self):
        
        #if get_or_none(Matches, user=)

        qs = DialogsModel.objects.filter(Q(user1_id=self.request.user.id) | Q(user2_id=self.request.user.id)) \
            .select_related('user1', 'user2')
        return qs.order_by('-created')

    def render_to_response(self, context, **response_kwargs):
        user_pk = self.request.user.id
        data = [serialize_dialog_model(i, user_pk) for i in context['object_list']]
        page: Page = context.pop('page_obj')
        paginator: Paginator = context.pop('paginator')
        return_data = {
            'page': page.number,
            'pages': paginator.num_pages,
            'data': data
        }
        return JsonResponse(return_data, **response_kwargs)



class ChatSelfInfoView(APIView):

    #permission_classes = [IsAuthenticated]
    def get(self, request, **response_kwargs):
        user = self.request.user
        
        data = {
            "username": user.first_name,
            "pk": str(user.pk)
        }
        return JsonResponse(data, **response_kwargs)

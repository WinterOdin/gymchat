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
from rest_framework import permissions
from .permissions import DisplayMatchesPermission, MessagePermission



class UsersListView(viewsets.ModelViewSet):
    permission_classes = [DisplayMatchesPermission]
    serializer_class = DisplayMatchedUsers
    
    def get_queryset(self):
        return Matches.objects.filter(user__id=self.request.user.id)



class MessagesModelList(ListView):

    permission_classes = [MessagePermission]
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

    permission_classes = [MessagePermission]
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


class SelfInfoView(LoginRequiredMixin, DetailView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):

        return self.request.user

    def render_to_response(self, context, **response_kwargs):
        user: AbstractBaseUser = context['object']
        
        data = {
            "username": user.first_name,
            "pk": str(user.pk)
        }
        return JsonResponse(data, **response_kwargs)


# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
# MAX_UPLOAD_SIZE = getattr(settings, 'MAX_FILE_UPLOAD_SIZE', 5242880)

# class UploadForm(ModelForm):
#     # TODO: max file size validation
#     # def check_file(self):
#     #     content = self.cleaned_data["file"]
#     #     content_type = content.content_type.split('/')[0]
#     #     if (content._size > MAX_UPLOAD_SIZE):
#     #         raise forms.ValidationError(_("Please keep file size under %s. Current file size %s")%(filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(content._size)))
#     #     return content
#     #
#     # def clean(self):

#     class Meta:
#         model = UploadedFile
#         fields = ['file']


# class UploadView(LoginRequiredMixin, CreateView):
#     http_method_names = ['post', ]
#     model = UploadedFile
#     form_class = UploadForm

#     def form_valid(self, form: UploadForm):
#         self.object = UploadedFile.objects.create(uploaded_by=self.request.user.id, file=form.cleaned_data['file'])
#         return JsonResponse(serialize_file_model(self.object))

#     def form_invalid(self, form: UploadForm):
#         context = self.get_context_data(form=form)
#         errors_json: str = context['form'].errors.get_json_data()
#         return HttpResponseBadRequest(content=json.dumps({'errors': errors_json}))

from django.conf import settings
from rest_framework.viewsets import GenericViewSet
from core.exceptions import RequestNotAllow, UserNotAuthError, UserNotAllowError
from core.view.mixins.drf_action_mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin,  DestroyModelMixin


class DRFActionBaseView(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    need_login = True
    http_method_names = ['get', 'post', 'put', 'patch']

    def get_serializer_class(self):
        if self.need_login and self.request.user.is_anonymous and settings.ENABLE_AUTH:
            raise UserNotAuthError
        if self.need_login and not self.request.user.is_allow_department:
            raise UserNotAllowError
        serializer_class = self.serializer_list.get(self.action, None)
        if not serializer_class:
            raise RequestNotAllow
        return serializer_class


from django.conf import settings
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import GenericViewSet
from core.exceptions import RequestNotAllow, UserNotAuthError, UserNotAllowError
from core.view.mixins.drf_mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin,  DestroyModelMixin





class DRFBaseView(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    need_login = True
    renderer_classes = (JSONRenderer,)
    http_method_names = ['get', 'post', 'put', 'patch']

    def get_serializer_class(self):
        serializer_class = self.serializer_list.get(self.action, None)
        if not serializer_class:
            raise RequestNotAllow
        return serializer_class



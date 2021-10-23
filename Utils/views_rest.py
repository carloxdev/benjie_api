# Django's Libraries
from django.core.exceptions import ImproperlyConfigured

# Third-party Libraries
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated


class ApiView(viewsets.GenericViewSet):
    permission_classes = (AllowAny, )
    request = None
    params = {}
    instance = None
    app_class = None
    serializer_list_class = None

    def set_Params(self, _request):
        self.params = _request.parser_context['kwargs']

    def run_Controller(self, _function, _data=None):
        if self.app_class is None:
            raise ImproperlyConfigured(
                "Favor de especificar una app_class"
            )

        if _function is None:
            raise ImproperlyConfigured(
                "Favor de especificar el metodo del Controller"
            )

        return getattr(self.app_class, _function)(
            self.request,
            self.params,
            _data,
            self.instance
        )


class ListApiView(object):
    list_method = None

    def list(self, request, *args, **kwargs):
        self.request = request
        self.set_Params(request)

        queryset = self.run_Controller(self.list_method)
        if queryset:
            queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        if self.serializer_list_class:
            serializer = self.serializer_list_class(queryset, many=True)

        else:
            serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class CreateApiView(object):
    create_method = None

    def create(self, request, *args, **kwargs):
        self.request = request
        self.set_Params(request)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.run_Controller(
            self.create_method,
            _data=serializer.validated_data
        )

        if self.serializer_list_class:
            serializer = self.serializer_list_class(instance)

        else:
            serializer = self.get_serializer(instance)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class RetrieveApiView(object):
    retrieve_method = None

    def retrieve(self, request, *args, **kwargs):
        self.request = request
        self.set_Params(request)

        instance = self.run_Controller(self.retrieve_method)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UpdateApiView(object):
    retrieve_method = None
    update_method = None

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.request = request
        self.set_Params(request)

        partial = kwargs.pop('partial', False)
        self.instance = self.run_Controller(self.retrieve_method)
        serializer = self.get_serializer(
            self.instance,
            data=request.data,
            partial=partial
        )

        serializer.is_valid(raise_exception=True)
        self.run_Controller(self.update_method, serializer.validated_data)

        if getattr(self.instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            self.instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class DeleteApiView(object):
    delete_method = None

    def destroy(self, request, *args, **kwargs):
        self.request = request
        self.set_Params(request)

        self.instance = self.run_Controller(self.delete_method)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SecurityApiView(ApiView):
    permission_classes = (IsAuthenticated, )

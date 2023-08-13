from django.contrib.postgres.aggregates import ArrayAgg
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from admin.movies.models import Filmwork

MOVIES_COUNT_ON_PAGE = 50


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self, **kwargs):
        return []

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return JsonResponse({})


class Movies(MoviesApiMixin, BaseListView):
    paginate_by = MOVIES_COUNT_ON_PAGE

    def get_paginator(self, queryset, **kwargs):
        return Paginator(queryset, self.paginate_by, 0, False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'paginator': self.get_paginator(self.get_queryset()),
            'page_obj': 0,
            'is_paginated': True,
            'results': list(self.get_queryset()),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'results': self.get_queryset(uuid=kwargs['uuid']),
        }
        return context

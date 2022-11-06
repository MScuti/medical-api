from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns


class BasicRouter(DefaultRouter):
    def __init__(self, *args, **kwargs):
        self.common_prefix = kwargs.pop('common_prefix') if 'common_prefix' in kwargs else ""
        super().__init__(*args, **kwargs)

    def _get_urls(self):
        """
        Use the registered viewsets to generate a list of URL patterns.
        """
        ret = []
        common_prefix = ""
        if self.common_prefix:
            common_prefix = self.common_prefix if self.common_prefix.endswith(r'/') else self.common_prefix+ "\\"

        for prefix, viewset, basename in self.registry:
            lookup = self.get_lookup_regex(viewset)
            routes = self.get_routes(viewset)

            for route in routes:

                # Only actions which actually exist on the viewset will be bound
                mapping = self.get_method_map(viewset, route.mapping)
                if not mapping:
                    continue

                # Build the url pattern
                regex = route.url.format(
                    prefix=common_prefix +prefix,
                    lookup=lookup,
                    trailing_slash=self.trailing_slash
                )

                # If there is no prefix, the first part of the url is probably
                #   controlled by project's urls.py and the router is in an app,
                #   so a slash in the beginning will (A) cause Django to give
                #   warnings and (B) generate URLS that will require using '//'.
                if not prefix and regex[:2] == '^/':
                    regex = '^' + regex[2:]

                initkwargs = route.initkwargs.copy()
                initkwargs.update({
                    'basename': basename,
                    'detail': route.detail,
                })

                view = viewset.as_view(mapping, **initkwargs)
                name = route.name.format(basename=basename)
                ret.append(url(regex, view, name=name))

        return ret

    def get_urls(self):
        urls = self._get_urls()
        if self.include_root_view:
            view = self.get_api_root_view(api_urls=urls)
            root_url = url(r'^$', view, name=self.root_view_name)
            urls.append(root_url)
        if self.include_format_suffixes:
            urls = format_suffix_patterns(urls)
        return urls
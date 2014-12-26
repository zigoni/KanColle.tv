from django.views.generic import ListView
from kc_doujin.models import KcComic
from kc_doujin.config import KC_DOUJIN_ITEM_PER_PAGE


class KcComicList(ListView):
    paginate_by = KC_DOUJIN_ITEM_PER_PAGE
    context_object_name = 'comics'
    template_name = 'kc_doujin/list.html'

    def get_queryset(self):
        queryset = KcComic.objects.filter(is_active=True)

        if self.request.user.is_authenticated():
            qfilter = self.request.session.get('comic_filter', 'normal')
        else:
            qfilter = 'normal'

        if qfilter == 'normal':
            queryset = queryset.filter(is_r18=False)
        elif qfilter == 'r18':
            queryset = queryset.filter(is_r18=True)
        elif qfilter == 'all':
            pass
        else:
            queryset = queryset.filter(is_r18=False)

        order = self.request.session.get('comic_order', 'time')
        if order == 'time':
            return queryset.order_by('-publish_time')
        elif order == 'otime':
            return queryset.order_by('publish_time')
        elif order == 'clicks':
            return queryset.order_by('-clicks')
        else:
            return queryset

    def get_context_data(self, **kwargs):
        c = super(KcComicList, self).get_context_data(**kwargs)
        c['active'] = 'doujin'
        return c
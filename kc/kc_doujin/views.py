from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from kc_doujin.models import KcComic
from kc_doujin.config import KC_DOUJIN_ITEM_PER_PAGE


class KcComicList(ListView):
    paginate_by = KC_DOUJIN_ITEM_PER_PAGE
    context_object_name = 'comics'
    template_name = 'kc_doujin/list.html'

    def get_queryset(self):
        queryset = KcComic.objects.filter(is_active=True)

        if self.request.user.is_authenticated():
            qfilter = self.request.session.get('doujin_filter', 'normal')
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

        order = self.request.session.get('doujin_order', 'time')
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


class KcComicDetail(DetailView):
    context_object_name = 'c'
    template_name = 'kc_doujin/detail.html'

    def get_queryset(self):
        queryset = KcComic.objects.filter(is_active=True)
        if not self.request.user.is_authenticated():
            queryset = queryset.filter(is_r18=False)
        return queryset

    def get_object(self):
        obj = super(KcComicDetail, self).get_object()
        flag = self.request.session.get('cm'+str(obj.id), None)
        if flag is None:
            obj.clicks += 1
            obj.save(update_fields=['clicks'])
            self.request.session['cm'+str(obj.id)] = True
        return obj

    def get_context_data(self, **kwargs):
        context = super(KcComicDetail, self).get_context_data(**kwargs)
        context['active'] = 'doujin'
        page = int(self.kwargs.get('page', '1'))
        context['current'] = page
        if page > 1:
            context['previous'] = page - 1
        if page < self.object.pages:
            context['next'] = page + 1
        #fullscreen = self.kwargs.get('fullscreen', False)
        #if fullscreen:
        #    self.template_name = 'kc_doujin/detail_fullscreen.html'
        return context


def orderby(request, order):
    request.session['doujin_order'] = order
    return redirect('kc-doujin')


@login_required
def filterby(request, qfilter):
    request.session['doujin_filter'] = qfilter
    return redirect('kc-doujin')


@login_required
def search(request):
    q = request.GET.get('q', '')
    if len(q) < 2:
        context = {
            'active': 'doujin',
            'title': '搜索失败',
            'message': '请至少输入两个字符进行搜索',
        }
        return render(request, 'warning.html', context)
    else:
        queryset = KcComic.objects.filter(title__contains=q)
        context = {
            'active': 'doujin',
            'queryset': queryset,
            'q': q,
        }
        return render(request, 'kc_doujin/search.html', context)
import django_filters
from django_filters import CharFilter
from django.db.models import Q
from django.forms.widgets import TextInput
from .models import Forum, Topic, Thread



class ForumFilter(django_filters.FilterSet):

    forum = CharFilter(method='filter_by_all_name_fields', label='', widget=TextInput(attrs=
    {

        'placeholder': 'Search forums',
        'class': 'searchbox',

    }))

    #description = CharFilter(field_name='desc', lookup_expr='icontains')

    class Meta:
        model = Forum
        fields = '__all__'
        exclude = ['published', 'created_at', 'slug', 'owner', 'category', 'name', 'desc']

    def filter_by_all_name_fields(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(desc__icontains=value)
        )

    # CHOICES = (
    #     ('ascending', 'Ascending'),
    #     ('descending', 'Descending')
    # )
    #
    # ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES, method='filter_by_order')



        # {
        #
        #     'name': ['icontains'],
        #     'desc': ['icontains'],
        #
        # }

    # def filter_by_order(self, queryset, name, value):
    #     expression = 'created_at' if value == 'ascending' else '-created_at'
    #     return queryset.order_by(expression)

class TopicFilter(django_filters.FilterSet):

    topic = CharFilter(method='filter_by_all_name_fields', label='', widget=TextInput(attrs=
    {

        'placeholder': 'Search topics in forum',
        'class': 'searchbox',

    }))

    class Meta:
        model = Topic
        fields = '__all__'
        exclude = ['name', 'forum', 'slug', 'desc', 'creator', 'created_at', 'last_activity', 'views']

    def filter_by_all_name_fields(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(desc__icontains=value))


class ThreadFilter(django_filters.FilterSet):

    topic = CharFilter(method='filter_by_all_name_fields', label='', widget=TextInput(attrs=
    {

        'placeholder': 'Search thread in topic',
        'class': 'searchbox',

    }))

    class Meta:
        model = Thread
        fields = '__all__'
        exclude = ['name', 'topic', 'content', 'creator', 'created_at', 'last_activity', 'views']

    def filter_by_all_name_fields(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(content__icontains=value))

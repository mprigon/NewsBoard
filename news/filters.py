from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter, CharFilter
from django.forms import DateTimeInput


class CommentFilter(FilterSet):
    added_after = DateTimeFilter(  # календарь для поиска дата после
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            # для тега HTML - <input> elements of type datetime-local create input controls that
            # let the user easily enter both a date and a time, including the year,
            # month, and day as well as the time in hours and minutes.
            # datetime-local выводит календарь
            attrs={'type': 'datetime-local'},
        ),
    )

    text = CharFilter(
        field_name='text',
        lookup_expr='icontains',
        label='Text',
    )

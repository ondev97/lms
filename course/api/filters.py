import django_filters
from django.db.models import Q
from ..models import Subject,Course,Enrollment

class SubjectFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='custom_search')

    class Meta:
        model = Subject
        fields = ['search']

    def custom_search(self,queryset,name,value):
        return queryset.filter(
            Q(subject_name__icontains=value)
        )

class CourseFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='custom_search')

    class Meta:
        model = Course
        fields = ['search']

    def custom_search(self,queryset,name,value):
        return queryset.filter(
            Q(course_name__icontains=value)
        )

class EnrollFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='custom_search')

    class Meta:
        model = Enrollment
        fields = ['search']

    def custom_search(self,queryset,name,value):
        return queryset.filter(
            Q(course_name__icontains=value)
        )
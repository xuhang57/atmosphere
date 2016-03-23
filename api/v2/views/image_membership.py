from django.db.models import Q
import django_filters

from core.models import ApplicationMembership as ImageMembership
from service.machine import add_membership, remove_membership
from api.v2.serializers.details import ImageMembershipSerializer
from api.v2.views.base import AuthViewSet


class Filter(django_filters.FilterSet):
    image_id = django_filters.MethodFilter(action='filter_by_uuid')
    created_by = django_filters.MethodFilter(action='filter_owner')

    def filter_owner(self, queryset, value):
        return queryset.filter(
            Q(application__created_by__username=value)
        )

    def filter_by_uuid(self, queryset, value):
        # NOTE: Remove this *HACK* once django_filters supports UUID as PK
        return queryset.filter(application__id=value)

    class Meta:
        model = ImageMembership
        fields = ['image_id', 'created_by']


class ImageMembershipViewSet(AuthViewSet):

    """
    API endpoint that allows image memberships to be viewed
    """
    queryset = ImageMembership.objects.none()
    serializer_class = ImageMembershipSerializer
    filter_class = Filter

    def get_queryset(self):
        """
        Show only memberships for the given users groups
        """
        return ImageMembership.available_for(self.request.user)

    def perform_destroy(self, instance):
        remove_membership(instance.image, instance.group)
        instance.delete()

    def perform_create(self, serializer):
        image = serializer.validated_data['image']
        group = serializer.validated_data['group']
        add_membership(image, group)
        serializer.save()

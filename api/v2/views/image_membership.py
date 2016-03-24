from django.db.models import Q
import django_filters

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from core.models import ApplicationMembership as ImageMembership
from core.models import Application, Group
from service.machine import add_image_membership, remove_image_membership
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
        #FIXME: Performance problems! 8seconds/result!
        remove_image_membership(instance.application, instance.group)
        instance.delete()

    def create(self, request):
        data = request.data

        serializer = self.get_serializer_class()(data=data, context={'request':request})
        if not serializer.is_valid():
            return Response(
                "Error(s) occurred while "
                "creating image membership: %s" % (serializer.errors,),
                status=status.HTTP_400_BAD_REQUEST)
        # ASSERT: Data is assumed to be valid. serializer has *NOT* been saved.
        validated_data = serializer.initial_data
        image = Application.objects.get(uuid=validated_data['image'])
        group = Group.objects.get(uuid=validated_data['group'])
        add_image_membership(image, group)
        return Response(status=status.HTTP_201_CREATED)

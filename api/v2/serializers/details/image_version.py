from core.models import ApplicationVersion as ImageVersion
from core.models import Application as Image
from rest_framework import serializers
from api.v2.serializers.summaries import (
    LicenseSummarySerializer,
    UserSummarySerializer,
    ImageSummarySerializer,
    IdentitySummarySerializer,
    ImageVersionSummarySerializer)
from api.v2.serializers.fields import (
    ProviderMachineRelatedField, ModelRelatedField)


class ImageVersionSerializer(serializers.HyperlinkedModelSerializer):

    """
    Serializer for ApplicationVersion (aka 'image_version')
    """
    # NOTE: Implicitly included via 'fields'
    # id, application
    parent = ImageVersionSummarySerializer()
    # name, change_log, allow_imaging
    licenses = LicenseSummarySerializer(many=True, read_only=True)  # NEW
    membership = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
        many=True)  # NEW
    user = UserSummarySerializer(source='created_by')
    identity = IdentitySummarySerializer(source='created_by_identity')
    machines = ProviderMachineRelatedField(many=True)
    image = ModelRelatedField(
        source='application',
        queryset=Image.objects.all(),
        serializer_class=ImageSummarySerializer,
        style={'base_template': 'input.html'})
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField(allow_null=True)

    class Meta:
        model = ImageVersion
        view_name = 'api:v2:providermachine-detail'
        fields = ('id', 'parent', 'name', 'change_log',
                  'image', 'machines', 'allow_imaging',
                  'licenses', 'membership',
                  'user', 'identity',
                  'start_date', 'end_date')

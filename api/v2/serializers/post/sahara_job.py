from rest_framework import serializers


class JobSerializer(serializers.Serializer):
    """
    """
    # Flags
    uuid = serializers.CharField(max_length=36, read_only=True)

    class Meta:
        fields = "__all__"

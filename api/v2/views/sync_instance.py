from api.v2.views.base import AuthViewSet
from rest_framework.response import Response
from rest_framework import status
from service.tasks.monitoring import monitor_instances_for


class SyncInstanceViewSet(AuthViewSet):

    """
    API endpoint that calls monitor_instances_for.
    """

    def get(self, request, pk=None):
        return self.list(request)

    def list(self, request, *args, **kwargs):
        results = []
        user = self.request.user
        results = [{"name": user.username, "project": user.projects.first().name}]
        monitor_instances_for(1, [user.username], [user.projects.first().name])
        return Response(results, status=status.HTTP_200_OK)


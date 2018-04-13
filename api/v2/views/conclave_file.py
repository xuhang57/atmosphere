from api.v2.views.base import AuthViewSet

from rest_framework.response import Response
from rest_framework import status
import os

class FileViewSet(AuthViewSet):

    """
    API endpoint that allows Files to be viewed or edited.
    """

    def get(self, request, pk=None):
        return self.list(request)

    def list(self, request, *args, **kwargs):
        files = os.listdir("/shared_directory")
        results = []
        for f in files:
            if f.startswith("uploaded_script"):
                results.append({"fileName": f})
        return Response(results, status=status.HTTP_200_OK)

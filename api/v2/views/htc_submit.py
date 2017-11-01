from api.v2.views.base import AuthViewSet

from rest_framework.response import Response
from rest_framework import status
import os

import pyslurm

class HTCViewSet(AuthViewSet):

    """
    API endpoint that allows HTC Submit to be viewed or edited.
    """

    def create(self, request):
        data = self.request.data
        job_script = data['file']
        job_name = job_script['fileName']
        saved_file = "/shared_directory/" + str(job_name)
        output_name = str(job_name) + ".out"
        data_file = data['data']
        data_name = data_file['fileName']
        job_id, ok = pyslurm.slurm_submit_batch_job({'script': saved_file})
        return Response({'submit_batch_job': job_id}, status=status.HTTP_200_OK)

    def get(self, request, pk=None):
        return self.list(request)

    def list(self, request, *args, **kwargs):
        files = os.listdir("/opt/dev/atmosphere")
        results = []
        for f in files:
            if not f.startswith('slurm'):
                continue
            results.append({"fileName": f})
        return Response(results, status=status.HTTP_200_OK)


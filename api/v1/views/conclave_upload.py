import os
from api.v1.views.base import AuthAPIView
from rest_framework.parsers import FileUploadParser
import uuid

from rest_framework import status
from rest_framework.response import Response
import requests

from threepio import logger


class ConclaveUpload(AuthAPIView):

    """
    API endpoint that allows HIL Node to be viewed or edited.
    """
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        saved_file, file_num = self.handle_uploaded_file(file_obj)
        #rc = pyslurm.slurm_submit_batch_job({'script':saved_file,
        #'nodelist':'compute1', 'output': 'giji-output%d.out' % (file_num)})
        return Response({'submit_batch_job': "submitted"}, status=status.HTTP_204_NO_CONTENT)
        #return Response({'submit_batch_job': rc}, status=status.HTTP_204_NO_CONTENT)

    def handle_uploaded_file(self, f):
        current = 0
        for filename in os.listdir("/shared_directory"):
            current += 1
        with open('/shared_directory/uploaded_script%d.py' % (current), 'wb+') as destination:
            for line in f.readlines():
                if "WebKitFormBoundary" not in line:
                    if "Content" not in line:
                        if line.replace("\r", "").rstrip():
                            logger.debug("inline")
                            destination.write(line.replace("\r", ""))
        file_loc = '/shared_directory/uploaded_script%d.py' % (current)
        return file_loc, current

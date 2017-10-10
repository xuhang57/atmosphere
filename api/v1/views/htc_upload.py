import os
from api.v1.views.base import AuthAPIView
from rest_framework.parsers import FileUploadParser
import uuid

from rest_framework import status
from rest_framework.response import Response
import requests

import pyslurm

class HTCUpload(AuthAPIView):

    """
    API endpoint that allows Files to be uploaded.
    """
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        saved_file, file_num = self.handle_uploaded_file(file_obj)
        rc = pyslurm.slurm_submit_batch_job({'script':saved_file,
        'nodelist':'compute1', 'output': 'giji-output%d.out' % (file_num)})
        return Response({'submit_batch_job': rc}, status=204)

    def handle_uploaded_file(self, f):
        current = 0
        #we have to manually create this directory so far
        for filename in os.listdir("/opt/giji_upload_scripts"):
            current += 1
        with open('/opt/giji_upload_scripts/uploaded_script%d.sh' % (current), 'wb+') as destination:
            for line in f.readlines():
                if not "WebKitFormBoundary" in line:
                    if not "Content" in line:
                        if line.replace("\r", "").rstrip():
                            destination.write(line.replace("\r", ""))
        #currently, we have to manually create this directory. Looking for a solution
        file_loc = '/opt/giji_upload_scripts/uploaded_script%d.sh' % (current)
        return file_loc, current


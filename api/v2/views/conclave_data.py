from api.v2.views.base import AuthViewSet
from rest_framework.response import Response
from rest_framework import status
import os

import json
import requests  # http://docs.python-requests.org/en/master/
from datetime import datetime


class DataSourceViewSet(AuthViewSet):

    """
    API endpoint that allows Data to be viewed or edited.
    """

    def get(self, request, pk=None):
        return self.list(request)

    def list(self, request, *args, **kwargs):
        dataverse_server = 'http://128.31.24.163:8080' # no trailing slash
        api_key = 'we can get the api key from the Cloud Dataverse test server'
        if not request.GET.get("doi_id"):
            return Response([], status=status.HTTP_200_OK)
        doi_id = request.GET.get("doi_id")
        doi_id_list = []
        doi_id_list.append(doi_id)
        persistent_id_list = doi_id_list[0].split(',')

        info = {} # will be a dictionary formatted as {persistentId: {'containerName': containerName, 'title': title}, ...}

        for persistent_id in persistent_id_list:
            # --------------------------------------------------
            # Get Dataset metadata using persistent Id
            # --------------------------------------------------
            # curl -X GET http://localhost:8080/api/datasets/:persistentId/?persistentId=$persistentId
            header = {'X-Dataverse-key': api_key}
            url_dataset = '{0}/api/datasets/:persistentId/versions/:latest?persistentId={1}'.format(dataverse_server, persistent_id)
            # -------------------
            # Make the request
            # -------------------
            # print('-' * 40)
            # print('making request: %s' % url_dataset)
            r = requests.get(url_dataset, headers=header)

            # -------------------
            # Print the response
            # -------------------

            container_name = r.json()['data']['storageIdentifier'].split(':')[-1]
            title = r.json()['data']['metadataBlocks']['citation']['fields'][0]['value']
            files = {} # dictionary formatted {id1: name1, id2: name2, ...}
            for file in r.json()['data']['files']:
                storageId = file['dataFile']['storageIdentifier']
                ident = storageId[storageId.rindex(':')+1:]
                files[ident] = file['dataFile']['filename']
            info[persistent_id] = {'containerName': container_name, 'title': title, 'files': files}

        results = []
        for i in info:
            results.append({"containerName": info[i]['containerName'], "title": info[i]['title'], "files": '\n'.join(info[i]['files'].values())})
        return Response(results, status=status.HTTP_200_OK)

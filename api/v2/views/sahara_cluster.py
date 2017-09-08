from api.v2.views.base import AuthViewSet, AuthOptionalViewSet

from core.models import AtmosphereUser, Identity
from keystoneauth1.identity import v3
from rtwo.drivers.openstack_network import NetworkManager
from rtwo.drivers.openstack_user import UserManager
from keystoneauth1 import session

from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import detail_route

from threepio import logger

class ClusterViewSet(AuthViewSet):

    """
    API endpoint that allows cluster to be viewed or edited.
    """

    def create(self, request):
        user = self.request.user
        data = self.request.data
        plugin_name = data['pluginName']
        if plugin_name == "vanilla":
            hadoop_version = "2.7.1"
        elif plugin_name == "spark":
            hadoop_version = "1.6.0"
        elif plugin_name == "storm":
            hadoop_version = "1.0.1"
        else:
            raise Exception("Cannot find the plugin")
        name = data['clusterName']
        cluster_size = data['clusterSize']
        identity = Identity.objects.get(created_by=user)
        all_creds = identity.get_all_credentials()
        auth_url = all_creds.get('auth_url')
        if not "/v3" in auth_url:
            auth_url += "/v3"
        project_name = identity.project_name()
        token = all_creds['ex_force_auth_token']
        token_auth=v3.Token(
            auth_url=auth_url,
            token=token,
            project_name=project_name,
            project_domain_id="default")
        ses = session.Session(auth=token_auth)
        network_driver = NetworkManager(session=ses)
        user_driver = UserManager(auth_url=auth_url, auth_token=token, project_name=project_name, domain_name="default", session=ses, version='v3')
        kp = user_driver.nova.keypairs.list()[0]
        net_id= network_driver.neutron.list_networks()['networks'][0]['id']
        image = None
        for img in user_driver.glance.images.list():
            if "Sahara: Spark 1.6.0 OCATA" in img.name:
                image = img
                image_id= image.id
        cluster_template = network_driver.sahara.cluster_templates.list()
        if cluster_template:
            ct = network_driver.sahara.cluster_templates.list()[1]
        else:
            node_group_templates = network_driver.sahara.node_group_templates.list()
            if node_group_templates:
                ct = self._create_cluster_template(network_driver)
            else:
                self._create_node_group_template(network_driver)
                ct = self._create_cluster_template(network_driver)

        cluster = self._create_cluster(network_driver, plugin_name, hadoop_version, ct, image_id, kp, name, net_id)
        results = [{"id": cluster.id, "clusterName": name, "pluginName": plugin_name, "hadoop_version": hadoop_version}]
        return Response(results, status=status.HTTP_201_CREATED)


    def get(self, request, pk=None):
        return self.list(request)

    def list(self, request):
        user = self.request.user
        network_driver, user_driver = self.get_network_and_user_driver(user)
        clusters_list = network_driver.sahara.clusters.list()
        results = []
        for cluster in clusters_list:
            try:
                ip = cluster.node_groups[0]['instances'][0]['management_ip']
                results.append({"clusterName": cluster.name, "id": cluster.id,
                "pluginName": cluster.plugin_name, "clusterStatus":
                cluster.status, "clusterMasterIP": ip})
            except:
                results.append({"clusterName": cluster.name, "id": cluster.id,
                "pluginName": cluster.plugin_name, "clusterStatus":
                cluster.status, "clusterMasterIP": "not associated"})
        return Response(results, status=status.HTTP_200_OK)
        return Response(results, status=status.HTTP_200_OK)


    def retrieve(self, request, pk=None):
        url_list = request.path.split("/")
        cluster_id = url_list[-1]
        user = self.request.user
        network_driver, user_driver = self.get_network_and_user_driver(user)
        try:
            cluster = network_driver.sahara.clusters.get(cluster_id)
            results = []
            try:
                ip = cluster.node_groups[0]['instances'][0]['management_ip']
                results.append({"clusterName": cluster.name, "id": cluster.id, "pluginName": cluster.plugin_name, "clusterStatus": cluster.status, "clusterMasterIP": ip})
                return Response(results, status=status.HTTP_200_OK)
            except:
                results.append({"clusterName": cluster.name, "id": cluster.id,
                "pluginName": cluster.plugin_name, "clusterStatus":
                cluster.status, "clusterMasterIP": "not associated"})
                return Response(results, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        user = self.request.user
        network_driver, user_driver = self.get_network_and_user_driver(user)
        clusters_list = network_driver.sahara.clusters.list()
        results = []
        for cluster in clusters_list:
            results.append({"clusterName": cluster.name, "id": cluster.id, "pluginName": cluster.plugin_name, "clusterStatus": "Luanched"})
        return Response(results, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        user = self.request.user
        network_driver, user_driver = self.get_network_and_user_driver(user)
        url_list = request.path.split("/")
        cluster_id = url_list[-1]
        network_driver.sahara.clusters.delete(str(cluster_id))
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def get_network_and_user_driver(self, user):
        identity = Identity.objects.get(created_by=user)
        all_creds = identity.get_all_credentials()
        auth_url = all_creds.get('auth_url')
        if not "/v3" in auth_url:
            auth_url += "/v3"
        project_name = identity.project_name()
        token = all_creds['ex_force_auth_token']
        token_auth=v3.Token(
            auth_url=auth_url,
            token=token,
            project_name=project_name,
            project_domain_id="default")
        ses = session.Session(auth=token_auth)
        network_driver = NetworkManager(session=ses)
        user_driver = UserManager(auth_url=auth_url, auth_token=token, project_name=project_name, domain_name="default", session=ses, version='v3')
        return network_driver, user_driver

    def _create_node_group_template(self, network_driver):
        node_processes_master = ["namenode", "master"]
        node_processes_worker = ["datanode", "slave"]
        network_driver.sahara.node_group_templates.create(plugin_name="spark", hadoop_version="1.6.0", node_processes=node_processes_master, flavor_id = '2', name ='test-master-template-spark-cli')
        network_driver.sahara.node_group_templates.create(plugin_name="spark", hadoop_version="1.6.0", node_processes=node_processes_worker, flavor_id = '2', name ='test-worker-template-spark-cli')

    def _create_cluster_template(self, network_driver):
        worker, master = None, None
        for template in network_driver.sahara.node_group_templates.list():
            if "worker" in template.name:
                worker = template
            else:
                master = template
        node_groups = [{"name": "worker", "count": 2, "node_group_template_id": str(worker.id)}, {"name": "master", "count": 1, "node_group_template_id": str(master.id)}]
        ct = network_driver.sahara.cluster_templates.create(plugin_name="spark", hadoop_version="1.6.0", node_groups=node_groups, name="test-cluster-template-cli")
        return ct

    def _create_cluster(self, network_driver, plugin_name, hadoop_version, ct, image_id, kp, name, net_id):
        cluster = network_driver.sahara.clusters.create(plugin_name=plugin_name, hadoop_version=hadoop_version, cluster_template_id=str(ct.id), default_image_id=str(image_id), user_keypair_id=str(kp.id), name=name, net_id=str(net_id))
        return cluster


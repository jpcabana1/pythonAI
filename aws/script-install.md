sudo swapoff -a
sudo vi /etc/sysctl.conf


vm.max_map_count=262144

export OPENSEARCH_INITIAL_ADMIN_PASSWORD=OpenSearchftd@2024
curl https://localhost:9200 -ku admin:$OPENSEARCH_INITIAL_ADMIN_PASSWORD

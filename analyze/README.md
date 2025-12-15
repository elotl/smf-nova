# Listing Kubernetes Objects in a Helm Chart

This folder provides a script to list the Kind, Namespace and Names of Kubernetes Objects in a given Kubernetes manifest file.

## Usage

We use the helm template command to first generate all the manifests associated with the helm chart.


```
helm template prom prometheus-community/kube-prometheus-stack --namespace monitoring  > kube-prometheus-stack-manifests.yaml
```


We then execute this script on the generated manifest file:


```
./list-k8s-objects.sh kube-prometheus-stack-manifests.yaml
```

This is a snippet of the output produced:

```
% ./list-k8s-objects.sh kube-prometheus-stack-manifests.yaml                                                                  
KIND	NAMESPACE	NAME
ServiceAccount                  monitoring                 prom-grafana
ServiceAccount                  monitoring                 prom-kube-state-metrics
ServiceAccount                  monitoring                 prom-prometheus-node-exporter
ServiceAccount                  monitoring                 prom-kube-prometheus-stack-alertmanager
ServiceAccount                  monitoring                 prom-kube-prometheus-stack-operator
ServiceAccount                  monitoring                 prom-kube-prometheus-stack-prometheus
Secret                          monitoring                 prom-grafana
Secret                          monitoring                 alertmanager-prom-kube-prometheus-stack-alertmanager
ConfigMap                       monitoring                 prom-grafana-config-dashboards
ConfigMap                       monitoring                 prom-grafana
ConfigMap                       monitoring                 prom-kube-prometheus-stack-grafana-datasource
ConfigMap                       monitoring                 prom-kube-prometheus-stack-alertmanager-overview
...
ConfigMap                       monitoring                 prom-kube-prometheus-stack-prometheus
ConfigMap                       monitoring                 prom-kube-prometheus-stack-proxy
ConfigMap                       monitoring                 prom-kube-prometheus-stack-scheduler
ConfigMap                       monitoring                 prom-kube-prometheus-stack-workload-total
ClusterRole                     unknown-or-cluster-scoped  prom-grafana-clusterrole
ClusterRole                     unknown-or-cluster-scoped  prom-kube-state-metrics
ClusterRole                     unknown-or-cluster-scoped  prom-kube-prometheus-stack-operator
ClusterRole                     unknown-or-cluster-scoped  prom-kube-prometheus-stack-prometheus
ClusterRoleBinding              unknown-or-cluster-scoped  prom-grafana-clusterrolebinding
ClusterRoleBinding              unknown-or-cluster-scoped  prom-kube-state-metrics
ClusterRoleBinding              unknown-or-cluster-scoped  prom-kube-prometheus-stack-operator
ClusterRoleBinding              unknown-or-cluster-scoped  prom-kube-prometheus-stack-prometheus
Role                            monitoring                 prom-grafana
RoleBinding                     monitoring                 prom-grafana
Service                         monitoring                 prom-grafana
Service                         monitoring                 prom-kube-state-metrics
Service                         monitoring                 prom-prometheus-node-exporter
...
Service                         monitoring                 prom-kube-prometheus-stack-operator
Service                         monitoring                 prom-kube-prometheus-stack-prometheus
DaemonSet                       monitoring                 prom-prometheus-node-exporter
Deployment                      monitoring                 prom-grafana
Deployment                      monitoring                 prom-kube-state-metrics
Deployment                      monitoring                 prom-kube-prometheus-stack-operator
Alertmanager                    monitoring                 prom-kube-prometheus-stack-alertmanager
MutatingWebhookConfiguration    unknown-or-cluster-scoped  prom-kube-prometheus-stack-admission
Prometheus                      monitoring                 prom-kube-prometheus-stack-prometheus
PrometheusRule                  monitoring                 prom-kube-prometheus-stack-alertmanager.rules
PrometheusRule                  monitoring                 prom-kube-prometheus-stack-config-reloaders
...
PrometheusRule                  monitoring                 prom-kube-prometheus-stack-etcd
PrometheusRule                  monitoring                 prom-kube-prometheus-stack-prometheus-operator
PrometheusRule                  monitoring                 prom-kube-prometheus-stack-prometheus
ServiceMonitor                  monitoring                 prom-grafana
ServiceMonitor                  monitoring                 prom-kube-state-metrics
ServiceMonitor                  monitoring                 prom-prometheus-node-exporter
...
ServiceMonitor                  monitoring                 prom-kube-prometheus-stack-kubelet
ServiceMonitor                  monitoring                 prom-kube-prometheus-stack-operator
ServiceMonitor                  monitoring                 prom-kube-prometheus-stack-prometheus
ValidatingWebhookConfiguration  unknown-or-cluster-scoped  prom-kube-prometheus-stack-admission
ServiceAccount                  monitoring                 prom-grafana-test
ServiceAccount                  monitoring                 prom-kube-prometheus-stack-admission
ConfigMap                       monitoring                 prom-grafana-test
ClusterRole                     unknown-or-cluster-scoped  prom-kube-prometheus-stack-admission
ClusterRoleBinding              unknown-or-cluster-scoped  prom-kube-prometheus-stack-admission
Role                            monitoring                 prom-kube-prometheus-stack-admission
RoleBinding                     monitoring                 prom-kube-prometheus-stack-admission
Pod                             monitoring                 prom-grafana-test
Job                             monitoring                 prom-kube-prometheus-stack-admission-create
Job                             monitoring                 prom-kube-prometheus-stack-admission-patch
```


 

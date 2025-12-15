# Listing Kubernetes Objects in a Helm Chart

This folder provides a Python script to list the Kind, Namespace, Names and Labels of Kubernetes Objects in a given Kubernetes manifest file.

## Usage

We use the helm template command to first generate all the manifests associated with a helm chart.


```
% helm template dashboard  kubernetes-dashboard/kubernetes-dashboard --namespace monitoring > dashboard-manifests-monitoring.yaml 
```

We then execute this script on the generated manifest file:


```
% python list-k8s-objects.py dashboard-manifests-monitoring.yaml | column -t            
```

This is a snippet of the output produced:

```
KIND                NAMESPACE                  NAME                                            LABELS
ServiceAccount      monitoring                 dashboard-kong                                  app.kubernetes.io/name=kong,helm.sh/chart=kong-2.52.0,app.kubernetes.io/instance=dashboard,app.kubernetes.io/managed-by=Helm,app.kubernetes.io/version=3.9
ServiceAccount      unknown-or-cluster-scoped  dashboard-kubernetes-dashboard-api              helm.sh/chart=kubernetes-dashboard-7.14.0,app.kubernetes.io/instance=dashboard,app.kubernetes.io/managed-by=Helm,app.kubernetes.io/part-of=kubernetes-dashboard

ConfigMap           unknown-or-cluster-scoped  dashboard-kubernetes-dashboard-web-settings     helm.sh/chart=kubernetes-dashboard-7.14.0,app.kubernetes.io/instance=dashboard,app.kubernetes.io/managed-by=Helm,app.kubernetes.io/part-of=kubernetes-dashboard
...
ClusterRole         unknown-or-cluster-scoped  dashboard-kubernetes-dashboard-metrics-scraper  helm.sh/chart=kubernetes-dashboard-7.14.0,app.kubernetes.io/instance=dashboard,app.kubernetes.io/managed-by=Helm,app.kubernetes.io/part-of=kubernetes-dashboard
...
ClusterRoleBinding  unknown-or-cluster-scoped  dashboard-kubernetes-dashboard-metrics-scraper  helm.sh/chart=kubernetes-dashboard-7.14.0,app.kubernetes.io/instance=dashboard,app.kubernetes.io/managed-by=Helm,app.kubernetes.io/part-of=kubernetes-dashboard
...
Role                unknown-or-cluster-scoped  dashboard-kubernetes-dashboard-api              helm.sh/chart=kubernetes-dashboard-7.14.0,app.kubernetes.io/instance=dashboard,app.kubernetes.io/managed-by=Helm,app.kubernetes.io/part-of=kubernetes-dashboard
...
RoleBinding         unknown-or-cluster-scoped  dashboard-kubernetes-dashboard-web              helm.sh/chart=kubernetes-dashboard-7.14.0,app.kubernetes.io/instance=dashboard,app.kubernetes.io/managed-by=Helm,app.kubernetes.io/part-of=kubernetes-dashboard
...
Service             monitoring                 dashboard-kong-proxy                            app.kubernetes.io/name=kong,helm.sh/chart=kong-2.52.0,app.kubernetes.io/instance=dashboard,app.kubernetes.io/managed-by=Helm,app.kubernetes.io/version=3.9,enable-metrics=true
...
Deployment          monitoring                 dashboard-kong                                  app.kubernetes.io/name=kong,helm.sh/chart=kong-2.52.0,app.kubernetes.io/instance=dashboard,app.kubernetes.io/managed-by=Helm,app.kubernetes.io/version=3.9,app.kubernetes.io/component=app
```














```
helm template prom prometheus-community/kube-prometheus-stack --namespace monitoring  > kube-prometheus-stack-manifests.yaml
```





```
python list-k8s-objects.py dashboard-manifests.yaml | column -t
```


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


## Usage without labels


The provided script can also be run with the `--exclude-labels` flag to leave out the labels.


```
% python list-k8s-objects.py dashboard-manifests-monitoring.yaml --exclude-labels | column -t
```

Sample of the output:

```
KIND                NAMESPACE                  NAME
ServiceAccount      monitoring                 dashboard-kong
Secret              unknown-or-cluster-scoped  dashboard-kubernetes-dashboard-csrf
ConfigMap           unknown-or-cluster-scoped  kong-dbless-config
ConfigMap           unknown-or-cluster-scoped  dashboard-kubernetes-dashboard-web-settings
ClusterRole         unknown-or-cluster-scoped  dashboard-kubernetes-dashboard-metrics-scraper
ClusterRoleBinding  unknown-or-cluster-scoped  dashboard-kubernetes-dashboard-metrics-scraper
Role                unknown-or-cluster-scoped  dashboard-kubernetes-dashboard-api
RoleBinding         unknown-or-cluster-scoped  dashboard-kubernetes-dashboard-web
Service             monitoring                 dashboard-kong-proxy
Deployment          monitoring                 dashboard-kong
``` 

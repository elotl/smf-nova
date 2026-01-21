# Deploy SMF to span multiple clusters


## Prerequisites

1. Cilium Cluster Mesh installed on both Nova workload clusters, configured for connectivity between the clusters."
2. Nova installed with `multi-cluster-capacity` option. If Nova is already installed, then the Nova scheduler deployment can be edited  on the Nova control plane to add this option.

```
kubectl --context ${NOVA_HOSTINGCLUSTER_CONTEXT} edit deploy nova-scheduler  -n elotl
```

The nova-scheduler manifest with the added flags will look like this:
```
    spec:
      containers:
      - args:
        - -c
        - cp /etc/nova-config/kubeconfig /etc/nova/kubeconfig && /nova-scheduler --v=3
          --rbac-controller-enabled --luna-management-enabled --multi-cluster-capacity
        command:
```


## 1. Schedule Policy Creation


Before installing a new SMF instance, delete any stale workloads and policies. Prior schedule policies can be viewed as follows:

```
kubectl --context ${NOVA_CONTROLPLANE_CONTEXT} get schedulepolicies
```

If there are any previously scheduled SMF workloads delete them too.


### A. Setup Environment Variables

Set environment variable `SMF_REPO_ROOT` to the root of this repo.
```
export SMF_REPO_ROOT=$HOME/github.com/elotl/smf-nova
```

Set environment variable `SMF_NAMESPACE_1` to the namespace in which to run the SMF application.
```
export SMF_NAMESPACE_1=smf-namespace1
```

Set env var `NOVA_HOSTINGCLUSTER_CONTEXT` to the context of the Nova hosting cluster.
```
export NOVA_HOSTINGCLUSTER_CONTEXT=selvi-nova
```

Set env var `NOVA_CONTROLPLANE_CONTEXT` to the context of the Nova hosting cluster.
```
export NOVA_CONTROLPLANE_CONTEXT=nova
```

Set env variables to access the workload cluster context names:

```
export K8S_CLUSTER_CONTEXT_1=selvik-12232
export K8S_CLUSTER_CONTEXT_2=selvik-30337
```

### B. Create Spread Policy 

This Spread policy will be used for resources that are needed on both clusters. This will include:

1) Namespace: The namespace within which all Application components will be placed on both clusters.
2) Configmaps, Secrets, ServiceAccounts, Services, etc: All resources that will be needed by the deployment that will span both clusters as well as the workloads that will remain on the primary cluster.

```
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f ${SMF_REPO_ROOT}/policies/multicluster-span-policies/smf-namespace-policy.yaml
```

Verify that the policy was created:

```
% kubectl --context ${NOVA_CONTROLPLANE_CONTEXT} get schedulepolicies
NAME            AGE
smf-ns-policy   24s
```

Create the `smf` namespace.
```
envsubst < ${SMF_REPO_ROOT}/policies/multicluster-span-policies/smf-namespace.yaml | kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f -
```

Verify that the namespace has been duplicated to all the workload clusters.
```
kubectl --context=${K8S_CLUSTER_CONTEXT_1} get ns
kubectl --context=${K8S_CLUSTER_CONTEXT_2} get ns
```

```
% kubectl --context=${K8S_CLUSTER_CONTEXT_1} get ns
NAME                                             STATUS   AGE
...
smf-namespace1                                   Active   1s

% kubectl --context=${K8S_CLUSTER_CONTEXT_2} get ns
NAME                                             STATUS   AGE
...
smf-namespace1                                   Active   4s
```

### C. Schedule policy for SMF components on the primary-cluster

All Kubernetes resources of the SMF app that are to be deployed on the primary workload cluster will be placed using a label-based 
specific-cluster policy. The following policy matches all resources with the label: `app: primary`. 

```
envsubst < ${SMF_REPO_ROOT}/policies/multicluster-span-policies/smf-primary-policy.yaml | kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f -
```

Verify that the policy was created:
```
% kubectl --context ${NOVA_CONTROLPLANE_CONTEXT} get schedulepolicies
NAME                 AGE
smf-ns-policy        3m55s
smf-primary-policy   4s
```

### D. Schedule policy for the SMF Deployment that will span multiple clusters

The Kubernetes `deployment` that will span two Nova workload clusters will be placed using a `Fill-and-Spill` Schedule Policy.

This policy matches all resources with the label: `app: span-multiple`. A `Fill and Spill` policy allows users to place workloads on a list of clusters ordered by **priority**. For the Schedule policy snippet shown below, clusters are listed in the order: cluster-1 and then cluster-2. So workload pods will first be placed on cluster-1 and any pods that cannot be placed on cluster-1 will be placed on cluster-2.

```
  orderedClusterSelector:
    matchExpressions:
      - key: kubernetes.io/metadata.name
        operator: In
        values: [cluster-1, cluster-2]
```

The policy uses these env variables whose values correspond to the names that were given during Nova agent install in the workload clusters:
```
export NOVA_WORKLOAD_CLUSTER_1=selvik-onprem
export NOVA_WORKLOAD_CLUSTER_2=selvik-cloud 
```

```
envsubst < ${SMF_REPO_ROOT}/policies/multicluster-span-policies/smf-fill-and-spill-policy.yaml | kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f -
```

Verify that the policy was created:
```
% kubectl --context ${NOVA_CONTROLPLANE_CONTEXT} get schedulepolicies
NAME                        AGE
smf-fill-and-spill-policy   6m32s
smf-ns-policy               15m
smf-primary-policy          12m
```

## 2. Install the SMF helm chart 

```
helm install --kube-context ${NOVA_CONTROLPLANE_CONTEXT} ...
```

## 3. Adding necessary labels

We add the following labels to ensure the objects are placed as intended:

1. Add label `app: primary` to all the resources that need to be on the primary-cluster only. 
2. Add label `app: smf-spread` to the common Kubernetes objects that will be needed by workloads on the primary cluster as well as the Deployment that will span across the two clusters.
3. Add label `app: span-multiple` to the Deployment that will need to span across two workload clusters.


## 4. Update App configuration for Cilium Cluster Mesh.

When Cilium Cluster Mesh is used, services whose pods span multiple clusters as well as Services that need to be accessed from the other clusters should be made a Global Service.

A Kubernetes `Service` can be converted to a `Global Service` by including the following annotation:

```
 service.cilium.io/global: "true".
```

You can read more about Global Services here: (Cilium Load Balancing with Global Services)[https://docs.cilium.io/en/stable/network/clustermesh/services/#load-balancing-with-global-services]


Edit the Services associated with the deployment to be spanned and add the above annotation.

```
kubectl --context ${NOVA_CONTROLPLANE_CONTEXT} edit service -n ${SMF_NAMESPACE_1} <smf-deployment-service> 
```

Also update any other services that would need to be accessed from both clusters.

## 5. Verify Application deployment

```
kubectl --context=${K8S_CLUSTER_CONTEXT_1} get pods -n ${SMF_NAMESPACE_1}
kubectl --context=${K8S_CLUSTER_CONTEXT_2} get pods -n ${SMF_NAMESPACE_1}
```


# Deploy SMF to span multiple clusters


## Prerequisites

1. Cilium Cluster Mesh installed on both Nova workload clusters
2. Nova installed with `multi-cluster-capacity` option. If Nova is already installed, then the Nova scheduler deployment can be editted  on the Nova control plane to add this option.

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


Before installing a new SMF instance, delete any stale workloads and policies. Prior schedule policie can be viewed as follows:.

```
kubectl --context ${NOVA_CONTROLPLANE_CONTEXT} get schedulepolicies
```

If there are any previously scheduled workloads delete them too.


### Setup Environment Variables

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

### Create Namespace policy.

```
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f ./policies/multicluster-span-policies/smf-namespace-policy.yaml
```

Create the `smf` mamespace.
```
envsubst < ${SMF_REPO_ROOT}/deploy-scripts/namespace.yaml | kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f -
```

Verify Namespace has been Duplicated to all the workload clusters.
```
kubectl --context=${K8S_CLUSTER_CONTEXT_1} get ns
kubectl --context=${K8S_CLUSTER_CONTEXT_2} get ns
```

### Schedule policy for SMF components on the primary-cluster

All Kubernetes resources of the SMF app that are to be deployed on the primary workload cluster will be placed using a label-based 
specific-cluster policy. The folowing policy matches all resources with the label: `app: primary`. 

```
envsubst < ${SMF_REPO_ROOT}/policies/multicluster-span-policies/smf-primary-policy.yaml | kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f -
```

### Schedule policy for SMF Deployment that will span mulitple clusters

The Kubernetes `deployment` that will span two Nova workload clusters as well as any other dependent objects this deployment needs (secrets, configmaps, etc) will be placed using a Fill-and-Spill Schedule Policy.

This policy matches all resources with the label: `app: span-multiple`. 

```
envsubst < ${SMF_REPO_ROOT}/policies/multicluster-span-policies/smf-fill-and-spill-policy.yaml | kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f -
```

## 3. Install the SMF helm chart 

```
helm install --kube-context ${NOVA_CONTROLPLANE_CONTEXT} ...
```

## 4. Adding necessary labels

We add the following labels to ensure the objects are placed as intended:

1. Add label `app: primary` to all resources except the Deployment (and its corresponding) that will need to span across two clusters.
2. Add label `app: span-multiple` to the Deployment that will need to span across two workload clusters.
3. Add label `app: smf-spread` to the Service of the Deployment that will need to span across two clusters.


## Update App configuration for Cilium Cluster Mesh.

When Cilium Cluster Mesh is used, services whose pods may span multiple clusters are expected to include the following annotation to make it a `Global Service`.

```
 service.cilium.io/global: "true".
```

You can read more about Global Services here: (Cilium Load Balancing with Global Services)[https://docs.cilium.io/en/stable/network/clustermesh/services/#load-balancing-with-global-services]


Edit the service associated with the deployment to be spanned and add the above annotation.

```
kubectl --context ${NOVA_CONTROLPLANE_CONTEXT} edit service -n ${SMF_NAMESPACE_1} <smf-deployment-service> 
```

## 4. Verify Application deployment

```
kubectl --context=${K8S_CLUSTER_CONTEXT_1} get all -n ${SMF_NAMESPACE_1}
kubectl --context=${K8S_CLUSTER_CONTEXT_2} get all -n ${SMF_NAMESPACE_1}
```


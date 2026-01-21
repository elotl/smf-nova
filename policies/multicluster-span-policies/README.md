# Deploy SMF to span multiple clusters


## Prerequisites

1. Cilium Cluster Mesh installed on both Nova workload clusters


## Install Nova with `multi-cluster-capacity` option

If Nova is already installed, then you can edit the Nova scheduler deployment on the Nova control plane and add this option.

```
kubectl --context ${} edit nova-scheduler -n elotl 
```

The nova-scheduler manifest with the added flags will look like this:


## 1. Schedule Policy Creation

### Clean up any stale workloads and policies


If there are prior schedule policies, list them and delete them.

```
kubectl --context ${NOVA_CONTROL_PLANE} get schedulepolicies
```

If there are any previously scheduled workloads delete them.

### Setup needed environment variables.

Set environment variable `SMF_REPO_ROOT` to the root of this repo.
```
export SMF_REPO_ROOT=$HOME/github.com/elotl/smf-nova
```

Set environment variable `SMF_NAMESPACE_1` to the namespace in which to run the SMF application.
```
export SMF_NAMESPACE_1=smf-namespace1
```

### Create Namespace policy.

```
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f ./policies/multicluster-span-policies/namespace-policy.yaml
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

The Kubernetes `deployment` that will span two Nova workload clusters will be placed using a Fill-and-Spill Schedule Policy.

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

When Cilium Cluster Mesh is used, services whose pods may span multiple clusters are expected to include the following annotation:

```
 service.cilium.io/global: "true".
```

Edit the service and add the above annotation.

```
kubectl --context ${NOVA_CONTROLPLANE_CONTEXT} edit service <smf-deployment-service> 
```

## 4. Verify Application deployment

```
kubectl --context=${K8S_CLUSTER_CONTEXT_1} get all -n smf-namespace1
kubectl --context=${K8S_CLUSTER_CONTEXT_2} get ns
```


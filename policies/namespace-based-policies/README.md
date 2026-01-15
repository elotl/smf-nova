# Deploying SMF using a namespace-based policy

Using this README all namespace-scoped resources in the SMF app will be placed using a namespace-based policy.
All cluster-scoped resources in the SMF app, will need to be placed using a label-based policy. Using labels is necessary since we need a way to identify (or mark) cluster-scoped Kubernetes objects that belong to the SMF app that will need to be scheduled by Nova.


## 1. Create Nova Schedule policies

Set environment variable `SMF_REPO_ROOT` to the root of this repo.
```
export SMF_REPO_ROOT=$HOME/github.com/elotl/smf-nova
```

Set environment variable `SMF_NAMESPACE_1` to the namespace in which to run the SMF application.
```
export SMF_NAMESPACE_1=smf-namespace1
```

### Create a policy for cluster-scoped resources

```
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f ${SMF_REPO_ROOT}/policies/namespace-based-policies/policy-for-cluster-scoped-resources.yaml
```
Cluster-scoped resources will be placed via a spread policy on all workload clusters.

### Create a policy for namespace-scoped resources

```
envsubst < ${SMF_REPO_ROOT}/policies/namespace-based-policies/policy-for-namespace-scoped-resources.yaml  | kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f -
```
Namespace-scoped resources will be placed via a specific-cluster policy on one workload cluster.

## 2. Create the namespace for SMF 

```
envsubst < ${SMF_REPO_ROOT}/manifests/smf_namespace.yaml  | kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f -
```
The namespace's name is defined by the env variable: `${SMF_NAMESPACE_1}`. Ensure that this env variable is defined.

## 3. Install the SMF helm chart 

```
helm install --kube-context ${NOVA_CONTROLPLANE_CONTEXT} ... 
```

## 4. Add labels for only cluster-scoped resources

Label all the cluster-scoped objects in the SMF app with `app: smf-cs-resources`. This includes resources such as such as clusterroles, clusterrolebindings, CustomResourceDefinitions, etc.
```
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} label crd ${SMF_CRD} app=smf-cs-resources
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} label clusterrole ${SMF_CLUSTERROLE} app=smf-cs-resources
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} label clusterrolebinding ${SMF_CLUSTERROLEBINDING} app=smf-cs-resources
...
```

Nova will now place all the namespace-scoped resources in the namespace: `${SMF_NAMESPACE_1}` and the labelled cluster-scoped resources in the Nova workload cluster, specified in the policy: `${NOVA_WORKLOAD_CLUSTER_1}`



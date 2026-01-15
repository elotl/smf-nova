# Deploying SMF using a namespace-based policy

Using this README all namespace-scoped resources in the SMF app will be placed using a namespace-based policy.
All cluster-scoped resources in the SMD app, will need to be placed using a label-based policy. Using labels is necessart since we need a way to identify or mark Kubernetes objects that belong to the SMF app (that will then be scheduled by Nova).


## 1. Create Nova Schedule policies

### Create a policy for cluster-scoped resources

```
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f ./policies/namespace-based-policies/policy-for-cluster-scoped-resources.yaml
```

### Create a policy for namespace-scoped resources

```
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f ./policies/namespace-based-policies/policy-for-cluster-scoped-resources.yaml
```

## 2. Create the namespace for SMF 

```
envsubst < ${SMF_REPO_ROOT}/manifests/smf_namespace.yaml  | kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f -
```
The namespace's name is defined by the env variable: `${SMF_NAMESPACE_1}`

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



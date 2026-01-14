# Deploying SMF using a primarily namespace-based policy

All namespace-scoped resources will be placed using a namespace-based policy.


All cluster-scoped resources, will be placed using a label-based policy. Using labels is still necessary since we do need a way to identify or mark Kubernetes objects that are cluster-scoped and will need to be scheduled by Nova.


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

## 3. Install SMF helm chart 

```
helm install <smf-helm-chart>
```

## 4. Add labels for only cluster-scoped resources


Label only cluster-scoped objects in the SMF app with `app: smf-cs-resources`.
This includes resources such as such as clusterroles, clusterrolebindings, CustomResourceDefinitions, etc.
```
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} label crd ${SMF_CRD} app.kubernetes.io/component=smf-cs-resources
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} label clusterrole ${SMF_CLUSTERROLE} app.kubernetes.io/component=smf-cs-resources
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} label clusterrolebinding ${SMF_CLUSTERROLEBINDING} app.kubernetes.io/component=smf-cs-resources
...
```


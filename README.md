# smf-nova
Deploy SMF to Nova cluster fleet

### Spread/Duplicate Namespace(s)

Set environment variable SMF_REPO_ROOT to the root of this repo.
```
export SMF_REPO_ROOT=$HOME/github.com/elotl/smf-nova
```

Set environment variable SMF_NAMESPACE_1 to namespace associated with SMF application.
```
export SMF_NAMESPACE_1=smf-namespace1
```

Create Namespace policy.
```
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f ./policies/namespace-policy.yaml
```

Create Namespace.
```
envsubst < ${SMF_REPO_ROOT}/deploy-scripts/namespace.yaml | kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f -
```

Verify Namespace has been Duplicated to all the workload clusters.
```
kubectl --context=${K8S_CLUSTER_CONTEXT_1} get ns
kubectl --context=${K8S_CLUSTER_CONTEXT_2} get ns
```

### Schedule Policy 1: Spread/Duplicate

Run one instance of SMF on every workload cluster in the fleet.

Create Spread/Duplicate Schedule Policy.
```
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f ./policies/smf-spread-duplicate-policy.yaml
```

You should see the new schedule policy on Nova.
```
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} get schedulepolicies
```

#### If using Helm, add a `commonLabels` `app.kubernetes.io/component=smf`

```
helm install --kube-context ${NOVA_CONTROLPLANE_CONTEXT} ... --set commonLabels."app\.kubernetes\.io/component"=smf
```

If `commonLabels` are not supported, please install Helm chart and then `kubectl label` Objects as described below.

#### If using manifest, apply manifest and then label Objects

Apply SMF manifest.
```
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f ${SMF_YAML}
```

Label SMF Objects with `app.kubernetes.io/component=smf`.
```
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} label crd ${SMF_CRD} app.kubernetes.io/component=smf
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} label deployment ${SMF_DEPLOYMENT} app.kubernetes.io/component=smf
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} label clusterrole ${SMF_CLUSTERROLE} app.kubernetes.io/component=smf
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} label clusterrolebinding ${SMF_CLUSTERROLEBINDING} app.kubernetes.io/component=smf
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} label serviceaccount ${SMF_SERVICEACCOUNT} app.kubernetes.io/component=smf
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} label role ${SMF_ROLE} app.kubernetes.io/component=smf
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} label rolebinding ${SMF_ROLEBINDING} app.kubernetes.io/component=smf
...
```

Wait for one instance of SMF to come up on each of the workload clusters.

### Schedule Policy 2: Schedule SMF to a single workload cluster

### Schedule Policy 3: Availability-based scheduling

Schedule SMF to any cluster with available resources. SMF will land on one cluster with available resources.



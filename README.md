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

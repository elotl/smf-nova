# smf-nova
Deploy SMF to Nova cluster fleet

### Step 0: Spread/Duplicate Namespace(s)

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

### Step 1: Schedule SMF to a single workload cluster

Schedule SMF to ${NOVA_WORKLOAD_CLUSTER_1}.

#### Create a simple Schedule Policy

```
envsubst < ${SMF_REPO_ROOT}/policies/simple-policy.yaml | kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f -
```

You should see the new schedule policy `simple-policy` in Nova.
```
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} get schedulepolicies
```

#### Schedule SMF to Nova

##### If using Helm, add a `commonLabels`

Add `commonLabels` `app.kubernetes.io/component=smf`.
```
helm install --kube-context ${NOVA_CONTROLPLANE_CONTEXT} ... --set commonLabels."app\.kubernetes\.io/component"=smf
```

If `commonLabels` are not supported, please install Helm chart and then `kubectl label` Objects as described below.

##### If using manifest, apply manifest and then label Objects

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

### Step 2: Verify SMF is scheduled to the target workload cluster

One unit of SMF should be running on ${NOVA_WORKLOAD_CLUSTER_1}.

### Step 3 (Optional): Update Schedule Policy

Edit Schedule Policy to change target cluster from ${NOVA_WORKLOAD_CLUSTER_1} to ${NOVA_WORKLOAD_CLUSTER_2}.

```
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} edit schedulepolicy simple-policy
```

You should see SMF move from ${NOVA_WORKLOAD_CLUSTER_1} to ${NOVA_WORKLOAD_CLUSTER_2}.

### Step 4: Explore advanced Schedule Policies

#### Spread/Duplicate

Run one instance of SMF on every workload cluster in the fleet.

Create Spread/Duplicate Schedule Policy.
```
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f ./policies/spread-duplicate-policy.yaml
```

You should see the new schedule policy on Nova.
```
kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} get schedulepolicies
```
One instance of SMF should be running on each of the workload clusters.

#### Availability-based scheduling

Schedule SMF to any cluster with available resources. SMF will land on one cluster with available resources. One instance of SMF should be running on one of the clusters with sufficient resources.

Policy Template coming soon.

#### Stretched scheduling

Schedule each tier of SMF on a different cluster. For example, schedule 1 unit of front end on workload cluster 1, 1 unit of app tier on workload cluster 2, 1 unit of database on workload cluster 2.

Policy Template coming soon.

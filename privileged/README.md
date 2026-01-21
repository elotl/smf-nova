# Scheduling Privileged Containers via Nova

## Update Kubernetes API server configuration 

We will first edit the Kubernetes API server to allow privileged containers to be scheduled. By default this is disabled.
Please note that the API server is running on the Nova hosting cluster (not the default `nova` context).

```
kubectl --context ${NOVA_HOSTING_CLUSTER_CONTEXT} edit deploy apiserver  -n elotl 
```

Add the following line to the `template::spec::containers::command` field:

```
        - --allow-privileged=true
``` 

This is what it will look like:
```
  template:
    metadata:
      creationTimestamp: null
      labels:
        component: apiserver
    spec:
      containers:
      - command:
        - kube-apiserver
        - --authorization-mode=RBAC
        - --allow-privileged=true
        - --client-ca-file=/etc/kubernetes/pki/ca.crt
        - --enable-admission-plugins=NodeRestriction
        - --enable-bootstrap-token-auth=true
```

## Example Privileged Pod and Policy Creation


### Create schedule policy

We first create the Nova Schedule Policy:

```
% kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f policy-for-privileged-pod.yaml 
schedulepolicy.policy.elotl.co/policy-priv-pod created

% kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} get schedulepolicies
NAME              AGE
policy-priv-pod   4s
```

### Create namespace

Next, we create the namespace needed for the privileged pod:

```
% kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f abc-namespace.yaml
namespace/abc created

% kubectl --context=${K8S_CLUSTER_CONTEXT_1} get namespaces                             
NAME                                             STATUS   AGE
abc                                              Active   74s

% kubectl --context=${K8S_CLUSTER_CONTEXT_1} get namespaces                              
NAME                                             STATUS   AGE
abc                                              Active   77s
```



### Create privileged pods

Finally, we create a sample privileged pod and check that it is scheduled successfully on both Nova workload clusters:


```
% kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f privileged-abc-busybox.yaml 
pod/privileged-demo created

% kubectl --context=${K8S_CLUSTER_CONTEXT_1} get pods -n abc                                     
NAME              READY   STATUS    RESTARTS   AGE
privileged-demo   1/1     Running   0          2s

% kubectl --context=${K8S_CLUSTER_CONTEXT_1} get pods -n abc                            
NAME              READY   STATUS    RESTARTS   AGE
privileged-demo   1/1     Running   0          10s
```


## Appendix

Without the API server configuration `--allow-privileged=true`, Nova Control Plane will not be able to run this privileged pod and will display this error:

```
% kubectl --context=${NOVA_CONTROLPLANE_CONTEXT} apply -f privileged-abc-busybox.yaml
The Pod "privileged-demo" is invalid: spec.containers[0].securityContext.privileged: Forbidden: disallowed by cluster policy
```


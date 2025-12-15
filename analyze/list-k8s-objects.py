#!/usr/bin/env python3

import sys, yaml, argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="List Kubernetes objects from a YAML manifest.")
parser.add_argument("manifest", help="Path to Kubernetes YAML manifest (supports multiple documents)")
parser.add_argument("--exclude-labels", action="store_true", help="Exclude the LABELS column from output")
args = parser.parse_args()

# Load and process YAML
with open(args.manifest) as f:
    rows = []
    for doc in yaml.safe_load_all(f):
        if not isinstance(doc, dict) or "kind" not in doc or "name" not in doc.get("metadata", {}):
            continue
        meta = doc["metadata"]
        kind = doc["kind"]
        namespace = meta.get("namespace", "unknown-or-cluster-scoped")
        labels = ",".join(f"{k}={v}" for k, v in meta.get("labels", {}).items()) if not args.exclude_labels else None
        rows.append((kind, namespace, meta["name"], labels))

# Print column names
if args.exclude_labels:
    print("KIND\tNAMESPACE\tNAME")
else:
    print("KIND\tNAMESPACE\tNAME\tLABELS")

# Print retrieved values
for kind, ns, name, labels in rows:
    if args.exclude_labels:
        print(f"{kind}\t{ns}\t{name}")
    else:
        print(f"{kind}\t{ns}\t{name}\t{labels or '-'}")


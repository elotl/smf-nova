#!/usr/bin/env bash

# This script prints the list of Kind resources and their names in a given Kubernetes manifest yaml file
# For each Kind resource, the namespace value is printed if available, if not, "unknown-or-cluster-scoped"
# will be printed.

set -euo pipefail

MANIFEST="$1"

if [[ $# -ne 1 || ! -f "$MANIFEST" ]]; then
  echo "Usage: $0 <kubernetes-manifest.yaml>"
  exit 1
fi

# Print header
printf "KIND\tNAMESPACE\tNAME\n"

# Print each object
yq -r '. as $doc
  | select($doc.kind != null)
  | [$doc.kind, ($doc.metadata.namespace // "unknown-or-cluster-scoped"), $doc.metadata.name]
  | @tsv' "$MANIFEST" \
| column -t -s $'\t'


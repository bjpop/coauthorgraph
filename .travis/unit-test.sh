#!/bin/bash

set -e
errors=0

# Run unit tests
python python/coauthgraph/coauthgraph_test.py || {
    echo "'python python/coauthgraph/coauthgraph_test.py' failed"
    let errors+=1
}

# Check program style
pylint -E python/coauthgraph || {
    echo "'pylint -E python/coauthgraph' failed"
    let errors+=1
}

[ "$errors" -gt 0 ] && {
    echo "There were $errors errors found"
    exit 1
}

echo "Ok : Python specific tests"

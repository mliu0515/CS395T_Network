#!/bin/bash

# Step 1: Download and install Linkerd
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install | sh
export PATH=$PATH:/users/mliu0515/.linkerd2/bin

# Step 2: Pre-installation checks
if linkerd check --pre; then
    echo "Pre-installation checks passed."

    # Step 3: Install Linkerd CRDs and main control plane
    linkerd install --crds | kubectl apply -f - && \
    linkerd install --proxy-cpu-limit 1 | kubectl apply -f - && \
    echo "Linkerd CRDs and main control plane installed."

    # Step 4: Post-installation checks
    if linkerd check; then
        echo "Linkerd installation validated."

        # Step 5: Install Linkerd Viz extension
        linkerd viz install | kubectl apply -f - && \
        echo "Linkerd Viz extension installed."

        # Step 6: Post-installation checks for Viz extension
        if linkerd viz check; then
            echo "Linkerd Viz extension validated."

            # Step 7: Launch Linkerd Dashboard
            linkerd viz dashboard &

            # Step 8: Inject Linkerd into existing Kubernetes deployments
            kubectl get deploy -o yaml | linkerd inject - | kubectl apply -f -
            echo "Linkerd injected into existing deployments."
        else
            echo "Error: Linkerd Viz check failed."
            exit 1
        fi
    else
        echo "Error: Linkerd post-installation check failed."
        exit 1
    fi
else
    echo "Error: Pre-installation checks failed."
    exit 1
fi

echo "Linkerd setup completed successfully."
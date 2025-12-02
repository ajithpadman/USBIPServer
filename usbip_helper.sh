#!/bin/bash
#
# usbip-helper: Safe root-only wrapper for USB/IP operations
# Allows limited privileged actions from an unprivileged web server
#

set -e

# Path to commands
USBIPD="/usr/bin/usbipd"
USBIP="/usr/bin/usbip"

# Check that the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "Error: usbip-helper must be run as root." >&2
    exit 1
fi

# Ensure a command was passed
if [ $# -lt 1 ]; then
    echo "Usage: $0 {start|bind|unbind|attach|detach} [busid|port]"
    exit 1
fi

cmd="$1"
arg="$2"

# Validate BUSID pattern safely (example: 1-1, 2-2.3, etc.)
valid_busid_regex='^[0-9]+(-[0-9]+(\.[0-9]+)*)$'

case "$cmd" in
    start)
        echo "Starting usbipd daemon..."
        exec "$USBIPD" --daemon
        ;;
    list)
       echo "Listing all USB devices..."
       exec "$USBIP" list -l
       ;;

    bind)
        if [[ ! "$arg" =~ $valid_busid_regex ]]; then
            echo "Invalid bus id: $arg"
            exit 1
        fi
        echo "Binding USB device $arg..."
        exec "$USBIP" bind -b "$arg"
        ;;

    unbind)
        if [[ ! "$arg" =~ $valid_busid_regex ]]; then
            echo "Invalid bus id: $arg"
            exit 1
        fi
        echo "Unbinding USB device $arg..."
        exec "$USBIP" unbind -b "$arg"
        ;;

    attach)
        # Example: attach to remote host
        # arg format: "host port"
        host="$2"
        port="$3"
        echo "Attaching $host:$port ..."
        exec "$USBIP" attach -r "$host" -p "$port"
        ;;

    detach)
        # detach using port number
        port="$arg"
        echo "Detaching port $port ..."
        exec "$USBIP" detach -p "$port"
        ;;

    *)
        echo "Invalid command: $cmd"
        echo "Usage: $0 {start|bind|unbind|attach|detach}"
        exit 1
        ;;
esac

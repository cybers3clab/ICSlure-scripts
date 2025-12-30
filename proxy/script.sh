#!/bin/bash

# Set variables
INTERFACE="eth0"
CAPTURE_DIR="/root/tcpdump"  # Set your preferred directory for .pcap files
BUCKET_NAME="plc"
PREFIX="pcap_capture"           # Prefix for captured files
ROTATE_INTERVAL=3000             # Rotate every 3000 seconds (5 minutes)

# Create capture directory if it doesn't exist
mkdir -p "$CAPTURE_DIR"
while :
do
# Start tcpdump in the background
tcpdump -i $INTERFACE -w $CAPTURE_DIR/$PREFIX-%Y%m%d%H%M%S.pcap -G $ROTATE_INTERVAL -s 0 &

inotifywait -m "$CAPTURE_DIR" -e close_write --format '%w%f' | while read NEWFILE
do
    # Check if the file ends with .pcap.gz to only upload the rotated files
    if [[ "$NEWFILE" =~ \.pcap$ ]]; then
	tcpdump -i $INTERFACE -w $CAPTURE_DIR/$PREFIX-%Y%m%d%H%M%S.pcap -G $ROTATE_INTERVAL -s 0 &
        # Upload the file to MinIO
        mc mv "$NEWFILE" myminio/$BUCKET_NAME/
	echo "File spostato"
        # Remove the local file after upload to free up space
        #rm -f "$NEWFILE"
    fi

done
done

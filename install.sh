#!/bin/bash
# Install raspiclock
# 
# Run using:
# $ ./install.sh
#
# Can be safely run multiple times
#

set -e

tmpfile=$(mktemp)
trap 'rm -f "$tmpfile"' EXIT

crontab -l 2>/dev/null | grep -v '/home/pi/RaspiDigiHamClock/raspiclock.py' > "$tmpfile" || true
cat ./cronfile >> "$tmpfile"
crontab "$tmpfile"
echo "Crontab entry installed for pi userid. OK"
 

echo "Finished installation."
echo "Reboot your pi now:  $ sudo reboot"
echo 

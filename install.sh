#!/bin/bash
# Install raspiclock
# 
# Run using:
# $ ./install.sh
#
# Can be safely run multiple times
#

crontab ./cronfile
echo "Crontab entry installed for pi userid. OK"
 

echo "Finished installation."
echo "Reboot your pi now:  $ sudo reboot"
echo 


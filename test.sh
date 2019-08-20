#!/bin/bash
#===============================================================================
#
#          FILE:  test.sh
# 
#         USAGE:  ./test.sh 
# 
#   DESCRIPTION:  
# 
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:   (), 
#       COMPANY:  
#       VERSION:  1.0
#       CREATED:  08/19/19 15:47:00 CEST
#      REVISION:  ---
#===============================================================================

#!/bin/sh 
osascript <<END 
tell application "System Events"
   tell current location of network preferences
       set VPNservice to service "Otto"
       if exists VPNservice then disconnect VPNservice
   end tell
end tell
END

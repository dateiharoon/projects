#!/usr/bin/bash
# ============================================================================
# Name:       news_feed.sh
# Purpose:    Inserting data into industry news trends table 
# Location:   /home/roohihea/scripts/projects
# Usage:      
#
# Parameters:
# 
# Amendment History:
#
# Name           	Date       Ver  Desc
# ============== 	========== ==== ==========================================
# H.IQBAL  			18/02/2023 1.0  Initial Release
# 
#
# ============================================================================
#
#
#Source in Standard Environment and Functions
source $HOME/.bash_profile
source $SH_BASE/shell/ip_functions.sh
MAIL_RECIPIENTS="harooncodes24@gmil.com"
#source activate MachineLearning


# cron job
# 0 * * * * /home/portaladmin/scripts/python/Data_Science/news_feed/news_feed.sh > /home/portaladmin/scripts/logs/news_feed.log 2>&1

#=============================================================================
#Activate Conda Environment
#source /home/portaladmin/scripts/python/Data_Science/news_feed/news_feed_env/bin/activate

#Install all of the packages that we need.
#logmsg "Running requirements"
pip3 install -r ~/home/roohihea/scripts/projects/requirements.txt

#Run the Python Scripts
echo "Inserting data into industry news trends table "
logmsg "running script"
cd ~/scripts/projects/projects $1 > $WORK2 2>&1

python3 ~/scripts/projects/projects/licensing-source_function.py $1 > $WORK2 2>&1
logmsg "licensing-source_function.py"


STATUS=$?
ERRCHK=`egrep "ERROR" ${WORK2} | wc -l`
WARNINGCHK=`egrep "Warning" ${WORK2} | wc -l`
MODELCHK=`egrep "completed" ${WORK2} | wc -l`

# Check status
logfile $WORK2

logmsg "Exit status : ${STATUS}"
logmsg "Errors : $ERRCHK"
logmsg "Warnings: $WARNINGCHK"
#logmsg "Trend Alerts Sent: $MODELCHK"

if [ "$ERRCHK" -gt 0 ] || [ "$STATUS" -gt 0 ]; then
     raise_crit "${PROG} - Errors found please check $LOG"
fi

# if [ "$WARNINGCHK" -gt 0 ] || [ "$STATUS" -gt 0 ]; then
#     raise_warn "${PROG} - Warning found please check $LOG"
# fi

if [ "$MODELCHK" -gt 0 ] || [ "$STATUS" -gt 0 ]; then
     raise_info "${PROG} - email sent $LOG"
     echo "error email sent"
fi
#echo "This has worked and completed running"
logmsg "This has worked and completed running"

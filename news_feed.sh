#!/usr/bin/bash
# ============================================================================
# Name:       news_feed.sh
# Purpose:    Inserting data into industry news trends table 
# Location:   /scripts/python/Data_Science/news_feed/news_feed.sh
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
pip3 install -r ~/scripts/python/Data_Science/news_feed/requirements.txt

#Run the Python Scripts
echo "Inserting data into industry news trends table "
logmsg "running script"
cd ~/scripts/python/Data_Science/news_feed $1 > $WORK2 2>&1
python3 ~/scripts/python/Data_Science/news_feed/Working_techcrunch.py $1 > $WORK2 2>&1
logmsg "Working_techcrunch.py"
python3 ~/scripts/python/Data_Science/news_feed/kidscreen_webscrapping.py $1 > $WORK2 2>&1
logmsg "kidscreen_webscrapping.py"
python3 ~/scripts/python/Data_Science/news_feed/script_license_magazine_working.py $1 > $WORK2 2>&1
logmsg "script_license_magazine_working.py"
python3 ~/scripts/python/Data_Science/news_feed/Total_licensing.py $1 > $WORK2 2>&1
logmsg "Total_licensing.py"
python3 ~/scripts/python/Data_Science/news_feed/ico_scrapping.py $1 > $WORK2 2>&1
logmsg "ico_scrapping.py"
python3 ~/scripts/python/Data_Science/news_feed/mrs-script_function.py $1 > $WORK2 2>&1
logmsg "mrs-script_function.py"
python3 ~/scripts/python/Data_Science/news_feed/licensing-source_function.py $1 > $WORK2 2>&1
logmsg "licensing-source_function.py"
python3 ~/scripts/python/Data_Science/news_feed/mojo_nation_function.py $1 > $WORK2 2>&1
logmsg "mojo_nation_function.py"
python3 ~/scripts/python/Data_Science/news_feed/poc-website_function.py $1 > $WORK2 2>&1
logmsg "poc-website_function.py"
python3 ~/scripts/python/Data_Science/news_feed/drum_nation_function.py $1 > $WORK2 2>&1
logmsg "drum_nation_function.py"
python3 ~/scripts/python/Data_Science/news_feed/c21_function.py $1 > $WORK2 2>&1
logmsg "c21_function.py"
python3 ~/scripts/python/Data_Science/news_feed/licensing_international_webscrapping.py $1 > $WORK2 2>&1
logmsg "licensing_international_webscrapping.py"
python3 ~/scripts/python/Data_Science/news_feed/One_mip_working.py $1 > $WORK2 2>&1
logmsg "One_mip_working.py"

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

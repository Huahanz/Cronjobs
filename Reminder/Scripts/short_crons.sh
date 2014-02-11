do
 source ~/.bash_profile; sudo sh /var/www/crons/Cronjobs/Reminder/bin/stockcronjob.sh &>> /var/www/logs/stockcronjob.log
 sleep 5
done


path='/var/www/logs/stockcronjob.log'
backup_path="/var/www/logs/stockcronjob-`date +%m-%d-%y`.log"
size=$(stat -c %s $path)
if [ "$size" > 100000 ]; then
	echo 'large'
	tail -n10000 $path > $backup_path
	rm $path
	#$cat $backup_path > $path
fi

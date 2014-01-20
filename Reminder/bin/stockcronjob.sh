export DIR_PATH=$(cd $(dirname "$1") && pwd -P)/$(basename "$1")
python $DIR_PATH/../StockJobs/stockjob.py
cd /home/ubuntu/indianliberals/bin
# files written to log will not be considered for publishing again
echo "python ./get_training_data.py ../input/content_map.txt ../logs/log.txt ../input/db_credentials.txt ../input/keywords.txt ../output/training_data.txt"
python ./get_training_data.py ../input/content_map.txt ../logs/log.txt ../input/db_credentials.txt ../input/keywords.txt ../output/training_data.txt

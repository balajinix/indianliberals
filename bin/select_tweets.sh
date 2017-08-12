echo "rm ../input/temp_tweets/*"
rm ../input/temp_tweets/*
# read from publish_tweets, use content_map to know where to publish, create log in log.txt and changed_files.txt
echo "python ./select_tweets.py ../input/content_map.txt ../logs/publish_tweets.txt ../logs/log.txt ../logs/changed_files.txt"
python ./select_tweets.py ../input/content_map.txt ../logs/publish_tweets.txt ../logs/log.txt ../logs/changed_files.txt

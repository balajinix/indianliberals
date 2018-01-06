cd /home/ubuntu/indianliberals/bin
echo "rm ../output/auto/*"
rm ../output/auto/*
# files written to log will not be considered for publishing again
echo "python ./classify_articles.py ../input/content_map.txt ../logs/log.txt ../input/db_credentials.txt ../input/keywords.txt"
python ./classify_articles.py ../input/content_map.txt ../logs/log.txt ../input/db_credentials.txt ../input/keywords.txt

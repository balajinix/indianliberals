echo "cd /home/ubuntu/indianliberals/bin"
cd /home/ubuntu/indianliberals/bin
echo "python ./submit_articles.py ../input/db_credentials.txt ../input/content_map.txt ../logs/publish.txt"
python ./submit_articles.py ../input/db_credentials.txt ../input/content_map.txt ../logs/publish.txt
echo "rm ../logs/publish.txt"
rm ../logs/publish.txt

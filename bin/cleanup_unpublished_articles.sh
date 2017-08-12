echo "cd /home/ubuntu/indianliberals/bin"
cd /home/ubuntu/indianliberals/bin
echo "python ./cleanup_unpublished_articles.py ../logs/publish.txt ../logs/log.txt ../input/db_credentials.txt"
python ./cleanup_unpublished_articles.py ../logs/publish.txt ../logs/log.txt ../input/db_credentials.txt
cd -

echo "cd /home/ubuntu/indianliberals/bin"
cd /home/ubuntu/indianliberals/bin
echo "python ./get_articles.py ../input/urls.txt log.txt ../logs/publish.txt"
python ./get_articles.py ../input/urls.txt ../logs/log.txt ../logs/publish.txt
cd -

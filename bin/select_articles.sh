echo "rm ../input/temp/*"
rm ../input/temp/*
echo "python ./select_articles.py ../input/facebook_pages.txt ../input/publish.txt ../logs/log.txt ../logs/changed_files.txt"
python ./select_articles.py ../input/facebook_pages.txt ../input/publish.txt ../logs/log.txt ../logs/changed_files.txt

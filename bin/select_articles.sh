echo "rm ../input/temp/*"
rm ../input/temp/*
echo "python ./select_articles.py ../input/content_map.txt ../logs/publish.txt ../logs/log.txt ../logs/changed_files.txt"
python ./select_articles.py ../input/content_map.txt ../logs/publish.txt ../logs/log.txt ../logs/changed_files.txt

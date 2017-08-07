echo "rm ../input/temp/*"
rm ../input/temp/*
# files written to log will not be considered for publishing again
echo "python ./get_selected_articles.py ../input/content_map.txt ../logs/log.txt ../logs/changed_files.txt"
python ./get_selected_articles.py ../input/content_map.txt ../logs/log.txt ../logs/changed_files.txt

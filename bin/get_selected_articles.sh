cd /home/ubuntu/indianliberals/bin
echo `date`
echo "rm ../output/temp/*"
rm ../output/temp/*
# files written to log will not be considered for publishing again
echo "python ./get_selected_articles.py ../input/content_map.txt ../logs/published.txt ../logs/changed_files.txt"
python ./get_selected_articles.py ../input/content_map.txt ../logs/published.txt ../logs/changed_files.txt

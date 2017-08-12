cd /home/ubuntu/indianliberals/bin
echo `date`
echo "rm ../output/temp/*"
rm ../output/temp/*
# files written to log will not be considered for publishing again
echo "python ./get_selected_articles.py ../input/content_map.txt ../logs/log.txt ../logs/changed_files.txt"
python ./get_selected_articles.py ../input/content_map.txt ../logs/log.txt ../logs/changed_files.txt
echo "python ./publish_to_facebook.py ../input/content_map.txt ../logs/publish.txt"
python ./publish_to_facebook.py ../input/content_map.txt ../logs/publish.txt

cd /home/ubuntu/indianliberals/bin
echo `date`
echo "python ./publish_to_facebook.py ../input/content_map.txt ../logs/published.txt"
python ./publish_to_facebook.py ../input/content_map.txt ../logs/published.txt
echo "rm ../output/temp/*"
rm ../output/temp/*
cd -


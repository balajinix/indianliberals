cd /home/ubuntu/indianliberals/bin
echo "python ./create_htmls.py ../output ../input/content_map.txt ../input/base_text/ ../input/agenda/"
python ./create_htmls.py ../output ../input/content_map.txt ../input/base_text/ ../input/agenda/
echo "python ./create_news_page.py ../output ../input/content_map.txt ../input/base_text/ ../input/agenda/"
python ./create_news_page.py ../output ../input/content_map.txt ../input/base_text/ ../input/agenda/

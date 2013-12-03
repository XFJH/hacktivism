from django.core.management import setup_environ
import mysite.settings
setup_environ(mysite.settings)

from defacements.models import Notifier, Defacements
from lxml import etree
import datetime
import os.path

def get_rss(path='.'):
    files = []
    for root_A, dir_A, file_A in os.walk(path):
        for file_A_A in file_A:
            base_name , extend_name = os.path.splitext(file_A_A)
            if extend_name == '.rss':
                files.append(file_A_A)
    return files

def store_to_mysql(n_notifier, path, pubdate):
    try:
        n = Notifier.objects.get(name=n_notifier)
    except Notifier.DoesNotExist:
        n = Notifier(name=n_notifier)
        n.save()
    try:
        d = Defacements.objects.get(notifier=n, full_path=path)
    except Defacements.DoesNotExist:
        d = Defacements(notifier = n, full_path = path, time = pubdate)
        d.save()
    
def rss_to_form( f_list):
    for f in f_list:
        rss_form = open("./rss_form.txt", mode='a')
        filename= str(f) 
        print filename
        fp = open('./rss_file/' + filename, 'r')

        xml = fp.read()
        root = etree.fromstring(xml)
        item_set = root.xpath('//item')
        hacktivism_list = ''
        for item in item_set:
            description = item.find('description').text
            full_path = description.split(' ')[0]
            notifier = description.split(' ')[-1]
            pubDate = item.find('pubDate').text
            pubdate = datetime.datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S +0000')
            
            store_to_mysql(notifier, full_path, pubdate)
            #record = [ {'T_cracked_pubDate': pubDate}, \
                           #{'T_cracked_notifier': notifier}, \
                           #{'T_cracked_path': full_path}  ]
            record = 'pubDate='+ str(pubdate) +','\
                'notifier=' + notifier + ',' \
                'full_path=' + full_path + ',\n'
            hacktivism_list += record
        rss_form.write( str(hacktivism_list))
        fp.close()
        rss_form.close()

    
    
if __name__ == '__main__':
    rss_file_list = get_rss(path='./rss_file/')
    rss_to_form(f_list=rss_file_list)
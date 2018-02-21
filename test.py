from urllib import request

from lxml import html

handler = request.urlopen('https://petition.parliament.uk/petitions/200292')
res_html = handler.read()
tree = html.fromstring(res_html.decode("utf-8"))
title = tree.xpath('/html/head/title')[0].text
print(title[:-12])


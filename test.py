from docxtpl import DocxTemplate
doc = DocxTemplate('D:/Final Year project/x/project/templates/template.docx')
results = [
    {
        'url': 'www.django.com',
        'match': 20
    },
    {
        'url': 'www.django.com',
        'match': 10
    },
    {
        'url': 'www.django.com',
        'match': 90
    },
    {
        'url': 'www.django.com',
        'match': 15
    },
    {
        'url': 'www.django.com',
        'match': 50
    },
    {
        'url': 'www.django.com',
        'match': 9
    }
]
maxk = ''
maxv = 0
for i in results:
    # print(i)
    if i['match'] > maxv:
        maxv = i['match']
        maxk = i['url']

context = {
    'plag_index': maxv,
    'plag_source': maxk,
    'rows': results
}
doc.render(context)
doc.save('template.docx')

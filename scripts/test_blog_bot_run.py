from blog_bot import create_blog_file

product_data={'id':'TEST123','title':'Test Product','description':'Short','price':'','link':'https://example.com','images':['/img/a.jpg','/img/b.jpg']}
ai_content={'title':"Kid's Room Ideas!",'description':'Great little ideas','tags':['Sharjah','Kid&#39;s Room Ideas','home & decor','special#tag',''],'intro':'Intro','product_section':'Details','why_it_works':['Point 1','Point 2'],'perfect_for':'Families','conclusion':'Done'}
fn=create_blog_file(product_data, ai_content)
print('Created:',fn)
with open('posts/'+fn) as f:
    data = f.read()
print(data.split('\n')[:30])

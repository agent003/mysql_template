from flask import Flask
from flask import render_template, flash, redirect, request
import MySQLdb
import sys
import unicodedata
import re

app = Flask(__name__)
data_set = {}
header = open('templates/temp1.html','r').read()
footer = open('templates/temp2.html','r').read()

#print data_set

#@app.route('/')
@app.route('/index')
def index():
    connection = MySQLdb.connect (host = '34.209.34.113', user = "abcd" , passwd = "abcd", db = "mintshowapp_live")
    cursor = connection.cursor (MySQLdb.cursors.DictCursor)
    query = 'select * from sys_email_templates'
    cursor.execute (query)
    data = cursor.fetchall()
    #field_names = [i[0] for i in cursor.description]
    #sub = [str(i['Subject']) for i in data]
    for i in data:
        data_set[i['ID']] = {'ID':i['ID'],'Name':i['Name'],'Body':i['Body'],'Desc':i['Desc'],'Subject':i['Subject']}
    return render_template('beta_index.html',data_set=data_set,keys=data_set.keys())

@app.route('/body/<user_id>/', methods=['GET', 'POST'])
def details(user_id):
    body = data_set[long(user_id)]['Body']
    body = body.replace('<bx_include_auto:_email_header.html/>','')
    body = body.replace('<bx_include_auto:_email_header.html />','')
    body = body.replace('<bx_include_auto:_email_header.html  />','')
    body = body.replace('<bx_include_auto:_email_footer.html />','')

    body = ''.join([i if ord(i) < 128 else ' ' for i in body])
    master_list = [line.rstrip('\n') for line in open('master.txt')]
    for i in master_list:
        body = body.replace(i,i[1:-1])
    content = header+ '<!-- ' + str('#'*121) + '-->' + str(body) + '<!-- '  +str('#'*120) + '-->' + footer
    return render_template('live1.html',content=content,user_id=user_id)


@app.route('/preview/<user_id>', methods=['GET', 'POST'])
def preview(user_id):
    query = request.form['ta']
    temp1 = '<!-- ' + str('#'*121) + '-->'
    temp2 = '<!-- ' + str('#'*120) + '-->'
    query = query[query.index(temp1) + len(temp1):query.index(temp2)]
    user_id = int(user_id)
    data_set[user_id]['Body'] = query
    master_list = list(set([line.rstrip('\n') for line in open('master.txt')]))
    for i in master_list:
        if i[1:-1] in query:
            temp = query.index(i[1:-1])
            if(not query[temp-1].isalpha() and not query[temp+len(i)-2].isalpha()):
                print i + " Yessssss"
                query = query[:temp] + i + query[temp+len(i[1:-1]):]
    query = '<bx_include_auto:_email_header.html />' + query + '<bx_include_auto:_email_footer.html />'
    print query
    connection = MySQLdb.connect (host = '34.209.34.113', user = "abcd" , passwd = "abcd", db = "mintshowapp_live")
    cursor = connection.cursor (MySQLdb.cursors.DictCursor)
    #query1 = 'update sys_email_templates set Body="'+str(query)+'" where ID='+str(user_id)
    query2 = "update sys_email_templates set Body='%s' where ID=%d;"%(query,user_id)
    print query2
    cursor.execute (query2)
    return ('<html>Hello world</html>')

@app.route('/', methods=['GET', 'POST'])
def edit1():
    return render_template('live1.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

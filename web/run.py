from flask import Flask
from flask import render_template, flash, redirect, request
import MySQLdb
import sys
import unicodedata

app = Flask(__name__)
connection = MySQLdb.connect (host = '52.53.205.75', user = "yaacdev" , passwd = "yaacmydev", db = "mintshowapp_live")
cursor = connection.cursor (MySQLdb.cursors.DictCursor)
query = 'select * from sys_email_templates'
cursor.execute (query)
data = cursor.fetchall()
#field_names = [i[0] for i in cursor.description]
#sub = [str(i['Subject']) for i in data]
header = open('templates/temp1.html','r').read()
footer = open('templates/temp2.html','r').read()
data_set = {}
for i in data:
    data_set[i['ID']] = {'ID':i['ID'],'Name':i['Name'],'Body':i['Body'],'Desc':i['Desc'],'Subject':i['Subject']}
#print data_set

@app.route('/')
@app.route('/index')
def index():
    return render_template('beta_index.html',data_set=data_set,keys=data_set.keys())
            


     
@app.route('/body/<user_id>/', methods=['GET', 'POST'])
def details(user_id):
    temp = open('templates/abcd.html','w')
    body = data_set[long(user_id)]['Body']
    body = body.replace('<bx_include_auto:_email_header.html />','')
    body = body.replace('<bx_include_auto:_email_footer.html />','')
    #print body
    temp.write(header + str(body) + footer )
    temp.close()
    return render_template('abcd.html')



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

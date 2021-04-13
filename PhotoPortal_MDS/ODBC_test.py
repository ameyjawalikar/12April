import os
import datetime
import pyodbc
import textwrap
import json
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello():
    print("Program Execution Started")
    driver= '{ODBC Driver 17 for SQL Server}'
    server_name= 'tcp:sqlserveruat2021'
    database_name= 'TestDB'
    server= '{server_name}.database.windows.net, 1433'.format(server_name=server_name)
    #server='tcp:sqlserveruat2021.database.windows.net, 1433'
    #print(server)
    user_name='systemadmin'
    password='Test@123'
    connection_string= textwrap.dedent('''
        Driver= {driver};
        Server= {server};
        Database={database_name};
        Uid={user_name};
        Pwd={password};
        Encrypt=yes;
        TrustServerCertificate=No;
        Connection Timeout=30;
    '''.format(
        driver=driver,
        server=server,
        database_name=database_name,
        user_name=user_name,
        password=password
    ))
    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()
    
    datetimes = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    FileName = 'Result_' + datetimes + '.txt'
    f = open(FileName, "w")
    sql = "INSERT INTO ImageDetails (Name, quality, bluriness, darkness, brightness) VALUES (?, ?, ?, ?, ?)"
    val = ('Test1.jpg', 'Custom','Blur', 'Dark', '')
    cursor.execute(sql, val)
    cnxn.commit()
    f.write(FileName +" -- " + "\n")
    f.close()
    os.remove(FileName)
    print("Program Execution completed")
    return ('Success Executed At: '+datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
if __name__ == '__main__':
    app.run(debug=True)

from pkg import access_form

access=access_form.AccessForm()

if access.status:
   interface=access_form.MysqlInterface(access.connection)
   interface.cursor.close()
   access.connection.close()
   
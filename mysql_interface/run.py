from pkg import access_form

#AccessForm creates a window which asks the client to type username and password for the connection.
#If both are correct, it establishes a connection with the database.
access=access_form.AccessForm()

if access.status:
   #If a connection is established, the program runs the interface with MySQL.
   interface=access_form.MysqlInterface(access.connection)
   
   #When MysqlInterface is ended, cursor and connection are closed.
   interface.cursor.close()
   access.connection.close()
   

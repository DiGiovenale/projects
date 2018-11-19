from .main import *


class AccessForm():

   '''
   The class creates a form, which asks the client to insert user and password to MySQL db.
   Then checks if the insert data enables a connection via pymysql.
   If that is the case, closes the form and return a self.status=True
   '''

   def __init__(self):

      self.status=False
      self.connection=None

      self.root=tk.Tk()
      self.root.title('MySQL')

      self.lab_usr=tk.Label(self.root,text='User:')
      self.lab_usr.grid(row=0,column=0)

      self.ent_usr=tk.Entry(self.root)
      self.ent_usr.grid(row=0,column=1)
      self.ent_usr.focus_set()
      self.ent_usr.bind('<Return>',lambda x: self.ent_psw.focus_set())
      self.ent_usr.bind('<Down>',lambda x: self.ent_psw.focus_set())

      self.lab_psw=tk.Label(self.root,text='Password:')
      self.lab_psw.grid(row=1,column=0)

      self.ent_psw=tk.Entry(self.root)
      self.ent_psw.grid(row=1,column=1)
      self.ent_psw.bind('<Return>',self.check_input)
      self.ent_psw.bind('<Up>',lambda x: self.ent_usr.focus_set())

      self.conf=tk.Button(self.root,text='Confirm',fg='red',command=self.check_input)
      self.conf.bind('<Return>',self.check_input)
      self.conf.grid(row=2,columnspan=2)

      self.root.mainloop()

   def check_input(self,event=''):
      '''
      When called, verifies if the data provided in ent_usr and ent_psw are valid for the connection to MySQL.
      '''
      
      try:
         self.connection=pymysql.connect(user=self.ent_usr.get(),password=self.ent_psw.get())
      except:
         messagebox.showwarning('Access denied','Incorrect username or password')
      else:
         self.root.destroy()
         self.status=True


if __name__=='__main__':
   
   tester=AccessForm()
   if tester.status:
      messagebox.showinfo('Connected','Connection estabilished')
      tester.connection.close()

import tkinter as tk
from tkinter import scrolledtext,messagebox
import pymysql


class MysqlInterface():
   '''
   Creates an interface with MySQL. The generetor requires a connection with the databases already established. The class uses tkinter as "tk".

   To execute the command, insert the statement into the entry-box and then press Return.
   The output will be shown in the scrolledtext at the bottom of the window.

   By pressing Up or Down in the entry-box the interface will show up, repectively, the previous and the preceding committed command.
   '''

   def __init__(self,connection):

      self.connection=connection
      self.cursor=connection.cursor()

      # self.commands stores the last 20 commands committed, self.comm_index is used to jump, with Up and Down, through the commands in self.commands.
      self.commands=['']
      self.comm_index=0

      self.root=tk.Tk()
      self.root.title('MySQL - Interface')
   
      self.lab=tk.Label(self.root,text='Enter command here:')
      self.lab.pack()

      self.entry=tk.Entry(self.root)
      self.entry.pack(fill='x')
      self.entry.focus_set()
      self.entry.bind('<Return>',self._execute)
      self.entry.bind('<Up>',self.recall_command)
      self.entry.bind('<Down>',self.recall_command)

      self.empty=tk.Label(self.root)
      self.empty.pack()

      self.scr=scrolledtext.ScrolledText(self.root)
      self.scr.pack(fill=tk.BOTH)

      self.root.mainloop()


   def _execute(self,event=''):
      '''
      If the result from self.commandhandler is None (i.e., an error occurred in the execution of the query) breaks the process and returns None.
      Else, it collects the result from the query, adding the name for each column, if present.
   
      Finally, calls show_tables, which prints the output to the user.
      '''

      res=self.commandhandler()

      if not res: return

      #The if statement tests if the name of the columns are presente in the response from the db and adds them to the result tuple.
      #The name of the column are stored in the element 0 of each tuple in cursor.description.
      if self.cursor.description:
         result = (tuple(elm[0].upper() for elm in self.cursor.description),)
      else:
         result=tuple()
      result = result + self.cursor.fetchall()
      
      len_columns=length_col(result)
      self.show_table(result,self.scr,len_columns)
      
   def show_table(self,result,len_columns):
      '''
      As output, prints in self.scr a table, with every row separated by a '|'.
      If there is no table to be returned, prints in self.scr only 'EXECUTED'.

      The input accepted is compound by 2 nested iterables, where every cell is identified by input[row][col].


      len_columns defines the maximum length for each column, in the form of an iterable of the type:
      (len_col1, len_col2, len_col3, ...)
      '''

      table=str()

      #Iterates through the rows
      for row in range(len(result)):

         #Iterates through the columns
         for col in range(len(result[0])):

            cell= '%'+ str(len_columns[col]) + 's|'
            table += cell % str(result[row][col])

         table += '\n'

      self.scr.delete(1.0,tk.END)
     
      if table:
         self.scr.insert(tk.INSERT,table.rstrip('\n'))
      else:
         self.scr.insert(tk.INSERT,'EXECUTED')


   def commandhandler(self):
      '''
      The function tries to execute the command written in self.entry. If it fails, pops up an error-box and returns None.
      If succeeds, stores the command in the first position of self.commands and returns True.
      '''

      try:
         self.cursor.execute(self.entry.get())
      except:
         messagebox.showerror('Error','Incorrect command!')
         return

      self.commands.insert(0,self.entry.get())
      self.commands=self.commands[:20]
      self.comm_index=-1

      self.entry.delete(0,'end')

      return True


   def recall_command(self,event=''):
      '''
      The function is used to display to the user the privious or preceding commands typed in the interface.
      
      According to the keywork pressed ('Up' or 'Down') recall_command updates the self.comm_index.
      Then shows to the user the recalled command in the scrolledtext.
      '''
      self.entry.delete(0,'end')

      if event.keysym=='Up': 
         recalled_command=self.commands[self.comm_index]
         if self.comm_index<len(self.commands)-2:
            self.comm_index += 1

      elif event.keysym=='Down':
         if self.comm_index>0:
            self.comm_index -= 1
            recalled_command=self.commands[self.comm_index]
         else:
            recalled_command=''

      self.entry.insert(0,recalled_command)


#######################################################################

def length_col(table):
   '''
   The function accepts as input a nested iterables as a table, where every cell is identified by input[row][col].
   It returns an ordered list containing the maximum length for each column.
   '''

   if table:
      result=list()
      len_row=len(table)

      #selects one columns a time
      for col in range(len(table[0])):

         #column_lengths stores, as a generator, the length of every cell in the considered column.
         column_lengths=(len(str(table[row][col])) for row in range(len_row))
         
         result.append(max(column_lengths))
   else:
      result=[]

   return result

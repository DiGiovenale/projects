import tkinter as tk
from tkinter import scrolledtext,messagebox
import pymysql


class MysqlInterface():
   '''
   Creates an interface with MySQL. The generetor requires a connection with the databases already established. The class uses tkinter as "tk".

   To execute the command, insert the statement into the entry-box and then press Return.
   The output will be shown in the scrolledtext at the bottom of the window.

   By pressing Up or Down in the entry-box the interface will show up, repectively, the previous and the sequent command already committed.
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
      If the result from self.commandhandler is None (i.e., an error occurred in the execution of the query) breaks the process.
      Else, it collects the result from the query with the name of each column, if present.
   
      Finally, calls show_tables, which prints the output to the user.
      '''

      res=self.commandhandler()

      if not res: return

      if self.cursor.description:
         result = (tuple(elm[0].upper() for elm in self.cursor.description),)
      else:
         result=tuple()
      result = result + self.cursor.fetchall()
      
      len_columns=length_col(result)
      show_table(result,self.scr,len_columns)


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

def length_col(l):
   '''
Funzione che riceve in entrata una lista o tuple dove ogni elemento rappresenta una riga
e ogni elemento all'interno di questo una colonna.
Consegna, in una lista ordinata, la lunghezza di caratteri massimi ritrovata per ogni colonna.

Es di variabile accettata: ((1,2,3),(a,b,c))
In questo caso 1 sara' all'interno della prima riga, prima colonna;
a, invece, sara' nella seconda riga, prima colonna.
'''
   if l:
      out=list()
     #prende in considerazione una colonna alla volta (il numero e' dato da n)
      lenrow=len(l)
      for n in range(len(l[0])):
         #temp rappresenta una tupla contenente le lunghezze di tutti gli elementi in una data colonna
         temp=(len(str(l[elm][n])) for elm in range(lenrow))
         
         #out sceglie solamente la massima
         out.append(max(temp))
   else:
      out=[]
   return out

#####################################################################################

def show_table(out,scroll,lmax):
   
   temp=str()
   for i in range(len(out)):
      for n in range(len(out[0])):

         str_temp= '%'+ str(lmax[n]) + 's|'
         temp += str_temp % str(out[i][n])

      temp += '\n'
   scroll.delete(1.0,tk.END)

   if temp:
      scroll.insert(tk.INSERT,temp.rstrip('\n'))
   else:
      scroll.insert(tk.INSERT,'EXECUTED')

#####################################################################################


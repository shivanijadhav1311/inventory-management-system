from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1200x700+220+150")
        self.root.title("Inventory Management System    |   Developed By Shivani")
        self.root.config(bg="white")
        self.root.focus_force()
        
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        
        title=Label(self.root,text="Manage Product Details",font=("goudy old style",30),bg="blueviolet",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        lbl_name=Label(self.root,text="Enter Category Name",font=("goudy old style",30),bg="white").place(x=50,y=100)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",20),bg="lightyellow").place(x=50,y=170,width=300)     
        btn_add=Button(self.root,text="ADD",command=self.add,font=("goudy old style",15),bg="red",fg="white").place(x=360,y=170,width=150,height=30)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="green",fg="white",).place(x=520,y=170,width=150,height=30)
        
        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=100,width=380,height=500)
        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)
        
        self.Category_Table=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.Category_Table.xview)
        scrolly.config(command=self.Category_Table.yview)
           
        self.Category_Table.heading("cid",text="CATEGORY ID")
        self.Category_Table.heading("name",text="NAME")
        self.Category_Table["show"]="headings"
        self.Category_Table.column("cid",width=90)
        self.Category_Table.column("name",width=100)  
        self.Category_Table.pack(fill=BOTH,expand=1) 
        self.Category_Table.bind("<ButtonRelease-1>",self.get_data)

        self.img1=Image.open("images/cat.jpg")
        self.img1=self.img1.resize((500,250),Image.ANTIALIAS)
        self.img1=ImageTk.PhotoImage(self.img1)
        self.lbl_img1=Label(self.root,image=self.img1,bd=2,relief=RIDGE)
        self.lbl_img1.place(x=50,y=220)
        self.show()

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Category name must be required",parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This category already present, try different",parent=self.root)
                else:
                    cur.execute("Insert into category (name) values (?)",(self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Category Added Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from category")
            rows=cur.fetchall()
            self.Category_Table.delete(*self.Category_Table.get_children())
            for row in rows:
                self.Category_Table.insert('',END,values=row)
                            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root) 
            
    def get_data(self,ev):
        f=self.Category_Table.focus()
        content=(self.Category_Table.item(f))
        row=content['values']
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1]) 
        
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","Please category from the list",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Error please try again",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete",parent=self.root)
                    if op==True:
                            cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                            con.commit()
                            messagebox.showinfo("Delete","Category Deleted Successfully",parent=self.root)
                            self.show()
                            self.var_cat_id.set("")
                            self.var_name.set("")
                            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root) 
    
if __name__=="__main__":    
    root=Tk()
    obj=categoryClass(root)
    root.mainloop()  
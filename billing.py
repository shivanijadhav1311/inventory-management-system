from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import time
import sqlite3
import os
import tempfile
class billClass:
    
    def __init__(self,root):
        self.root=root
        self.root.geometry("1600x800+0+0")
        self.root.title("Inventory Management System    |   Developed By Shivani")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0
        
        #   title
        self.icon_title=PhotoImage(file="G:\IMS\images\logo1.png")
        
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="blue",fg="white",padx=20).place(x=0,y=0,relwidth=1,height=70)
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="pink",cursor="hand2").place(x=1300,y=10,height=50,width=150)
        
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date : DD-MM-YYYY\t\t Time : HH:MM:SS",font=("times new roman",15),bg="gray",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        
        #=======================================================
        
        self.var_search=StringVar()
        
        productframe1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        productframe1.place(x=20,y=120,width=500,height=650)
        
        ptitle=Label(productframe1,text="All Products",font=("goudy old style",20,"bold"),bg="black",fg="white").pack(side=TOP,fill=X)
        
        productframe2=Frame(productframe1,bd=2,relief=RIDGE,bg="white")
        productframe2.place(x=5,y=45,width=480,height=100)
        
        lbl_search=Label(productframe2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)
        lbl_name=Label(productframe2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)
        txt_search=Entry(productframe2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=140,y=50,width=150,height=25)
        btn_search=Button(productframe2,text="Search",command=self.search,font=("goudy old style",15),bg="red",fg="white").place(x=310,y=50,width=100,height=25)
        btn_show=Button(productframe2,text="Show All",command=self.show,font=("goudy old style",15),bg="green4",fg="white").place(x=310,y=10,width=100,height=25)
        
        productframe3=Frame(productframe1,bd=2,relief=RIDGE)
        productframe3.place(x=5,y=150,width=480,height=450)
        scrolly=Scrollbar(productframe3,orient=VERTICAL)
        scrollx=Scrollbar(productframe3,orient=HORIZONTAL)
        
        self.productTable=ttk.Treeview(productframe3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)
           
        self.productTable.heading("pid",text="pid")
        self.productTable.heading("name",text="name")
        self.productTable.heading("price",text="price")
        self.productTable.heading("qty",text="qty")
        self.productTable.heading("status",text="status")
        
        self.productTable["show"]="headings"
        
        self.productTable.column("pid",width=90)
        self.productTable.column("name",width=100)
        self.productTable.column("price",width=100)
        self.productTable.column("qty",width=100)    
        self.productTable.column("status",width=100)
        self.productTable.pack(fill=BOTH,expand=1) 
        self.productTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        lbl_note=Label(productframe1,text="Note:'Enter 0 Quantity to remove product from the cart'",font=("goudy old style",15,"bold"),bg="white",fg="red").pack(side=BOTTOM,fill=X)
        
        #====================================================
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        customerframe=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        customerframe.place(x=550,y=120,width=500,height=100)
        
        ctitle=Label(customerframe,text="Customer Details",font=("goudy old style",20,"bold"),bg="lightgray").pack(side=TOP,fill=X)
        lbl_name=Label(customerframe,text="Name",font=("times new roman",15),bg="white").place(x=5,y=50)
        txt_name=Entry(customerframe,textvariable=self.var_cname,font=("times new roman",15),bg="lightyellow").place(x=70,y=50,width=150)
        lbl_contact=Label(customerframe,text="contact No.",font=("times new roman",15),bg="white").place(x=230,y=50)
        txt_contact=Entry(customerframe,textvariable=self.var_contact,font=("times new roman",15),bg="lightyellow").place(x=330,y=50,width=150)
        
        cartframe=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        cartframe.place(x=550,y=220,width=500,height=380)
        self.carttitle=Label(cartframe,text="Cart \t Total Product: [0]",font=("goudy old style",15,"bold"),bg="lightgray")
        self.carttitle.pack(side=TOP,fill=X)
        scrolly=Scrollbar(cartframe,orient=VERTICAL)
        scrollx=Scrollbar(cartframe,orient=HORIZONTAL)
        
        self.cartTable=ttk.Treeview(cartframe,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.cartTable.xview)
        scrolly.config(command=self.cartTable.yview)
           
        self.cartTable.heading("pid",text="pid")
        self.cartTable.heading("name",text="name")
        self.cartTable.heading("price",text="price")
        self.cartTable.heading("qty",text="qty")
        
        self.cartTable["show"]="headings"
        
        self.cartTable.column("pid",width=90)
        self.cartTable.column("name",width=100)
        self.cartTable.column("price",width=100)
        self.cartTable.column("qty",width=100)    
        self.cartTable.pack(fill=BOTH,expand=1) 
        self.cartTable.bind("<ButtonRelease-1>",self.get_data_cart)
        
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
                
        addcartframe=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        addcartframe.place(x=550,y=600,width=500,height=150)
        lblpname=Label(addcartframe,text="Product Name",font=("times new roman",15),bg="white").place(x=10,y=15)
        txtpname=Entry(addcartframe,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=10,y=50,width=150,height=25)
        lblpprice=Label(addcartframe,text="Price Per Qty",font=("times new roman",15),bg="white").place(x=180,y=15)
        txtpprice=Entry(addcartframe,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=180,y=50,width=150,height=25)
        lblpqty=Label(addcartframe,text="Quantity",font=("times new roman",15),bg="white").place(x=350,y=15)
        txtpqty=Entry(addcartframe,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=350,y=50,width=100,height=25)
        
        self.lbl_instock=Label(addcartframe,text="In stock",font=("times new roman",15),bg="white")
        self.lbl_instock.place(x=10,y=100)
     
        btn_clear_cart=Button(addcartframe,text="Clear",command=self.clear_cart,font=("times new roman",15,"bold"),bg="lightgray").place(x=180,y=100,width=100,height=30)
        btn_add_cart=Button(addcartframe,text="Add | Update Cart",command=self.add_cart,font=("times new roman",15,"bold"),bg="orange").place(x=300,y=100,width=180,height=30)
        
        #=========================================================
        billframe=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billframe.place(x=1080,y=120,width=450,height=470)
        
        btitle=Label(billframe,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="orange").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billframe,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        self.txt_bill_area=Text(billframe,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)
        
        billmenuframe=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billmenuframe.place(x=1080,y=600,width=450,height=150)
        
        self.lbl_amnt=Label(billmenuframe,text='Bill Amount \n [0]',font=("goudy old style",15,"bold"),bg='green')
        self.lbl_amnt.place(x=5,y=5,width=130,height=70)
        self.lbl_discount=Label(billmenuframe,text='Discount \n [5%]',font=("goudy old style",15,"bold"),bg='red')
        self.lbl_discount.place(x=140,y=5,width=130,height=70)
        self.lbl_netpay=Label(billmenuframe,text='Net Pay \n [0]',font=("goudy old style",15,"bold"),bg='blue')
        self.lbl_netpay.place(x=280,y=5,width=160,height=70)
        
        btn_print=Button(billmenuframe,text='Print',command=self.print_bill,font=("goudy old style",15,"bold"),bg='gray')
        btn_print.place(x=5,y=80,width=130,height=50)
        btn_clear=Button(billmenuframe,text='Clear All',command=self.clear_all,font=("goudy old style",15,"bold"),bg='lightgreen')
        btn_clear.place(x=140,y=80,width=130,height=50)
        btn_generate=Button(billmenuframe,text='Generate Bill',command=self.generate_bill,font=("goudy old style",15,"bold"),bg='skyblue')
        btn_generate.place(x=280,y=80,width=160,height=50)
        
        self.update_time()
        #===========================================================
        
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.productTable.delete(*self.productTable.get_children())
            for row in rows:
               self.productTable.insert('',END,values=row)                
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input should be requirred",parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.productTable.delete(*self.productTable.get_children())
                    for row in rows:
                       self.productTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found|||",parent=self.root)
                            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root) 
            
    def get_data(self,ev):
        f=self.productTable.focus()
        content=(self.productTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')
        
    def get_data_cart(self,ev):
        f=self.cartTable.focus()
        content=(self.cartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In stock [{str(row[4])}]")
        self.var_stock.set(row[4])
        
        
    def add_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error',"Please select product from the list",parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror('Error',"Quantity is Required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror('Error',"Invalid Quantity",parent=self.root)
        else:
            price_cal=self.var_price.get()
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            present='no'
            index=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index+=1
            if present=='yes':
                op=messagebox.askyesno('confirm',"product already present\nDo you want to Update | Remove from the Cart List",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index)
                    else:
                        self.cart_list[index][3]=self.var_qty.get()
            else:
                self.cart_list.append(cart_data)        
            self.show_cart()
            self.bill_updates()
    
    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-((self.bill_amnt*5)/100)
        self.lbl_amnt.config(text=f'Bill Amnt\n{str(self.bill_amnt)}')    
        self.lbl_netpay.config(text=f'Net Pay\n{str(self.net_pay)}')    
        self.carttitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")
            
    def show_cart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for row in self.cart_list:
               self.cartTable.insert('',END,values=row)                
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror('Error',f"Customer Deatils are required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror('Error',f"Please Add product to the Cart!!!",parent=self.root)
        else:
            self.bill_top()
            self.bill_middle()
            self.bill_bottom()
            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close() 
            messagebox.showinfo('Saved',"Bill has been Generated/Saved in Backend",parent=self.root)
            self.chk_print=1           
                   
    def bill_top(self):
        self.invoice=time.strftime("%I%M%S")+time.strftime("%d%m%y")
        bill_top_temp=f'''
\t\t\tXYZ-Inventory
\tPhone No.88054***** , Delhi-1235001
{str("="*47)}
Customer Name: {self.var_cname.get()}
Ph No. :{self.var_contact.get()}\t\t\tTime: {str(time.strftime("%I-%M"))}
BillNo. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%y"))}
{str("="*47)}
Product Name \t\tPrice\tQTY\tTotal Price
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)
        
    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
Bill Amount\t\t\t\tRs.{self.bill_amnt}
Discount\t\t\t\tRs.{self.discount}
Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*47)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)
        
    def bill_middle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                price=row[2]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'
                Total_price=float(row[2])*int(row[3])
                Total_price=str(Total_price)
                self.txt_bill_area.insert(END,"\n"+name+"\t\t"+price+"\t"+row[3]+"\tRs."+Total_price)
                cur.execute('Update product set qty=?,status=? where pid=?',(
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_instock.config(text=f"In stock")
        self.var_stock.set('')
        
    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.var_search.set('')
        self.txt_bill_area.delete('1.0',END)
        self.carttitle.config(text=f"Cart \t Total Product: [0]")
        self.clear_cart()
        self.show()
        self.show_cart()
        
    def update_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date : {str(date_)}\t\t Time : {str(time_)}")
        self.lbl_clock.after(200,self.update_time)
        
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('Print',"Please generate bill, to print the receipt",parent=self.root)
            
    def logout(self):
        self.root.destroy()
        os.system("python login.py")
                            
if __name__=="__main__":    
    root=Tk()
    obj=billClass(root)
    root.mainloop()   
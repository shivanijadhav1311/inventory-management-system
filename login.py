from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
import time
class login_system:

    def __init__(self,root):
        self.root=root
        self.root.geometry("1600x800+0+0")
        self.root.title("Login System    |   Developed By Shivani")
        self.root.config(bg="white")
        
        self.employee_id=StringVar()
        self.password=StringVar()
        
        self.phoneimg=ImageTk.PhotoImage(file="images/phone.png")
        self.lblphoneimg=Label(self.root,image=self.phoneimg,bd=0).place(x=200,y=50)
        
        Loginframe=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Loginframe.place(x=650,y=90,width=350,height=500)
        title=Label(Loginframe,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)
        lbluser=Label(Loginframe,text="Employee ID",font=("Andalus",15),bg="white").place(x=50,y=100)
        txtuser=Entry(Loginframe,textvariable=self.employee_id,font=("times new roman",15),bg="lightyellow").place(x=50,y=150,width=250)
        lblpass=Label(Loginframe,text="Password",font=("Andalus",15),bg="white").place(x=50,y=200)
        txtpass=Entry(Loginframe,textvariable=self.password,show="*",font=("times new roman",15),bg="lightyellow").place(x=50,y=250,width=250)
        btn_login=Button(Loginframe,text="Log In",command=self.login,font=("Arial Rounded MT Bold",15),bg="lightblue",activebackground="lightblue").place(x=50,y=300,width=250,height=40)
        hr=Label(Loginframe,bg="lightgray").place(x=50,y=390,width=250,height=2)
        or_=Label(Loginframe,text="OR",bg="white",fg="gray",font=("times new roman",15,"bold")).place(x=150,y=375)
        btn_forget=Button(Loginframe,text="Forget Password?",command=self.forget,font=("times new roman",15,"bold"),activebackground="white",bg="white",bd=0).place(x=100,y=430)
        
        self.img1=ImageTk.PhotoImage(file="images/im1.png")
        self.img2=ImageTk.PhotoImage(file="images/im2.png")
        self.img3=ImageTk.PhotoImage(file="images/im3.png")
        
        self.lbl_change_image=Label(self.root,bg="white")
        self.lbl_change_image.place(x=365,y=150,width=240,height=430)
        
        self.animate()
        
    def animate(self):
        self.img=self.img1
        self.img1=self.img2
        self.img2=self.img3
        self.img3=self.img 
        self.lbl_change_image.config(image=self.img)
        self.lbl_change_image.after(2000,self.animate)
        
    def login(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror('Error',"All fields are required",parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? AND pass=?",(self.employee_id.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror('Error',"Invalid USERNAME / PASSWORD",parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   
            
    def forget(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror('Error',"Employee ID must be required",parent=self.root)
            else:
                cur.execute("select * from employee where eid=?",(self.employee_id.get()))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror('Error',"Invalid Employee ID, try agian",parent=self.root)
                else:
                    #=================
                   
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()
                    #call send_mail_function()
                                      
                    self.forget_win=Toplevel(self.root)
                    self.forget_win.title("RESET PASSWORD")
                    self.forget_win.geometry('400x350+500+100')
                    self.forget_win.focus_force()
                        
                    title=Label(self.forget_win,text='Reset Password',font=('goudy old style',15,'bold'),bg="pink").pack(side=TOP,fill=X)
                    
                    lbl_new_pass=Label(self.forget_win,text="New Password",font=("times new roman",15)).place(x=20,y=50)
                    txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=100,width=250,height=30)
                    lbl_c_pass=Label(self.forget_win,text="Confirm Password",font=("times new roman",15)).place(x=20,y=150)
                    txt_c_pass=Entry(self.forget_win,textvariable=self.var_conf_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=200,width=250,height=30)
                    self.btn_submit=Button(self.forget_win,text="SUBMIT",command=self.update_pass,font=("times new roman",15),bg="lightblue")
                    self.btn_submit.place(x=150,y=250,width=100,height=30)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root) 
    
    def update_pass(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Error","Password is required",parent=self.forget_win)
        elif self.var_new_pass.get()!=self.var_conf_pass.get():
            messagebox.showerror("Error","New Password & confirm password should be same",parent=self.forget_win)            
        else:
            con=sqlite3.connect(database=r'ims.db')
            cur=con.cursor()
            try:
                cur.execute("Update employee SET pass=? where eid=?",(self.var_new_pass.get(),self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Success","Password update sucessfully",parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root) 
                                      
if __name__=="__main__":    
    root=Tk()
    obj=login_system(root)
    root.mainloop()   
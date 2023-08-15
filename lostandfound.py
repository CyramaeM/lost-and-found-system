import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector as mysql
from datetime import datetime

def database():
    global cursor, db

    db = mysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="app"
    )
    cursor = db.cursor()

    create_query_reporter = """CREATE TABLE IF NOT EXISTS reporter(
        reporter_id INT AUTO_INCREMENT PRIMARY KEY,
        fname VARCHAR(255),
        lname VARCHAR(255),
        contact VARCHAR(25),
        address VARCHAR(255),
        gender VARCHAR(1)
    )"""

    cursor.execute(create_query_reporter)

    create_query_claimant = """CREATE TABLE IF NOT EXISTS claimant (
        claimant_id INT AUTO_INCREMENT PRIMARY KEY,
        fname VARCHAR(255),
        lname VARCHAR(255),
        contact VARCHAR(25),
        address VARCHAR(255),
        gender VARCHAR(1)
    )"""

    cursor.execute(create_query_claimant)

    create_query_lost_items = """CREATE TABLE IF NOT EXISTS lost_items(
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    reporter_id INT,
    claimant_id INT,
    FOREIGN KEY(reporter_id) REFERENCES reporter(reporter_id),
    FOREIGN KEY(claimant_id) REFERENCES claimant(claimant_id),
    role VARCHAR(25),
    report_date DATE,
    claim_date DATE,
    description VARCHAR(255),
    rep_time TIME,
    claim_time TIME,
    location VARCHAR(255)
    )"""


    cursor.execute(create_query_lost_items)


def Delete():
    database()
    if not tree.selection():
        messagebox.showwarning("WARNING","Select data to delete")
    else:
        result = messagebox.askquestion("CONFIRM"," Are you sure you want to delete this record?", icon="warning")
        if result=="yes":
            db = mysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="app"
        )
            cursor = db.cursor()
            for selecteditem in tree.selection():
                cursor.execute("DELETE FROM lost_items WHERE item_id= %s",(tree.set(selecteditem,"#1"),))
                db.commit()
                tree.delete(selecteditem)
            db.close()

def Search():
    database()
    if search_text.get() != "":
        tree.delete(*tree.get_children())
        try:
            # Try to parse the search date in the given format 'dd-mm-yyyy'
            parsed_date = datetime.strptime(search_text.get(), '%d-%m-%Y')
            formatted_date = parsed_date.strftime('%Y-%m-%d')  # Convert to 'YYYY-MM-DD' format

            cursor.execute("SELECT lost_items.item_id, lost_items.report_date,lost_items.rep_time,lost_items.claim_date,lost_items.claim_time, lost_items.description,lost_items.location, reporter.reporter_id, claimant.claimant_id FROM lost_items LEFT JOIN claimant ON lost_items.claimant_id = claimant.claimant_id LEFT JOIN reporter ON lost_items.reporter_id = reporter.reporter_id WHERE report_date = %s", (formatted_date,))
            fetch = cursor.fetchall()
            for data in fetch:
                item_id = data[0]
                report_date = data[1]
                report_time = data[2]
                claim_date = data[3]
                claim_time = data[4]
                description = data[5]
                location = data[6]
                reporter_id = data[7]
                claimant_id = data[8]
                
                status = "Claimed" if claimant_id is not None else "Not Claimed"
        
                tree.insert("", "end", values=(item_id, report_date,report_time,claim_date,claim_time, description,location, reporter_id, claimant_id, status))
            cursor.close()
            db.close()
        except ValueError:
            messagebox.showinfo("Warning", "Invalid date format. Use 'dd-mm-yyyy' format.", icon="warning")
def DisplayData():
    database()
    tree.delete(*tree.get_children())
    cursor.execute("SELECT lost_items.item_id, lost_items.report_date,lost_items.rep_time,lost_items.claim_date,lost_items.claim_time, lost_items.description,lost_items.location, reporter.reporter_id, claimant.claimant_id FROM lost_items LEFT JOIN claimant ON lost_items.claimant_id = claimant.claimant_id LEFT JOIN reporter ON lost_items.reporter_id = reporter.reporter_id ORDER BY report_date")
    fetch = cursor.fetchall()
    for data in fetch:
        item_id = data[0]
        report_date = data[1]
        report_time = data[2]
        claim_date = data[3]
        claim_time = data[4]
        description = data[5]
        location = data[6]
        reporter_id = data[7]
        claimant_id = data[8]
        
        status = "Claimed" if claimant_id is not None else "Not Claimed"
        
        tree.insert("", "end", values=(item_id, report_date,report_time,claim_date,claim_time, description,location, reporter_id, claimant_id, status))
        
    cursor.close()
    db.close()

def sort(): 
    database()
    if sort_text.get() == "Date":
        tree.delete(*tree.get_children())
        cursor.execute("SELECT lost_items.item_id, lost_items.report_date,lost_items.rep_time,lost_items.claim_date,lost_items.claim_time, lost_items.description,lost_items.location, reporter.reporter_id, claimant.claimant_id FROM lost_items LEFT JOIN claimant ON lost_items.claimant_id = claimant.claimant_id LEFT JOIN reporter ON lost_items.reporter_id = reporter.reporter_id ORDER BY report_date")
        fetch = cursor.fetchall()
        for data in fetch:
            item_id = data[0]
            report_date = data[1]
            report_time = data[2]
            claim_date = data[3]
            claim_time = data[4]
            description = data[5]
            location = data[6]
            reporter_id = data[7]
            claimant_id = data[8]
            
            status = "Claimed" if claimant_id is not None else "Not Claimed"
            
            tree.insert("", "end", values=(item_id, report_date,report_time,claim_date,claim_time, description,location, reporter_id, claimant_id, status))
            
        cursor.close()
        db.close()

 
    elif sort_text.get() == "Claimed":
        tree.delete(*tree.get_children())
        cursor.execute("SELECT lost_items.item_id, lost_items.report_date,lost_items.rep_time, lost_items.claim_date,lost_items.claim_time, lost_items.description,lost_items.location, reporter.reporter_id, claimant.claimant_id FROM lost_items LEFT JOIN claimant ON lost_items.claimant_id = claimant.claimant_id LEFT JOIN reporter ON lost_items.reporter_id = reporter.reporter_id WHERE claimant.claimant_id IS NOT NULL ORDER BY claim_date")
        fetch = cursor.fetchall()
        for data in fetch:
            item_id = data[0]
            report_date = data[1]
            report_time = data[2]
            claim_date = data[3]
            claim_time = data[4]
            description = data[5]
            location = data[6]
            reporter_id = data[7]
            claimant_id = data[8]
                
            status = "Claimed"
            
            tree.insert("", "end", values=(item_id, report_date,report_time,claim_date,claim_time, description,location, reporter_id, claimant_id, status))
            
        cursor.close()
        db.close()

    elif sort_text.get() == "Not Claimed":
        tree.delete(*tree.get_children())
        cursor.execute("SELECT lost_items.item_id, lost_items.report_date,lost_items.rep_time, lost_items.claim_date,lost_items.claim_time, lost_items.description,lost_items.location, reporter.reporter_id, claimant.claimant_id FROM lost_items LEFT JOIN claimant ON lost_items.claimant_id = claimant.claimant_id LEFT JOIN reporter ON lost_items.reporter_id = reporter.reporter_id WHERE claimant.claimant_id IS NULL ORDER BY report_date")
        fetch = cursor.fetchall()
        for data in fetch:
            item_id = data[0]
            report_date = data[1]
            report_time = data[2]
            claim_date = data[3]
            claim_time = data[4]
            description = data[5]
            location = data[6]
            reporter_id = data[7]
            claimant_id = data[8]
            
            status = "Not Claimed"
            
            tree.insert("", "end", values=(item_id, report_date,report_time,claim_date,claim_time, description,location, reporter_id, claimant_id, status))
            
        cursor.close()
        db.close()


def Displayform():

    def clear():
        tree.delete(*tree.get_children())
        entry_search.delete(0,END)
        entry_first_name.delete(0,END)
        entry_last_name.delete(0,END)
        entry_gender.delete(0,END)
        entry_contact_number.delete(0,END)
        entry_address.delete(0,END)
        entry_date.delete(0,END)
        entry_description.delete(0,END)
        entry_location.delete(0,END)

    def register():

        window1 = Toplevel()
        window1.geometry("400x400")
        window1.title("Report item")

        global entry_first_name,entry_last_name,entry_contact_number,entry_gender,entry_date,entry_description,entry_location
        global droplist

        def Report():
                database()
                first_name = first_Name_text.get()
                last_name = last_Name_text.get()
                gender = Gender_text.get()
                contact = contact_number_text.get()
                address = address_text.get()
                date = date_text.get()
                describe = entry_description.get("1.0", "end-1c")
                locate = location_text.get()

                if first_name == "" or last_name == "" or gender == "" or contact == "" or address == "" or date == "" or describe == "":
                    messagebox.showinfo("Warning", "Fill the Empty field!", icon="warning")
                    return

                try:
                    db = mysql.connect(
                        host="localhost",
                        user="root",
                        password="root",
                        database="app"
                    )
                    cursor = db.cursor()

                    try:
                        # Try to parse the date in the given format 'dd-mm-yyyy'
                        parsed_date = datetime.strptime(date, '%d-%m-%Y')
                        formatted_date = parsed_date.strftime('%Y-%m-%d')  # Convert to 'YYYY-MM-DD' format
                        now = datetime.now()
                    except ValueError:
                            messagebox.showinfo("Warning", "Invalid date format. Use 'dd-mm-yyyy' format.", icon="warning")
                            return

                    # Insert into reporter table
                    sql = ("INSERT INTO reporter (fname, lname, gender, contact, address) VALUES (%s, %s, %s, %s, %s)")
                    val = (first_name, last_name, gender, contact, address)
                    cursor.execute(sql, val)
                    reporter_id = cursor.lastrowid

                    # Insert into lost_items table
                    sql1 = ("INSERT INTO lost_items (reporter_id, role, report_date, description,location,rep_time) VALUES (%s, %s, %s, %s,%s,%s)")
                    val2 = (reporter_id, "reporter", formatted_date, describe,locate,now)
                    cursor.execute(sql1, val2)

                    db.commit()
                    messagebox.showinfo("Message", "Stored Successfully")
                    DisplayData()

                except mysql.Error as e:
                    print("Error:", e)
                    db.rollback()
                    messagebox.showerror("Error", "An error occurred while inserting data.")

                finally:
                    db.close()

                entry_search.delete(0, END)
                entry_first_name.delete(0, END)
                entry_last_name.delete(0, END)
                entry_gender.delete(0, END)
                entry_address.delete(0, END)
                entry_contact_number.delete(0, END)
                entry_location.delete(0, END)
                entry_description.delete("1.0", END)

                window1.destroy()

        label_id= Label(window1,text="first name")
        label_id.place(x=10,y=50)
        entry_first_name= Entry(window1,textvariable= first_Name_text)
        entry_first_name.place(x=70,y=50)

        label_name = Label(window1,text="Last Name")
        label_name.place(x=10,y=90)
        entry_last_name = Entry(window1, textvariable=last_Name_text)
        entry_last_name.place(x=70,y=90)

        label_gender = Label(window1,text="Gender")
        label_gender.place(x=10,y=125)
        entry_gender = Entry(window1, textvariable= Gender_text)
        list1 =['F','M']
        droplist = OptionMenu(window1,Gender_text,*list1)
        droplist.config(width=5,height=1)
        Gender_text.set('F')
        droplist.place(x=60,y=115)

        label_contact= Label(window1,text="Contact Number")
        label_contact.place(x=10,y=160)
        entry_contact_number = Entry(window1, textvariable=contact_number_text)
        entry_contact_number.place(x=115,y=160)

        label_address = Label(window1,text="Address")
        label_address.place(x=10,y=190)
        entry_address = Entry(window1,textvariable=address_text)
        entry_address.place(x=70,y=190)

        label_date = Label(window1,text="Date")
        label_date.place(x=10,y=220)
        entry_date = Entry(window1,textvariable=date_text)
        entry_date.place(x=75,y=220)

        label_location =Label(window1,text="Location")
        label_location.place(x=10,y=250)
        entry_location = Entry(window1,textvariable=location_text)
        entry_location.place(x=75,y=250)

        label_description =Label(window1,text="Description")
        label_description.place(x=10,y=280)
        entry_description = tk.Text(window1,width=30,height=5)
        entry_description.grid(row=5, column=1, padx=5, pady=5)
        entry_description.place(x=75,y=280)



        buttonAdd = Button(window1,text="report",width=12,command=Report)
        buttonAdd.place(x=150,y=370)

        window1.mainloop()

    def Update():

        #UPDATE BUTTON FUNCTION

        if not tree.selection():
            messagebox.showwarning("Warning","Select data to Update",icon="warning")
        else:
            result =messagebox.askquestion('Confirm', 'Are you sure you want to update this item?',icon="question")
            if result == 'yes':
                window2= Toplevel()
                window2.geometry("400x400")
                window2.title("Update item")

                global entry_first_name,entry_last_name,entry_contact_number,entry_gender,entry_date,entry_address


                def update1():
                    database()
                    d1 = first_Name_text.get()
                    d2 = last_Name_text.get()
                    d3 = Gender_text.get()
                    d4 = contact_number_text.get()
                    d5 = address_text.get()
                    d6 = date_text.get()

                    selected = tree.selection()  # Get the selected item

                    if not selected:
                        messagebox.showwarning("Warning", "Select an item to update", icon="warning")
                        return

                    item_id = tree.set(selected, "#1")  # Get the item_id from the selected item

                    db = mysql.connect(
                        host="localhost",
                        user="root",
                        passwd="root",
                        database="app"
                    )
                    cursor = db.cursor()

                    try:
                        # Try to parse the date in the given format 'dd-mm-yyyy'
                        parsed_date = datetime.strptime(d6, '%d-%m-%Y')
                        formatted_date = parsed_date.strftime('%Y-%m-%d')  # Convert to 'YYYY-MM-DD' format
                        now = datetime.now()
                    except ValueError:
                            messagebox.showinfo("Warning", "Invalid date format. Use 'dd-mm-yyyy' format.", icon="warning")
                            return

                    # Update claimant table
                    cursor.execute(
                        "INSERT INTO claimant (fname, lname, gender, contact, address) VALUES (%s, %s, %s, %s, %s) "
                        "ON DUPLICATE KEY UPDATE fname=VALUES(fname), lname=VALUES(lname), gender=VALUES(gender), "
                        "contact=VALUES(contact), address=VALUES(address)",
                        (d1, d2, d3, d4, d5)
                    )
                    claimant_id = cursor.lastrowid

                    # Update lost_items table
                    cursor.execute(
                        "UPDATE lost_items SET claimant_id=%s, role=%s, claim_date=%s,claim_time=%s WHERE item_id=%s",
                        (claimant_id, "claimant", formatted_date,now, item_id)
                    )

                    db.commit()
                    cursor.close()
                    DisplayData()
                    db.close()

                    entry_search.delete(0, END)
                    entry_first_name.delete(0, END)
                    entry_last_name.delete(0, END)
                    entry_gender.delete(0, END)
                    entry_contact_number.delete(0, END)
                    entry_address.delete(0, END)
                    entry_date.delete(0, END)
                    
                    window2.destroy()
                                    

                label_id= Label(window2,text="first name")
                label_id.place(x=10,y=50)
                entry_first_name= Entry(window2,textvariable= first_Name_text)
                entry_first_name.place(x=70,y=50)

                label_name = Label(window2,text="Last Name")
                label_name.place(x=10,y=90)
                entry_last_name = Entry(window2, textvariable=last_Name_text)
                entry_last_name.place(x=70,y=90)

                label_gender = Label(window2,text="Gender")
                label_gender.place(x=10,y=125)
                entry_gender = Entry(window2, textvariable= Gender_text)
                list1 =['F','M']
                droplist = OptionMenu(window2,Gender_text,*list1)
                droplist.config(width=5,height=1)
                Gender_text.set('F')
                droplist.place(x=60,y=115)

                label_contact= Label(window2,text="Contact Number")
                label_contact.place(x=10,y=160)
                entry_contact_number = Entry(window2, textvariable=contact_number_text)
                entry_contact_number.place(x=115,y=160)

                label_address = Label(window2,text="Address")
                label_address.place(x=10,y=190)
                entry_address = Entry(window2,textvariable=address_text)
                entry_address.place(x=70,y=190)

                label_date = Label(window2,text="Date")
                label_date.place(x=10,y=220)
                entry_date = Entry(window2,textvariable=date_text)
                entry_date.place(x=75,y=220)



                
                button_update=Button(window2,text="Update",width=12,command=update1)
                button_update.place(x=150,y=280)

                #button_update = Button(window, text="Update", width=12, command=update1(tree.selection()))

                window2.mainloop()


    #--------------------------------------contacts WINDOW-------------------------
    def contacts():
        window3 = Tk()
        window3.geometry("900x500")
        window3.title("Contact List")

        def reporterContacts():
            database()
            tree2.delete(*tree2.get_children())
            db = mysql.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="app"
            )
            cursor = db.cursor()
            cursor.execute("SELECT reporter.*,lost_items.item_id FROM reporter INNER JOIN lost_items ON lost_items.reporter_id = reporter.reporter_id")
            fetch = cursor.fetchall()
            for data in fetch:
                reporter_id = data[0]
                reporter_fname = data[1]
                reporter_lname = data[2]
                reporter_gender = data[5]
                reporter_contact = data[3]
                reporter_address = data[4]
                item_id = data[6]
                tree2.insert('', 'end', values=(reporter_id,reporter_fname, reporter_lname, reporter_gender, reporter_contact, reporter_address,item_id,"Reporter" ))
            db.commit()
            db.close()

        def claimantContact():
            database()
            tree2.delete(*tree2.get_children())
            db = mysql.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="app"
            )
            cursor = db.cursor()
            cursor.execute("SELECT claimant.*,lost_items.item_id FROM claimant INNER JOIN lost_items ON lost_items.claimant_id = claimant.claimant_id")
            fetch = cursor.fetchall()
            for data in fetch:
                claimant_id = data[0]
                claimant_fname = data[1]
                claimant_lname = data[2]
                claimant_gender = data[5]
                claimant_contact = data[3]
                claimant_address = data[4]
                item_id = data[6]
                tree2.insert('', 'end', values=(claimant_id, claimant_fname, claimant_lname, claimant_gender, claimant_contact, claimant_address, item_id,"Claimant"))
            db.commit()
            db.close()

        
    #----------------------BUTTONS FOR CONTACTLIST-----------------------

        button_display=Button(window3,text="Claimant",width=12, command=claimantContact)
        button_display.place(x=50,y=80)

        button_add=Button(window3,text="Reporter",width=12,command=reporterContacts)
        button_add.place(x=150,y=80)
        #----------------------TREE---------------------------

        tree2= ttk.Treeview(window3,selectmode='browse')
        tree2.place(x=10,y=150)
        vsb= ttk.Scrollbar(window3, orient ="vertical",command=tree2.yview)
        vsb.place(x=850,y=150,height=225)
        tree2.configure(yscrollcommand=vsb.set)
        tree2["columns"]=("1","2","3","4","5","6","7","8")
        tree2["show"]="headings"
        tree2.column("1",width =50,anchor='c') 
        tree2.column("2",width =130,anchor='c')
        tree2.column("3",width =150,anchor='c')
        tree2.column("4",width =100,anchor='c')
        tree2.column("5",width =100,anchor='c')
        tree2.column("6",width =100,anchor='c')
        tree2.column("7",width =110,anchor='c')
        tree2.column("8",width =110,anchor='c')
        tree2.heading("1",text="ID")
        tree2.heading("2",text="first name")
        tree2.heading("3",text="last name")
        tree2.heading("4",text="gender")
        tree2.heading("5",text="contact number")
        tree2.heading("6",text="address")
        tree2.heading("7",text="Item ID")
        tree2.heading("8",text="Role")


        reporterContacts()

        window3.mainloop()





    #----------------------------------------------------
    window= Tk()
    window.geometry("1200x430")
    window.title("Lost and Found System")
    global tree
    global first_Name_text,Gender_text,last_Name_text,date_text,description_text,contact_number_text,address_text,search_text,sort_text


    search_text=StringVar()
    first_Name_text= StringVar()
    last_Name_text= StringVar()
    Gender_text= StringVar()
    contact_number_text= StringVar()
    address_text= StringVar()
    description_text= StringVar()
    date_text= StringVar()
    sort_text=StringVar()
    location_text = StringVar()

    entry_first_name=Entry(window,textvariable=first_Name_text)
    entry_last_name=Entry(window,textvariable=last_Name_text)
    entry_gender=Entry(window,textvariable=Gender_text)
    entry_address=Entry(window,textvariable=address_text)
    entry_contact_number=Entry(window,textvariable=contact_number_text)
    entry_date=Entry(window,textvariable=date_text)
    entry_description=Entry(window,textvariable=description_text)
    entry_location=Entry(window,textvariable=location_text)
    

    label_space=Label(window,text="             ")
    label_space.grid(row=2,column=2)

    label_searchId=Label(window,text="Search")
    label_searchId.grid(row=3,column=1)
    entry_search=Entry(window,textvariable=search_text)
    entry_search.grid(row=3,column=2)

    label_space1=Label(window,text="            ")
    label_space1.grid(row=4,column=0)

    #label_sort=Label(window,text="Sort by")
    #label_sort.place(x=140,y=136)
    #entry_sort=Entry(window,textvariable=sort_text)
    list4=['Claimed','Not Claimed','Date']
    droplist= OptionMenu(window,sort_text,*list4)
    droplist.config(width=10)
    sort_text.set('Date')
    droplist.place(x=250,y=132)


    #-----------------------BUTTONS-----------------
    button_search=Button(window,text="Search",width=10,command=Search)
    button_search.place(x=207,y=20)

    button_delete=Button(window,text="Delete",width=10,command=Delete)
    button_delete.place(x=300,y=20)

    button_display=Button(window,text="Display All",width=12, command=DisplayData)
    button_display.place(x=39,y=80)

    button_add=Button(window,text="Report",width=12,command=register)
    button_add.place(x=140,y=80)

    button_update=Button(window,text="Update",width=12,command=Update)
    button_update.place(x=240,y=80)

    button_Sort=Button(window,text="Sort",width=7,command=sort)
    button_Sort.place(x=185,y=136)

    button_clear=Button(window,text="Clear",width=9,command=clear)
    button_clear.place(x=620,y=130)

    button_list=Button(window,text="Contact List",width=10,command=contacts)
    button_list.place(x=700,y=20)

    #--------------------------TREE VIEW------------------------


    tree = ttk.Treeview(window,selectmode='browse')
    tree.place(x=10,y=170)
    vsb= ttk.Scrollbar(window, orient ="vertical",command=tree.yview)
    vsb.place(x=1150,y=170,height=225)
    tree.configure(yscrollcommand=vsb.set)
    tree["columns"]=("1","2","3","4","5","6","7","8","9","10")

    tree["show"]="headings"
    tree.column("1",width =110,anchor='c') 
    tree.column("2",width =130,anchor='c') 
    tree.column("3",width =130,anchor='c') 
    tree.column("4",width =160,anchor='c')
    tree.column("5",width =100,anchor='c') 
    tree.column("6",width =100,anchor='c') 
    tree.column("7",width =100,anchor='c') 
    tree.column("8",width =100,anchor='c')
    tree.column("9",width =100,anchor='c')
    tree.column("10",width =100,anchor='c')

    tree.heading("1",text="ID")
    tree.heading("2",text="Report date")
    tree.heading("3",text="Report Time")
    tree.heading("4",text="Claim date")
    tree.heading("5",text="Claim Time")
    tree.heading("6",text="Description")
    tree.heading("7",text="Location")
    tree.heading("8",text="Reporter ID")
    tree.heading("9",text="Claimant ID")
    tree.heading("10",text="Status")

    DisplayData()


#Displayform()
if __name__ == "__main__":
    Displayform()
    mainloop()

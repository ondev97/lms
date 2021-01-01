# Main module to handle everything for client side

from tkinter import *
from tkinter import ttk
import tkinter as tk

from backend import Backend


class FrontEndTwo:

    def __init__(self, window):
        self.cars_list = []
        self.accessories_list = []
        self.backend = Backend()
        self.selected_car = None
        self.selected_accessories = []
        self.total_price = 0.0
        self.root = window



        self.root.title("FutureARROW Car Sale")
        self.root.geometry("1200x672+0+0")
        self.root.resizable(False, False)

        self.backend.createConnection()

        self.title = Label(self.root, text="FutureARROW Car Sale", bd=4, relief=GROOVE,
                           font=("times new roman", 40, "bold"))
        self.title.pack(side=TOP, fill=X)

        self.detail_frame = Frame(self.root, bd=4, relief=RIDGE)
        self.detail_frame.place(x=0, y=70, width=1198, height=600)

        self.car_frame = Frame(self.detail_frame, bd=4, relief=RIDGE)
        self.car_frame.place(x=10, y=10, width=860, height=230)

        self.car_title = Label(self.car_frame, text="Cars", font=("times new roman", 15, "bold"))
        self.car_title.grid(row=0, columnspan=2, pady=20, padx=30)

        self.car_lbl_search = Label(self.car_frame, text="Search By", font=("times new roman", 10))
        self.car_lbl_search.grid(row=0, column=3, pady=10, padx=20, sticky='w')

        self.car_combobox = StringVar()
        self.car_combo_search = ttk.Combobox(self.car_frame, font=("times new roman", 10), state="readonly",
                                             textvariable=self.car_combobox)
        self.car_combo_search['values'] = (
            "Reg.No", "Color", "Model No", "Model Name", "Manufacturer Id", "Manufacturer Name")
        self.car_combo_search.grid(row=0, column=4, padx=20, pady=10)
        self.car_combo_search.current(0)

        self.car_search = StringVar()
        self.car_txt_search = Entry(self.car_frame, font=("times new roman", 10), bd=4, relief=GROOVE,
                                    textvariable=self.car_search)
        self.car_txt_search.grid(row=0, column=5, pady=10, padx=20, sticky='w')

        self.car_search_btn = Button(self.car_frame, text="Search", width=10, command=self.set_car_data).grid(
            row=0, column=6, padx=20, pady=10)
        self.car_showall_btn = Button(self.car_frame, text="Show All", width=10, command=self.car_showall).grid(row=0, column=7, padx=20,
                                                                                      pady=10)

        self.car_table_frame = Frame(self.car_frame, bd=4, relief=RIDGE)
        self.car_table_frame.place(x=10, y=60, width=830, height=150)

        self.car_scroll_y = Scrollbar(self.car_table_frame, orient=VERTICAL)
        self.car_table = ttk.Treeview(self.car_table_frame,
                                      columns=("reg_no", "color", "no_of_doors", "manufacturer_id", "manufacturer_name",
                                               "model_no", "model_name", "model_price"),
                                      yscrollcommand=self.car_scroll_y.set)
        self.car_scroll_y.pack(side=RIGHT, fill=Y)
        self.car_scroll_y.config(command=self.car_table.yview)
        self.car_table.heading("reg_no", text="Reg.No")
        self.car_table.heading("color", text="Color")
        self.car_table.heading("no_of_doors", text="No Of Doors")
        self.car_table.heading("model_no", text="Model No")
        self.car_table.heading("model_name", text="Model Name")
        self.car_table.heading("model_price", text="Price")
        self.car_table.heading("manufacturer_id", text="Manufacturer Id")
        self.car_table.heading("manufacturer_name", text="Manufacturer Name")
        self.car_table['show'] = 'headings'
        self.car_table.column("reg_no", width=20)
        self.car_table.column("color", width=20)
        self.car_table.column("no_of_doors", width=30)
        self.car_table.column("model_no", width=30)
        self.car_table.column("model_name", width=60)
        self.car_table.column("model_price", width=20)
        self.car_table.column("manufacturer_id", width=30)
        self.car_table.column("manufacturer_name", width=60)
        self.car_table.pack(fill=BOTH, expand=1)
        self.car_table.bind("<Double-1>", self.car_doubleclick)

        self.accessory_frame = Frame(self.detail_frame, bd=4, relief=RIDGE)
        self.accessory_frame.place(x=10, y=250, width=300, height=332)

        self.accessory_title = Label(self.accessory_frame, text="Accessories", font=("times new roman", 15, "bold"))
        self.accessory_title.grid(row=0, column=0, pady=20, padx=30)

        self.accessory_search = StringVar()
        self.accessory_txt_search = Entry(self.accessory_frame, font=("times new roman", 10), bd=4,
                                          relief=GROOVE,
                                          textvariable=self.accessory_search)
        self.accessory_txt_search.grid(row=1, column=0, pady=10, padx=20, sticky='w')

        self.accessory_search_btn = Button(self.accessory_frame, text="Search", width=10,
                                           command=self.set_accessory_data).grid(
            row=1, column=1, padx=20, pady=10)
        self.accessory_showall_btn = Button(self.accessory_frame, text="Show All", width=10,
                                            command=self.accessory_showall).grid(
            row=0, column=1, padx=20, pady=10)

        self.accessory_table_frame = Frame(self.accessory_frame, bd=4, relief=RIDGE)
        self.accessory_table_frame.place(x=10, y=120, width=272, height=192)

        self.accessory_scroll_y = Scrollbar(self.accessory_table_frame, orient=VERTICAL)
        self.accessory_table = ttk.Treeview(self.accessory_table_frame, columns=("id", "name", "price"),
                                            yscrollcommand=self.accessory_scroll_y.set)
        self.accessory_scroll_y.pack(side=RIGHT, fill=Y)
        self.accessory_scroll_y.config(command=self.accessory_table.yview)
        self.accessory_table.heading("id", text="Id")
        self.accessory_table.heading("name", text="Name")
        self.accessory_table.heading("price", text="Price")
        self.accessory_table['show'] = 'headings'
        self.accessory_table.column("id", width=10)
        self.accessory_table.column("name", width=60)
        self.accessory_table.column("price", width=40)
        self.accessory_table.pack(fill=BOTH, expand=1)
        self.accessory_table.bind("<Double-1>", self.accessory_doubleclick)

        self.manage_frame = Frame(self.detail_frame, bd=4, relief=RIDGE)
        self.manage_frame.place(x=320, y=250, width=550, height=100)

        self.accessory_lbl_id = Label(self.manage_frame, text="Id", font=("times new roman", 10))
        self.accessory_lbl_id.grid(row=0, column=0, pady=10, padx=20, sticky='w')

        self.accessory_id = StringVar()
        self.accessory_txt_id = Entry(self.manage_frame, font=("times new roman", 10), bd=5, relief=GROOVE,
                                      textvariable=self.accessory_id, state="readonly")
        self.accessory_txt_id.grid(row=1, column=0, pady=10, padx=20, sticky='w')

        self.accessory_lbl_qty = Label(self.manage_frame, text="Quantity", font=("times new roman", 10))
        self.accessory_lbl_qty.grid(row=0, column=1, pady=10, padx=20, sticky='w')

        self.accessory_qty = IntVar()
        self.accessory_txt_qty = Entry(self.manage_frame, font=("times new roman", 10), bd=5, relief=GROOVE,
                                        textvariable=self.accessory_qty)
        self.accessory_txt_qty.grid(row=1, column=1, pady=10, padx=20, sticky='w')

        self.accessory_clear_btn = Button(self.manage_frame, text="Clear", width=10, command=self.clear_list_item).grid(row=0, column=2, padx=10, pady=10)
        self.accessory_removeall_btn = Button(self.manage_frame, text="Remove All", width=10, command=self.removeall_list_item).grid(row=0, column=3, padx=10, pady=10)
        self.accessory_add_btn = Button(self.manage_frame, text="Add", width=10, command=self.add_list_item).grid(row=1, column=2, padx=10, pady=10)
        self.accessory_remove_btn = Button(self.manage_frame, text="Remove", width=10, command=self.remove_list_item).grid(row=1, column=3, padx=10, pady=10)

        self.price_frame = Frame(self.detail_frame, bd=4, relief=RIDGE)
        self.price_frame.place(x=320, y=360, width=550, height=223)

        self.total_price_lbl = Label(self.price_frame, text="Total Price :", font=("times new roman", 15, "bold"))
        self.total_price_lbl.grid(row=0, column=0, pady=10, padx=10, sticky='w')

        self.price_lbl = Label(self.price_frame, text="0", font=("times new roman", 15, "bold"))
        self.price_lbl.grid(row=1, column=1, pady=10, padx=10, sticky='w')

        self.msg_lbl = Label(self.price_frame, text="If you are ready to buy this vihicle with selected upgrades, click 'PROCEED'", font=("times new roman", 12))
        self.msg_lbl.grid(row=2, columnspan=3, pady=10, padx=26, sticky='w')

        self.proceed_btn = Button(self.price_frame, text="PROCEED", width="41", font=("times new roman", 15, "bold"))
        self.proceed_btn.grid(row=3, columnspan=3, padx=20, pady=10)



        self.currency_frame = Frame(self.detail_frame, bd=4, relief=RIDGE)
        self.currency_frame.place(x=880, y=10, width=300, height=55)

        self.currency_lbl = Label(self.currency_frame, text="Currency", font=("times new roman", 15, "bold"))
        self.currency_lbl.grid(row=0, column=0, pady=10, padx=10, sticky='w')

        self.currency_combobox_txt = StringVar()
        self.currency_combobox = ttk.Combobox(self.currency_frame, font=("times new roman", 10), state="readonly",
                                             textvariable=self.currency_combobox_txt)
        self.currency_combobox['values'] = (
            "Dollar")
        self.currency_combobox.grid(row=0, column=1, padx=20, pady=10)
        self.currency_combobox.current(0)

        self.list_frame = Frame(self.detail_frame, bd=4, relief=RIDGE)
        self.list_frame.place(x=880, y=75, width=300, height=508)

        self.list_title = Label(self.list_frame, text="List", font=("times new roman", 15, "bold"))
        self.list_title.grid(row=0, columnspan=2, pady=20, padx=30)

        self.list_table_frame = Frame(self.list_frame, bd=4, relief=RIDGE)
        self.list_table_frame.place(x=10, y=60, width=273, height=430)

        self.list_scroll_y = Scrollbar(self.list_table_frame, orient=VERTICAL)
        self.list_table = ttk.Treeview(self.list_table_frame, columns=("id", "qty", "price"),
                                       yscrollcommand=self.list_scroll_y.set)
        self.list_scroll_y.pack(side=RIGHT, fill=Y)
        self.list_scroll_y.config(command=self.list_table.yview)
        self.list_table.heading("id", text="Id")
        self.list_table.heading("qty", text="Qty")
        self.list_table.heading("price", text="Price")
        self.list_table['show'] = 'headings'
        self.list_table.column("id", width=50)
        self.list_table.column("qty", width=5)
        self.list_table.column("price", width=50)
        self.list_table.pack(fill=BOTH, expand=1)
        self.list_table.bind("<Double-1>", self.list_doubleclick)

        # Method Calls =======================================================================

        self.set_car_data()
        self.set_accessory_data()
        self.set_list_data()

    def set_car_data(self):
        search_by = self.car_combobox.get()
        condition = self.car_search.get().strip()
        self.cars_list = self.backend.viewCars("")
        self.car_table.delete(*self.car_table.get_children())
        for car in self.cars_list:
            if search_by == "Reg.No":
                if condition == "":
                    self.car_table.insert("", tk.END, values=(
                        car.getRegNo(), car.getColor(), car.getNoOfDoors(), car.getManufacturer().getId(),
                        car.getManufacturer().getName(), car.getModel().getModelNo(), car.getModel().getName(),
                        car.getModel().getPrice()))
                else:
                    if car.getRegNo().find(condition) != -1:
                        self.car_table.insert("", tk.END, values=(
                            car.getRegNo(), car.getColor(), car.getNoOfDoors(), car.getManufacturer().getId(),
                            car.getManufacturer().getName(), car.getModel().getModelNo(), car.getModel().getName(),
                            car.getModel().getPrice()))
            elif search_by == "Color":
                if condition == "":
                    self.car_table.insert("", tk.END, values=(
                        car.getRegNo(), car.getColor(), car.getNoOfDoors(), car.getManufacturer().getId(),
                        car.getManufacturer().getName(), car.getModel().getModelNo(), car.getModel().getName(),
                        car.getModel().getPrice()))
                else:
                    if car.getColor().find(condition) != -1:
                        self.car_table.insert("", tk.END, values=(
                            car.getRegNo(), car.getColor(), car.getNoOfDoors(), car.getManufacturer().getId(),
                            car.getManufacturer().getName(), car.getModel().getModelNo(), car.getModel().getName(),
                            car.getModel().getPrice()))
            elif search_by == "Model No":
                if condition == "":
                    self.car_table.insert("", tk.END, values=(
                        car.getRegNo(), car.getColor(), car.getNoOfDoors(), car.getManufacturer().getId(),
                        car.getManufacturer().getName(), car.getModel().getModelNo(), car.getModel().getName(),
                        car.getModel().getPrice()))
                else:
                    if car.getModel().getModelNo().find(condition) != -1:
                        self.car_table.insert("", tk.END, values=(
                            car.getRegNo(), car.getColor(), car.getNoOfDoors(), car.getManufacturer().getId(),
                            car.getManufacturer().getName(), car.getModel().getModelNo(), car.getModel().getName(),
                            car.getModel().getPrice()))
            elif search_by == "Model Name":
                if condition == "":
                    self.car_table.insert("", tk.END, values=(
                        car.getRegNo(), car.getColor(), car.getNoOfDoors(), car.getManufacturer().getId(),
                        car.getManufacturer().getName(), car.getModel().getModelNo(), car.getModel().getName(),
                        car.getModel().getPrice()))
                else:
                    if car.getModel().getModelName().find(condition) != -1:
                        self.car_table.insert("", tk.END, values=(
                            car.getRegNo(), car.getColor(), car.getNoOfDoors(), car.getManufacturer().getId(),
                            car.getManufacturer().getName(), car.getModel().getModelNo(), car.getModel().getName(),
                            car.getModel().getPrice()))

            elif search_by == "Manufacturer Id":
                if condition == "":
                    self.car_table.insert("", tk.END, values=(
                        car.getRegNo(), car.getColor(), car.getNoOfDoors(), car.getManufacturer().getId(),
                        car.getManufacturer().getName(), car.getModel().getModelNo(), car.getModel().getName(),
                        car.getModel().getPrice()))
                else:
                    if car.getManufacturer().getId().find(condition) != -1:
                        self.car_table.insert("", tk.END, values=(
                            car.getRegNo(), car.getColor(), car.getNoOfDoors(), car.getManufacturer().getId(),
                            car.getManufacturer().getName(), car.getModel().getModelNo(), car.getModel().getName(),
                            car.getModel().getPrice()))
            elif search_by == "Manufacturer Name":
                if condition == "":
                    self.car_table.insert("", tk.END, values=(
                        car.getRegNo(), car.getColor(), car.getNoOfDoors(), car.getManufacturer().getId(),
                        car.getManufacturer().getName(), car.getModel().getModelNo(), car.getModel().getName(),
                        car.getModel().getPrice()))
                else:
                    if car.getManufacturer().getName().find(condition) != -1:
                        self.car_table.insert("", tk.END, values=(
                            car.getRegNo(), car.getColor(), car.getNoOfDoors(), car.getManufacturer().getId(),
                            car.getManufacturer().getName(), car.getModel().getModelNo(), car.getModel().getName(),
                            car.getModel().getPrice()))
            else:
                self.car_table.insert("", tk.END, values=(
                    car.getRegNo(), car.getColor(), car.getNoOfDoors(), car.getManufacturer().getId(),
                    car.getManufacturer().getName(), car.getModel().getModelNo(), car.getModel().getName(),
                    car.getModel().getPrice()))

    def car_showall(self):
        self.car_search.set("")
        self.set_car_data()

    def accessory_showall(self):
        self.accessory_search.set("")
        self.set_accessory_data()

    def set_accessory_data(self):
        condition = self.accessory_search.get().strip()
        self.accessories_list = self.backend.viewAccessories("")
        self.accessory_table.delete(*self.accessory_table.get_children())
        for accessory in self.accessories_list:
            if condition == "":
                self.accessory_table.insert("", tk.END, values=(accessory.getId(), accessory.getName(), accessory.getPrice()))
            else:
                if accessory.getName().find(condition) != -1 or accessory.getId().find(condition) != -1:
                    self.accessory_table.insert("", tk.END, values=(accessory.getId(), accessory.getName(), accessory.getPrice()))

    def car_doubleclick(self,event):
        item = self.car_table.selection()
        for i in item:
            for c in self.cars_list:
                if c.getRegNo() == self.car_table.item(i, "values")[0]:
                    if self.selected_car == None:
                        self.selected_car = c
                    elif self.selected_car.getRegNo() == c.getRegNo():
                        self.selected_car = None
                    else:
                        self.selected_car = c
        self.set_list_data()

    def set_list_data(self):
        self.list_table.delete(*self.list_table.get_children())
        if self.selected_car != None:
            self.list_table.insert("", tk.END, values=(self.selected_car.getRegNo(), 1, self.selected_car.getModel().getPrice()))
        for a in self.selected_accessories:
            self.list_table.insert("", tk.END, values=(a[0].getId(), a[1], a[0].getPrice()))
        self.set_total_price()

    def add_list_item(self):
        id = self.accessory_id.get().strip()
        qty = self.accessory_qty.get()
        list = self.selected_accessories
        if id != "" and qty != 0:
            for a in self.selected_accessories:
                print(a[0].getId(), id)
                if a[0].getId() == id:
                    temp = a
                    list.remove(temp)
                    list.append((temp[0], qty))
                    break
            else:
                for ac in self.accessories_list:
                    if ac.getId() == id:
                        list.append((ac, qty))
            self.selected_accessories = list
            self.set_list_data()

    def remove_list_item(self):
        id = self.accessory_id.get().strip()
        if id != "":
            for a in self.selected_accessories:
                if a[0].getId() == id:
                    self.selected_accessories.remove(a)
                    break
            self.set_list_data()

    def removeall_list_item(self):
        self.selected_car = None
        self.selected_accessories = []
        self.set_list_data()

    def clear_list_item(self):
        self.accessory_id.set("")
        self.accessory_qty.set(0)

    def accessory_doubleclick(self, event):
        item = self.accessory_table.selection()
        for i in item:
            for a in self.accessories_list:
                self.accessory_id.set(self.accessory_table.item(i, "values")[0])

    def list_doubleclick(self,event):
        item = self.list_table.selection()
        for i in item:
            for c in self.accessories_list:
                if c.getId() == self.list_table.item(i, "values")[0]:
                    self.accessory_id.set(self.list_table.item(i, "values")[0])
                    self.accessory_qty.set(self.list_table.item(i, "values")[1])
                    break
            else:
                self.selected_car = None
                self.set_list_data()

    def set_total_price(self):
        total_price = 0.00
        if self.selected_car!=None:
            total_price +=self.selected_car.getModel().getPrice()
        for a in self.selected_accessories:
            total_price += a[0].getPrice() * a[1]
        self.total_price = total_price
        self.price_lbl.config(text="{:.2f}".format(total_price))

root = Tk()
ob = FrontEndTwo(root)
root.mainloop()

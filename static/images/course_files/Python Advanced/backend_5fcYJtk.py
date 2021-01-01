# To deal with database

import sqlite3
from sqlite3 import Error

from classes import Model, Manufacturer, Car, Accessory


class Backend:

    def __init__(self):
        self.connection = None
        self.cursor = None

    def createConnection(self):
        self.connection = None
        try:
            self.connection = sqlite3.connect("pythonsqlite3.db")
            self.cursor = self.connection.cursor()
        except Error as e:
            print(e)

    def removeConnection(self):
        try:
            self.connection.close()
        except Error as e:
            print(e)

    def createTables(self):
        try:
            self.cursor.execute("PRAGMA foreign_keys = ON")
            self.cursor.execute("CREATE TABLE model(model_no TEXT PRIMARY KEY, name TEXT NOT NULL, price REAL NOT NULL)")
            self.cursor.execute("CREATE TABLE accessory(id TEXT PRIMARY KEY, name TEXT NOT NULL, price REAL NOT NULL)")
            self.cursor.execute("CREATE TABLE manufacturer(id TEXT PRIMARY KEY, name TEXT NOT NULL)")
            self.cursor.execute("CREATE TABLE car(reg_no TEXT PRIMARY KEY, color TEXT NOT NULL, no_of_doors INTEGER NOT NULL, "
                                "model TEXT  NOT NULL, manufacturer TEXT NOT NULL, "
                                "CONSTRAINT fk_model FOREIGN KEY (model) REFERENCES Model(model_no) ON DELETE RESTRICT , "
                                "CONSTRAINT fk_manufacturer FOREIGN KEY(manufacturer) REFERENCES Manufacturer(id) ON DELETE RESTRICT )")
            self.cursor.execute(
                "CREATE TABLE sale(car_reg_no TEXT PRIMARY KEY, timestamp TIMESTAMP NOT NULL, final_amount REAL NOT NULL, "
                "CONSTRAINT fk_car FOREIGN KEY (car_reg_no) REFERENCES Car(reg_no) ON DELETE RESTRICT)")
            self.cursor.execute(
                "CREATE TABLE upgrade(car_reg_no TEXT, accessory_id TEXT NOT NULL, "
                "PRIMARY KEY (car_reg_no, accessory_id), "
                "CONSTRAINT fk_car FOREIGN KEY (car_reg_no) REFERENCES Car(reg_no) ON DELETE RESTRICT, "
                "CONSTRAINT fk_accessory FOREIGN KEY (accessory_id) REFERENCES Accessory(id) ON DELETE RESTRICT)")
            return "tables were successfully created"
        except Error as e:
            return  e

    def removeTables(self):
        pass

    def viewModels(self, condition):
        models = []
        try:
            self.cursor.execute('SELECT * FROM model')
            rows = self.cursor.fetchall()
            for row in rows:
                models.append(Model(row[0],row[1],row[2]))
        except Error as e:
            return models
        return models

    def getModel(self, model_no):
        model = None
        try:
            self.cursor.execute("SELECT * FROM model WHERE model_no='"+model_no+"'")
            rows = self.cursor.fetchall()
            for row in rows:
                model = Model(row[0], row[1], row[2])
        except Error as e:
            return model
        return model


    def addModel(self, model):
        con1 = model.getModelNo()==None or model.getModelNo().strip()==""
        con2 = model.getName()==None or model.getName().strip()==""
        con3 = model.getPrice()==None or model.getPrice()==0
        if con1 or con2 or con3:
            return "you have missed something"
        try:
            self.cursor.execute("INSERT INTO model VALUES(?,?,?)",(model.getModelNo(), model.getName(), model.getPrice()))
            self.connection.commit()
            return "successfully added into database"
        except Error as e:
            return e

    def removeModel(self, model):
        con1 = model.getModelNo() == None or model.getModelNo().strip() == ""
        if con1:
            return "you have missed something"
        try:
            self.cursor.execute("DELETE FROM model WHERE model_no='"+model.getModelNo()+"'")
            self.connection.commit()
            return "successfully deleted from database"
        except Error as e:
            return e

    def updateModel(self, model):
        con1 = model.getModelNo() == None or model.getModelNo().strip() == ""
        con2 = model.getName() == None or model.getName().strip() == ""
        con3 = model.getPrice() == None or model.getPrice() == 0
        if con1 or con2 or con3:
            return "you have missed something"
        try:
            self.cursor.execute("UPDATE model SET name = '" + model.getName() + "', price = " + str(model.getPrice()) +" WHERE model_no = '" + model.getModelNo() + "'")
            self.connection.commit()
            return "successfully updated the row of database"
        except Error as e:
            return e

    def viewManufacturers(self, condition):
        manufacturers = []
        try:
            self.cursor.execute('SELECT * FROM manufacturer')
            rows = self.cursor.fetchall()
            for row in rows:
                manufacturers.append(Manufacturer(row[0], row[1]))
        except Error as e:
            return manufacturers
        return manufacturers

    def getManufacturer(self, id):
        manufacturer = None
        try:
            self.cursor.execute("SELECT * FROM manufacturer WHERE id='"+id+"'")
            rows = self.cursor.fetchall()
            for row in rows:
                manufacturer = Manufacturer(row[0], row[1])
        except Error as e:
            return manufacturer
        return manufacturer

    def addManufacturer(self, manufacturer):
        con1 = manufacturer.getId() == None or manufacturer.getId().strip() == ""
        con2 = manufacturer.getName() == None or manufacturer.getName().strip() == ""
        if con1 or con2:
            return "you have missed something"
        try:
            self.cursor.execute("INSERT INTO manufacturer VALUES(?,?)", (manufacturer.getId(), manufacturer.getName()))
            self.connection.commit()
            return "successfully added into database"
        except Error as e:
            return e

    def removeManufacturer(self, manufacturer):
        con1 = manufacturer.getId() == None or manufacturer.getId().strip() == ""
        if con1:
            return "you have missed something"
        try:
            self.cursor.execute("DELETE FROM manufacturer WHERE id='" + manufacturer.getId() + "'")
            self.connection.commit()
            return "successfully deleted from database"
        except Error as e:
            return e

    def updateManufacturer(self, manufacturer):
        con1 = manufacturer.getId() == None or manufacturer.getId().strip() == ""
        con2 = manufacturer.getName() == None or manufacturer.getName().strip() == ""
        if con1 or con2:
            return "you have missed something"
        try:
            self.cursor.execute("UPDATE manufacturer SET name = '" + manufacturer.getName() + "' WHERE id = '" + manufacturer.getId() + "'")
            self.connection.commit()
            return "successfully updated the row of database"
        except Error as e:
            return e

    def viewCars(self, condition):
        cars = []
        try:
            self.cursor.execute('SELECT * FROM car')
            rows = self.cursor.fetchall()
            for row in rows:
                cars.append(Car(row[0], row[1], row[2], self.getModel(row[3]), self.getManufacturer(row[4])))
        except Error as e:
            return cars
        return cars

    def addCar(self, car):
        con1 = car.getRegNo() == None or car.getRegNo().strip() == ""
        con2 = car.getColor() == None or car.getColor().strip() == ""
        con3 = car.getNoOfDoors() == None or car.getNoOfDoors() == 0
        con4 = car.getModel() == None
        con5 = car.getManufacturer() == None
        if con1 or con2 or con3 or con4 or con5:
            return "you have missed something"
        try:
            self.cursor.execute("INSERT INTO car VALUES(?,?,?,?,?)", (car.getRegNo(), car.getColor(), car.getNoOfDoors(), car.getModel().getModelNo(), car.getManufacturer().getId()))
            self.connection.commit()
            return "successfully added into database"
        except Error as e:
            return e

    def removeCar(self, car):
        try:
            self.cursor.execute("DELETE FROM car WHERE reg_no='" + car.getRegNo() + "'")
            self.connection.commit()
            return "successfully deleted from database"
        except Error as e:
            return e

    def viewAccessories(self, condition):
        accessories = []
        try:
            self.cursor.execute('SELECT * FROM accessory')
            rows = self.cursor.fetchall()
            for row in rows:
                accessories.append(Accessory(row[0],row[1],row[2]))
        except Error as e:
            return accessories
        return accessories

    def getAccessory(self, id):
        accessory = None
        try:
            self.cursor.execute("SELECT * FROM accessory WHERE id='"+id+"'")
            rows = self.cursor.fetchall()
            for row in rows:
                accessory = Accessory(row[0], row[1], row[2])
        except Error as e:
            return accessory
        return accessory


    def addAccessory(self, accessory):
        con1 = accessory.getId() == None or accessory.getId().strip() == ""
        con2 = accessory.getName() == None or accessory.getName().strip() == ""
        con3 = accessory.getPrice() == None or accessory.getPrice() == 0
        if con1 or con2 or con3:
            return "you have missed something"
        try:
            self.cursor.execute("INSERT INTO accessory VALUES(?,?,?)",(accessory.getId(), accessory.getName(), accessory.getPrice()))
            self.connection.commit()
            return "successfully added into database"
        except Error as e:
            return e

    def removeAccessory(self, accessory):
        con1 = accessory.getId() == None or accessory.getId().strip() == ""
        if con1:
            return "you have missed something"
        try:
            self.cursor.execute("DELETE FROM accessory WHERE id='"+accessory.getId()+"'")
            self.connection.commit()
            return "successfully deleted from database"
        except Error as e:
            return e

    def updateAccessory(self, accessory):
        con1 = accessory.getId() == None or accessory.getId().strip() == ""
        con2 = accessory.getName() == None or accessory.getName().strip() == ""
        con3 = accessory.getPrice() == None or accessory.getPrice() == 0
        if con1 or con2 or con3:
            return "you have missed something"
        try:
            self.cursor.execute("UPDATE accessory SET name = '" + accessory.getName() + "', price = " + str(accessory.getPrice()) +" WHERE id = '" + accessory.getId() + "'")
            self.connection.commit()
            return "successfully updated the row of database"
        except Error as e:
            return e

    def addSale(self, sale, upgrades):
        try:
            pass
        except Error as e:
            return e


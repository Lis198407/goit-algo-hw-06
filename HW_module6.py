from collections import UserDict
import re

class WrongRecord(Exception):                                         # Exception for problem with records in AdressBook
    def __init__(self, message="No such record in address book"):
        self.message = message
        super().__init__(self.message)

class WrongPhone(Exception):                                          # Exception for problem with phones in Records
    def __init__(self, message="Error in phone"):
        self.message = message
        super().__init__(self.message)

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
		pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.is_phone = self.check_phone()                                 # Checking in auto mode Phone for 10 digits
  
    def check_phone(self):
        pattern = r'^\d\s?(\d{3}\s?){2}\d{3}$'                             # pattern for 10 digits. for 12 digits with+ '^\+?\d{1,3}\s?(\d{3}\s?){2}\d{3}$'
        return bool(re.match(pattern, self.value))                         # Use re.match to check if the string matches the pattern

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def find_by_phone(self, phone_str:str)-> Phone:                         #find a Phone obj in record by phone in str
        return next((phone for phone in self.phones if phone.value == phone_str), None)
    
    def add_phone(self, phone_str:str):                                     #Adding phone from str
        try:
            phone_to_add = Phone(phone_str)          
            if not phone_to_add.is_phone:                                    #checking the phone vs rules (10 digit)
                raise WrongPhone (f"Phone {phone_str} must have 10 digits!") # if not - message via exception
            elif phone_to_add in self.phones:                                # checking for duplicates
                raise WrongPhone (f"Phone {phone_str} already exist in this record!") #if exist - message to user via exception
            else:
                self.phones.append(phone_to_add)                             # adding the phone if it's OK
        except Exception as ex:
                print(ex)


    def del_phone(self, phone_str: str):                                        #deleting phone from record
        try:
            phone_to_del = self.find_by_phone(phone_str)                        #findind the Phone in Record by str of the phone
            if phone_to_del:
                self.phones.remove(phone_to_del)
            else:
                raise WrongPhone (f"No such phone {phone_str} in record!")  #if not found - raise a exception with message
        except Exception as ex:
            print(ex)
    
    def edit_phone(self, old_phone_str:str, new_phone_str:str):              # Editing the phone by finding the phone by phone and changing to new one
        try:
            old_phone = self.find_by_phone(old_phone_str)
            new_phone = Phone(new_phone_str)
            if old_phone and new_phone.is_phone:                             #checking if Phone to change in Record and weather new phone in Phone according to rules of 10 digits
                i = self.phones.index(old_phone)
                self.phones[i] = new_phone
            else:
                raise WrongPhone (f"Can't change phone {old_phone}. It's not in records, or {new_phone} not a phone")
        except Exception as ex:
                print(ex)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    record_count = 0                                                          #Quantity of records in Adress Book
    
    def __init__(self, name:str):
        self.name = Name(name)
        self.records = []
     
    def find(self, record_name: str) -> Record:                               #Finds Record by Name and returns Record if found
        return next((rec for rec in self.records if rec.name.value == record_name), None)
        
    def add(self, record:Record):                                             #adding the record by records
        try:
            if not self.find(record.name):                                    #checking for duplicates
                self.records.append(record)
                self.record_count +=1                                         #increasing Quantity of records in AdressBook                                
            else:
                raise WrongRecord(f"Record {record} already exist in phonebook {self.name}")
        except Exception as ex:
                print(ex)

    def delete(self, rec_name: str):                                          #deleting the Record by record Name
        try:
            record = self.find(rec_name)
            if record:                                                        # if Record in Records in AdressBook than Pop it
                self.records.remove(record)                
                self.record_count -=1
            else:
                raise WrongRecord(f"No such record {record} in phonebook {self.name}") #Raise the exception, that delete can't be made
        except Exception as ex:
                print(ex)

    def __str__(self):
        message = f"Adress Book name is {self.name.value}.\nContacts: \n"
        for record in self.records:
                message += f"{record}\n"
        return message

def main():
    book = AddressBook("FirstBook")                                     # Створення нової адресної книги

    john_record = Record("John")                                        # Створення запису для John
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_phone("666666")
    john_record.add_phone("666666666666")
    john_record.add_phone("66666666666")
    john_record.add_phone("6666666666")
    print(f"adding numbers to John, {john_record}")
    john_record.del_phone("6666666666")
    print(f"deleting phone 6666666666 {john_record}")

    book.add(john_record)                                               # Додавання запису John до адресної книги
    jane_record = Record("Jane")                                        # Створення та додавання нового запису для Jane
    jane_record.add_phone("9876543210")
    book.add(jane_record)

    print(f"Adressbook after add Jane is {book}")

    john = book.find("John")                                            # Знаходження та редагування телефону для John

    john.edit_phone("1234567890", "1112223333")
    print(f"John after edit phone 1234567890 to 1112223333 is {john}")  # Виведення: Contact name: John, phones: 1112223333; 5555555555
    
    found_phone = john.find_by_phone("5555555555")                      # Пошук конкретного телефону у записі John
    if found_phone: 
        print(f"{found_phone} is phone of {john}")                      # Виведення: 5555555555
    else:
        print(f"Record not found")
   
    book.delete("Jane")                                                # Видалення запису Jane
    print(f"Adressbook after del Jane is {book}")

if __name__ == "__main__":
    main()
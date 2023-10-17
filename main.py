from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    ...

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if len(self.value) != 10 or not self.value.isdigit():

            raise ValueError("Invalid phone number")

class Record:
    def __init__(self, name, phone = None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []

    def add_phone(self, phone):
        new_phone = ''.join(filter(str.isdigit, phone))
        if len(new_phone) != 10:
            print(f"Invalid phone length: {new_phone}")
        try:
            self.phones.append(Phone(new_phone))
        except ValueError:
            print("Invalid phone number")

    def edit_phone(self, old_phone, new_phone):
        found = False
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                found = True
        if not found:
            raise ValueError(f"The phone {old_phone} is not found.")

    def find_phone(self, phone:str):
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return None
    
    def remove_phone(self, phone):
        del_phone = None
        for ph in self.phones:
            if ph.value == phone:
                del_phone = ph
        self.phones.remove(del_phone)
        
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):

    def add_record(self,new_contact:Record) -> None:
        self.data[new_contact.name.value] = new_contact
        return f"Contact {new_contact.name.value} added succefully"

    def find(self, name):
        for rec in self.data:
            if rec == name:
                return self.data[rec]
        if not self.data.get(name):
            return None

    def delete(self, name):
        if not self.data.get(name):
            return f"did't delete contact {name}, not exsist"
        else:
            del self.data[name]
            return f"Contact {name} delete succsefull"


records = AddressBook()


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Give me name and phone please"
        except KeyError:
            return "Enter correct user name"
        except ValueError as e:
            if str(e) == "Not enough number":
                return "Not enought number"
            else:
                raise e  # Піднімаэмо помилку наверх, якщо вона іншого типу
    return inner

def sanitize_phone_number(phone):
    collected_phone = ""
    for ch in phone:
        collected_phone += ch
    new_phone = (
        collected_phone.strip()
            .removeprefix("+38")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
    )
    if len(new_phone) == 10:
         return new_phone
    # if len(new_phone) == 13:
    #      return new_phone
    else: 
        raise ValueError("Not enough number")
    
@user_error
def add_record(*args):
    name = args[0]
    phone_number = sanitize_phone_number(args[1:])
    if not records.data.get(name):
        name_record = Record(name)
        name_record.add_phone(phone_number)
        records.add_record(name_record)
    else:
        name_record = records.data.get(name)
        name_record.add_phone(phone_number)
    return f"Add record {name = }, {phone_number = }"

@user_error
def change_record(*args):
    name = args[0]
    old_phone_number = sanitize_phone_number(args[1])
    new_phone_number = sanitize_phone_number(args[2])
    print(old_phone_number, new_phone_number)

    if not records.data.get(name):
        raise ValueError("wrong name")
    else:
        name_record = records.data.get(name)
        name_record.edit_phone(old_phone_number, new_phone_number)
        return f"Change record {name = }, {new_phone_number = }"

def delete_record(*args):
    name = args[0]
    records.delete(name)
    return f"Contact name: {name}, delete successfull"

def unknown_cmd(*args):
    return "Unknown command. Try again. Or use 'help'"

def hello_cmd(*args):
    return "How can I help you?"

def help_cmd(*args):
    return_str = "\n"
    cmd_list = ["avalible command:",
            "hello - just say hello",
            "help - show avalible cmd",
            "add - add record - format 'name phone'",
            "change - change record - format 'name old phone new phone'",
            "delete - delete record - format 'name'",
            "phone - get phone by name - format 'phone name'",
            "show all - show all phone book",
            "good bye/close/exit - shotdown this script"]
    for ch in cmd_list:
        return_str += ch + "\n"
    return return_str

@user_error
def get_phone(*args):
    name = args[0]
    rec = records.find(name)
    if rec:
        return rec
    
@user_error 
def show_all(*args):
    return_str = "\n"
    for _, numbers in records.data.items() :
        return_str += str(numbers) + "\n"
    return return_str

def close_cmd(*args):
    return "Good bye!"

COMMANDS = {add_record: "add",
            # add_phone: "add phone",
            # edit_phone: "edit phone",
            delete_record: "delete",
            change_record: "change",
            hello_cmd: "hello",
            get_phone: "phone",
            show_all: "show all",
            help_cmd: "help",
            close_cmd: ("good bye", "close", "exit")}

def parser(text: str):
    for func, kw in COMMANDS.items():
        if text.lower().startswith(kw):
            return func, text[len(kw):].strip().split()
    return unknown_cmd, []

def main():
    while True:
        user_input = input(">>>")
        func, data = parser(user_input)
        print(func(*data))
        if func == close_cmd:
            break


if __name__ == "__main__":
    main()
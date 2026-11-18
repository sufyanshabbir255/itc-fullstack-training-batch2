# encapsulation, inheritance,polymorphism,abstraction

#encapsulation
class facebook:
    def __init__(self,username,password):
        self.username = "qwerty" #can we use it both as string/non string?
        self.__password = password

    def login(self,password):
        if password ==self.__password:
            print("login success")
        else:
            print("unsuccess")
    def change_password(self, old_password, new_password):
            if old_password == self.__password:
                print("password changed successfully")
            else:
                print("wrong old password")
#now create object
user1 = facebook ("qwerty","a123")
print(user1.username)
user1.login("a123")
user1.change_password("a123","xyz12")
user1.login("xyz12")


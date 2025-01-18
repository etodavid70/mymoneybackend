


# name= "eto david"
# age= 14
# hieght= 1.4556
# is_dark= True




# variables

details=[ "eto", "david", 14, ]



#turples are immutable
details_turple= ("eto", "david", 14, 0.5)

#unpacking a turple

w,x,y,z =details_turple

# print(w, x, y, z)

#key-value pairs
dictionary={
"name":"samuel eto",
"age": 14,
"height": 2.5,
"is_dark": False
}
#the keys are always strings, while the values can be any datatype

# print(dictionary["is_dark"])


#parameters


def sum(a, b, c):
  print("hello world")
  return a+b+c
  # print("hello world")

#every line of code after the return statement is invalid

#positional argument
# print(sum(12, 4, 7))

#keyword argument

#concepts of object oriented programming

#classes
#objects
#inheritance
#polymorphism
#encapsulation
#abstraction


#classes
#a class contains 
# attributes(variables) and 
# methods(functions): whenever a method is being created, always pass the self paramter


#parent class
class Details:
  #attributes
  name="eto david"
  age= 14
  height=2.4
  is_dark=True

  #method
  def display_details(self):
    
    print(f"""
  name : {self.name},
 age: {self.age},
 height: {self.height},
 is he dark: {self.is_dark}
    
    """)


#an object is the representation of a class, 
#is an instance of a class
#it simply means representing a class with a variable

#object of parent
my_details= Details()

# print(my_details.name)
# print(my_details.age)
# print(my_details.height)
# print(my_details.is_dark)
# my_details.display_details()

#child class
class DetailsSecond(Details):
  pass

#object of child class
details2= DetailsSecond()

# print(details2.name)
# printdetails2.age)
# print(details2.height)
# print(details2.is_dark)
# details2.display_details()



#parent class
class Button:
  def __init__(self, background, border, hieght, width):
    self.background=background
    self.border=border
    self.height=hieght
    self.width=width
  
  def on_click(self):
    print("the button has been clicked", [self.background,self.border, self.height,self.width ] )

# btn= Button(background="white", hieght=2.5, width=4.5,border=4.5 )

# #child class
class NewButton(Button):
  
  def __init__(self, background, border, hieght, width, animation, duration): 
    #call all at the attributes of parent class and child class
    super().__init__(background, border, hieght, width)
    #call only the attribute of the parent class in the super function


    self.animation=animation
    self.duration=duration


  def on_click_new(self):
    print("this is the new method")



# btn2= NewButton(background="white", border=2.4, hieght=3.5, width=3.0, animation="3D", duration=4.5,)
  

#assignment
#study and practice copiously on multi-level inheritance,
#abstraction


#polymorphism

class Display:
  def display(self):
    print("this is the old result")

# display_obj= Display()

# display_obj.display()

class NewDisplay(Display):

  def display(self):
    print("this is the new display")

display_obj= NewDisplay()
display_obj.display()
  

#encapsulation

class Me:
  def __init__(self, name, age):
    self.name=name
    self.age=age
    account="102456679"
    self.__pin="1234"


me= Me(name="eto david", age=14)
print(me._account) #can be accessed, however with discretion
print(me.__pin) #cant be accessed


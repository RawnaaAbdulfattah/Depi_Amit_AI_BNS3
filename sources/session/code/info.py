# def info_std(name :str, age :int):
#     print(f"my name is {name},my age is {age}")
def calc():
    print("Welcome to the simple calculator by Rawnaa :)")
    try:
        num1=float(input("enter the first number"))
        num2=float(input("enter the first number"))
    except:
        print("invalid input, please enter a numeric value")
    choice=input("choose an operation: 1.addition\n2.subtraction\n3.multiplication\n4.division\nor 'exit' for quit")
    def add(num1,num2):
        print(f"{num1} + {num2} = ",num1+num2)
    def sub(num1,num2):
        print(f"{num1} - {num2} = ",num1-num2)
    def muliply(num1,num2):
        print(f"{num1} * {num2} = ",num1*num2)
    def div(num1,num2):
        try:
            print(f"{num1} / {num2} = ",num1/num2)
        except:
            print("Error:division by zero")
    if choice=='1':
        add(num1,num2)
    elif choice=='2':
        sub(num1,num2)
    elif choice=='3':
        muliply(num1,num2)
    elif choice=='4':
        div(num1,num2)
    elif choice=='exit':
        print("Thanks for using simple calculator, Goodbye")
    else:
        print("unvalid input, enter your choice again!")
calc()
        
        
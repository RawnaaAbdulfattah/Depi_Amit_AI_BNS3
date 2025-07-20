"""
while True:
        print("\nWelcome to the Simple Calculator!")
        print("Select an operation:")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
    
        choice = input("Enter your choice (1/2/3/4) or 'exit' to quit: ")
        class calc:

            def __init__(self,n1,n2):
                self.n1=n1              # TASK
                self.n2=n2
            def add(self):
                return self.n1 + self.n2
            def sub(self):
                return self.n1-self.n2
            def multiply(self):
                return self.n1*self.n2
            def div(self):
                return self.n1/self.n2
                

        if choice == 'exit':
            print("Exiting the calculator. Goodbye!")
            break

        if choice not in ('1', '2', '3', '4'):
            print("Invalid input: Please enter 1, 2, 3, 4, or 'exit'.")
            continue

        try:
            n1 = float(input("Enter first number: "))
            n2 = float(input("Enter second number: "))
        except :
            print("Invalid input: Please enter numeric values.")
            continue
        c1=calc(n1,n2)
        if choice == '1':
            print(f"{n1}+{n2} = ",c1.add())
        elif choice == '2':
            print(f"{n1}-{n2} = ",c1.sub())
        elif choice == '3':
            print(f"{n1}*{n2} = ",c1.multiply())
        else:
            try:
                n1/n2
                print(f"{n1}/{n2} = ",c1.div())
            except:
                    print("Error:dividing by zero")
                """
    

import os
import random

def handle_directory(base_path: str):
   
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    folder_paths = [] 
    for i in range(10):
        inner_path = os.path.join(base_path, f"dir_{i}")
        os.makedirs(inner_path, exist_ok=True)
        folder_paths.append(inner_path)
        print(len(folder_paths))
    random_dir=random.choice(folder_paths)
    print(random_dir)
    for i in range(5):
        print("deleted:",random_dir)
        os.rmdir(random_dir)
        folder_paths.remove(random_dir)
base_path = "C:/Users/Computer Market/Desktop/Depi/Depi_Amit_AI_BNS3/sources/session/code/directories"
handle_directory(base_path)
     
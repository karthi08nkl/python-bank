import random
from datetime import datetime
print("----------BANK----------")
print("----------------------------------\n")
atm = {}
transaction = {}

try:
    with open("atm.txt","r") as file:
        for line in file:
            acc_num,name,balance,pin = line.strip().split(",")
            atm[int(acc_num)] = [name,float(balance),int(pin)]
except ValueError:
    pass

def transactions(acc_num,message):
    with open("transaction.txt","a") as file:
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        file.write(f"{acc_num},{current_time},{message}\n")

def save_accounts():
    with open("atm.txt","w") as file:
        for acc_num,details in atm.items():
            name,balance,pin = details
            file.write(f"{acc_num},{name},{balance},{pin}\n")

def create_account():
    name = input("Enter Name : ")
    balance =0
    while True: 
        try:
            pin = int(input("Enter Pin : "))
            break
        except ValueError:
            print("Pin must be only in numbers")
    while True:
        acc_num = random.randint(100000,999999)
        if acc_num not in atm:
            break
    atm[acc_num] = [name,balance,pin]
    print(f"Your Account Number is : {acc_num}\n")
    return name, pin, acc_num

def login():
    
    acc_num = int(input("Enter Account Number : "))
    pin = int(input("Enter Pin : "))

    return acc_num , pin

while True:
    print("1.Create Account")
    print("2.Check Balance")
    print("3.Deposit Money")
    print("4.Withdraw Money")
    print("5.Change Pin")
    print("6.Delete Account")
    print("7.Transfer Money")
    print("8.Transaction History")
    print("9.Exit\n")

    try:
        choice = int(input("Enter your choice (1-9) : "))
    except ValueError:
        print("Enter only Valid Choice (1-9)!")
        continue

    match choice:

        case 1:
            name ,pin,acc_num = create_account()
            save_accounts()
            transactions(acc_num,"Account Created")
            
        case 2:
            acc_num , pin = login()

            if acc_num not in atm:
                print("Account Not Found!")
            elif atm[acc_num][2] != pin:
                print("Incorrect Pin!")
            else:
                print(f"Your Account Balance is {atm[acc_num][1]}\n")        

        case 3:
            acc_num = int(input("Enter Account Number : "))
            amount = float(input("Enter Deposit Amount : "))
            if amount <= 0:
                print("Amount must be greater than 0!\n")
             
            elif acc_num not in atm:
                print("Account Not Found!\n")
            
            else:
                atm[acc_num][1]+=amount
                save_accounts()
                transactions(acc_num,f"Deposit : {amount}")
                print("Deposit Successfull!\n")
        
        case 4:
            acc_num = int(input("Enter Account Number : "))

            while True:
                        try:
                            amount = float(input("Enter Amount to Tranfer : "))
                            if amount<=0:
                                print("Amount must be greater than 0!")
                            else:
                                break
                        except ValueError:
                            print("Please Enter a Valid Number!")  
            if amount <= 0:
                print("Amount must be greater than 0!\n")
            pin = int(input("Enter Pin : "))


            if acc_num not in atm:
                print("Account Not Found!\n")
            elif atm[acc_num][2] != pin:
                print("Incorrect Pin!\n")
            elif amount > atm[acc_num][1]:
                print("Insufficient Balance!\n")    
            else:
                atm[acc_num][1]-=amount    
                save_accounts()
                transactions(acc_num,f"Withdraw : {amount}")
                print("Withdraw Successfull!\n")    

        case 5:
            acc_num , pin = login()
            if acc_num not in atm:
                print("Account Not Found!\n")
            elif atm[acc_num][2] != pin:
                print("Incorrect Pin!\n")
            else:
                while True:
                    try:
                        new_pin = int(input("Enter New Pin : "))
                        break
                    except ValueError:
                        print("Pin must be only in Numbers\n")

                atm[acc_num][2] = new_pin
                save_accounts()
                transactions(acc_num,"PIN Changed")
                print("Pin changed Successfully!\n")
                        
        
        case 6:
            acc_num , pin = login()
            
            if acc_num not in atm:
                print("Account Not Found!\n")
            elif atm[acc_num][2] != pin:
                print("Incorrect Pin!\n")
            else: 
                transactions(acc_num,"Account Deleted")   
                del atm[acc_num]
                save_accounts()
                
                print("Account Deleted Successfully!\n")

        case 7:
            sender_acc_num,sender_pin = login()
            receiver_acc_num = int(input("Enter Receiver Account Number : "))

            if sender_acc_num not in atm:
                print("Account Not Found!")
            elif atm[sender_acc_num][2] != sender_pin:
                print("Incorrect Pin!\n")  
            elif receiver_acc_num not in atm:
                print("Receiver Account Not Found!\n")    
            elif sender_acc_num == receiver_acc_num:
                print("No Transaction between Same Account\n")       
            else:
                while True:
                        try:
                            amount = float(input("Enter Amount to Tranfer : "))
                            if amount<=0:
                                print("Amount must be greater than 0!")
                            else:
                                break
                        except ValueError:
                            print("Please Enter a Valid Number!")    
 
                if amount > atm[sender_acc_num][1]:
                    print("Insufficent Balance\n")      
                else:
                    atm[receiver_acc_num][1]+=amount
                    atm[sender_acc_num][1]-=amount
                    save_accounts()
                    transactions(sender_acc_num,f"Transferred {amount} to {receiver_acc_num}")
                    transactions(receiver_acc_num,f"Received {amount} from {sender_acc_num}")
                    print("Transaction Success!\n")
 
        
        
        case 8:
            acc_num , pin = login()
            if acc_num not in atm:
                print("Account Not Found!\n")
            elif atm[acc_num][2] != pin:
                print("Incorrect Pin!\n")
            else:
                try:
                    found = False
                    with open("transaction.txt","r") as file:
                        for line in file:
                            account, current_time ,message = line.strip().split(",",2)

                            if int(account) == acc_num:
                                print(current_time, "-" , message)
                                found = True
                    if not found:
                        print("No Transaction History\n")            
                except FileNotFoundError:
                    print("Transaction History Not Found\n")
                    


        case 9:
            print("----Thank You----\n")
            print("-------------------\n")
            break

        case _:
            print("INVALID CHOICE!")     
            

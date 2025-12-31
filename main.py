import sys
from datetime import datetime
from sqlalchemy import create_engine,Integer,String,Column,UniqueConstraint
from sqlalchemy.orm import declarative_base,sessionmaker
Base=declarative_base()
class USERS(Base):
    __tablename__="users"
    username=Column(String)
    DOB=Column(String)
    Acc_no=Column(Integer,primary_key=True)
    Balance=Column(Integer)
    password=Column(String)
    transactions=Column(String) 
    
engine=create_engine(r"sqlite:///C:\sqlite\Admin.db")
session=sessionmaker(bind=engine)                
s=session()

def Create_Account():
    while(True):
        try:
            username=input("Enter your Name(or type 'back' to return):")
            if username.lower()=='back':
                break
            DOB=input("Enter date of birth(or type 'back' to return):")
            if DOB.lower()=='back':
                break
            Amount=input("Enter initial amount(or type 'back' to return):")
            if Amount.lower()=='back':
                break
            Amount=int(Amount)
            password=input("Enter password(or type 'back' to return):")
            if password.lower()=='back':
                break
        except Exception as e:
            print("pls enter valid input")
 
        data=USERS(username=username,DOB=DOB,Balance=Amount,password=password,transactions='')     
        s.add(data)
        s.commit()

        print("Account created successfully.")

        user=s.query(USERS).filter(USERS.password==password).first()
        if user:
            print("your Account number is:",user.Acc_no)             
            break
        else:
            print("something went wrong")
            break
                       
def admin_access():
    while(True):
        print("-----admin dashboard-----")
        print("1.create account")
        print("2.view user details")
        print("3.delete account")
        print("4.Exit")
        try:
            choice=int(input("enter your choice(1/2/3/4):"))
        except Exception as e:
            print("pls enter valid input")
            continue

        if choice==1:
            Create_Account()         
                
        elif choice==2:
            try:
                user_acc=input("enter user accountno(or type 'back' to return):")
                if user_acc.lower()=='back':
                    continue
                user_acc=int(user_acc)
            except Exception as e:
                print("pls enter valid input")
                continue
            
            user=s.query(USERS).filter_by(Acc_no=user_acc).first()
            
            if user:                 
                print("----user details----")
                print("Name:",user.username)
                print("Acc_no:",user.Acc_no)
                print("DOB:",user.DOB)
                print("Balance:",user.Balance)  
                continue
            else:
                print("Account not found")                
                continue
                
        elif choice==3:
            try: 
                user_acc = input("enter user accountno (or type 'back' to return): ")
                if user_acc.lower() == 'back':
                    continue
                user_acc = int(user_acc)              
        
            except Exception as e:
                print("pls enter valid input")
                continue
            
               
            d=s.query(USERS).filter(USERS.Acc_no==user_acc).first()

            if d:
                s.delete(d)
                s.commit()
                print("Account deleted successfully")
            else:
                print("Account not found")
    
        elif choice==4:
            print("exit admin dashboard")
            break

        else:
            print("enter valid input from 1 to 4")
            continue

Base=declarative_base()
class Beneficiary(Base):
    __tablename__="beneficiary"
    bene_id=Column(Integer,primary_key=True)
    beneficiary_name=Column(String)
    sender_acc=Column(Integer)
    be_acc=Column(Integer)
    __table_args__ = (
        UniqueConstraint('sender_acc', 'be_acc', name='unique_pair'),
    )
    
engine=create_engine(r"sqlite:///C:\sqlite\Admin.db")
Base.metadata.create_all(engine) 
session=sessionmaker(bind=engine)                
s=session()


def user_access(user_acc):
    while True:
        print("----user dashboard-----")
        print("1.Deposit")
        print("2.Withdraw")
        print("3.Checkbalance")
        print("4.Money Transaction")
        print("5.Transactionhistory")
        print("6.view profile")
        print("7.Exit")
        try:
            option=int(input("Enter your choice 1 to 7:"))
        except Exception as e:
            print("pls enter valid input")
            continue

        if option==1:
            while(True):
                try:
                    num=int(input("enter amount:"))
                except Exception as e:
                    print("pls enter valid input")
                    continue
                if num>0:
                    break
                else:
                    print("Amount must be greater than 0")

            user=s.query(USERS).filter_by(Acc_no=user_acc).first()

            if user:
                user.Balance+=num
                print("deposit completed successfully")
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                msg=f"\namount {num} deposited successfully on {date}"
                
                if user.transactions:
                    user.transactions+=msg
                else:
                    user.transactions=msg             

                s.commit()
                break
            else:
                print("Account not found")
                break

        elif option==2:
            while(True):
                try:
                    num=int(input("enter amount:"))
                except Exception as e:
                    print("pls enter valid input")
                    continue
                if num>0:
                    break
                else:
                    print("Amount must be greater than 0")
                    continue

            user=s.query(USERS).filter_by(Acc_no=user_acc).first()
            if user:
                if user.Balance>num:
                    user.Balance-=num
                    print("withdraw completed successfully")
                else:
                    print("Insufficient Balance")
                    break

                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                msg=f"\namount {num} withdrawn successfully on {date}"
                
                if user.transactions:
                    user.transactions+=msg  
                else:   
                    user.transactions=msg
                s.commit()
                break

            else:
                print("Account not found")
                break

        elif option==3:
            user=s.query(USERS).filter_by(Acc_no=user_acc).first()
            if user:
                print("balance:",user.Balance)                   
                break
            else:
                print("Account not found")
                continue
        
        elif option==4:
            user=s.query(USERS).filter_by(Acc_no=user_acc).first()
            bene=s.query(Beneficiary).all()
            if len(bene)==0:
                print("no beneficiary added yet")
            else:
                print("beneficiary list")
                for b in bene:
                    print(f"\nName:{b.beneficiary_name} and acc_no:{b.be_acc}")           

            add_beneficiary=input("enter add beneficiary (y/n)").lower()

            if add_beneficiary=='y':

                beneficiary_name=input("enter name as per their bank account:")
                acc_no=int(input("enter account number:"))

                beneficiary=Beneficiary(beneficiary_name=beneficiary_name,be_acc=acc_no,sender_acc=user_acc)
                b=s.query(Beneficiary).filter_by(be_acc=acc_no,sender_acc=user_acc).first()
                
                if b:
                    print("account already added to beneficiary")
                    continue 
                 
                else:
                    s.add(beneficiary)
                    s.commit()
                    print("beneficiary added successfully")   

            elif add_beneficiary=='n':
                try:
                    receiver_acc=input("enter account number of receiver(or type 'back' to return):")
                    if receiver_acc.lower()=='back':
                        continue
                    receiver_acc=int(receiver_acc)
                except Exception as e:
                    print("pls enter valid input")
                    continue  

                while(True):
                    try:
                        num=int(input("enter amount:"))
                    except Exception as e:
                        print("pls enter valid input")
                        continue                    
                    if num>0:
                        break
                    else:
                        print("Amount must be greater than 0")
                    
                user=s.query(USERS).filter_by(Acc_no=user_acc).first()
                bene=s.query(Beneficiary).filter_by(be_acc=receiver_acc,sender_acc=user_acc).first()

                if bene:
                    if user.Balance>num:
                        user.Balance-=num
                        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        msg=f"\namount {num} transfered successfully to {receiver_acc} on {date}"
                
                        if user.transactions:
                            user.transactions+=msg  
                        else:   
                            user.transactions=msg
                        s.commit()
                    
        
                        rec=s.query(USERS).filter_by(Acc_no=receiver_acc).first()
                        if rec:
                            rec.Balance+=num
                            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            msg=f"\namount {num} received successfully from {user_acc} on {date}"
                
                            if rec.transactions:
                                rec.transactions+=msg  
                            else:   
                                rec.transactions=msg
                            s.commit()
                            print("money transfered successfully")

                        else:
                            print("Receiver account not found in beneficiary")
                            break
                    
                    else:
                        print("Insufficient balance")
                else:
                    print("Account not found in beneficiary")
                    break

        elif option==5:
            user=s.query(USERS).filter_by(Acc_no=user_acc).first()
            print(user.transactions)
        
        elif option==6:
               
            user=s.query(USERS).filter_by(Acc_no=user_acc).first()
            
            if user:                 
                print("----user details----")
                print("Name:",user.username)
                print("Acc_no:",user.Acc_no)
                print("DOB:",user.DOB)
                print("Balance:",user.Balance)  
                continue
            else:
                print("Account not found")                
                continue
            
        elif option==7:
            print("exit from user dashboard")
            break

        else:
            print("pls enter valid input from 1 to 7")
            continue   


Base=declarative_base()
class Admin(Base):
    __tablename__="Admin"
    admin_name=Column(String)
    admin_id=Column(Integer,primary_key=True)
    password=Column(String)
    
engine=create_engine(r"sqlite:///C:\sqlite\Admin.db")
Base.metadata.create_all(engine) 
session=sessionmaker(bind=engine)                
s=session()
data=Admin(admin_name="admin",admin_id=111,password="123")
exist=s.query(Admin).filter_by(admin_id=111).first()
if not exist:
    s.add(data)
    s.commit()

while True:
    print("welcome to bank system")
    print("1.admin login")
    print("2.user signup")
    print("3.user login")
    print("4.Exit")
    try:
        choice=int(input("Enter your choice(1/2/3/4):"))
    except Exception as e:
        print("pls enter valid input")
        continue
    if choice==1:
        try:
            admin_name=input("Enter admin name(or type 'back' to return):")
            if admin_name.lower()=='back':
                continue
            admin_id=input("Enter adminid(or type 'back' to return):")
            if admin_id.lower()=="back":
                continue
            admin_id=int(admin_id)
            password=input("Enter password(or type 'back' to return)")
            if password.lower()=='back':
                continue
            
        except Exception as e:
            print("pls enter valid input")
            continue

        R=s.query(Admin).filter_by(admin_id=111).first()
     
        if R.admin_id==admin_id:   
            admin_access()
        else:
            print("Invalid credential.try again")
            continue

    elif choice==2:
        Create_Account()
        
    elif choice==3:
        try:
            user_acc=input("Enter user accountno(or type 'back' to return):")
            if user_acc.lower()=='back':
                continue
            user_acc=int(user_acc)
                  
        except Exception as e:
            print('pls enter valid input')
            continue
        
        R=s.query(USERS).filter_by(Acc_no=user_acc).first()
        
        if R:
            print("logged in successfully") 
            user_access(user_acc)

        else:
            print("login failed.")
            continue

    elif choice==4:
        sys.exit()
    else:
        print("invalid input enter 1 to 4")
        continue
                


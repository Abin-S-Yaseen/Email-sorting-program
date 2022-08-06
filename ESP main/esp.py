import imaplib
import email
from datetime import date,timedelta,datetime
from tkinter import *
from tkinter import scrolledtext

root = Tk()
root.title('Email Sorting Program')
root.resizable(height=False,width=False)
Font = ("Comic Sans MS", 10, "bold")

def showContent():
    txt_area.delete("1.0","end")
    k = 1
    for i in range(0,len(messages)-1):
        for part in messages[i].walk():
            if part.get_content_type() == 'text/plain':
                txt_area.insert(END, f'Message Number {k}')
                txt_area.insert(END,'\n')
                txt_area.insert(END,part.get_payload())
                txt_area.insert(END,'\n')
                k += 1

def showSubject():
    txt_area.delete("1.0","end")

    for i in range(0,len(messages)):
             
        txt_area.insert(END, f'\nMessage number {i+1}')
        txt_area.insert(END,f"\nFrom: {messages[i].get('From')}")
        txt_area.insert(END,f"\nDate: {messages[i].get('Date')}")
        txt_area.insert(END,f"\nSubject: {messages[i].get('Subject')}")
        txt_area.insert(END, '\n')
        i += 1

txt_area = scrolledtext.ScrolledText(root,wrap=WORD,font=Font)
txt_area.grid(row=0,column=0,columnspan=2)
contnt_btn = Button(root,text='Content',width=7,relief=RIDGE,command=showContent)
contnt_btn.grid(row=1,column=1,ipady=7)
subject_btn = Button(root,text='Subject',width=7,relief=RIDGE,command=showSubject)
subject_btn.grid(row=1,column=0,ipady=7)

file = open('unwanted-mails.txt', 'r')
unwanted_mails = []
for i in file:
    unwanted_mails.append(i)

email_server = "imap.gmail.com"
email_id = ""                       # add your gamil id inside the string.
app_password = ""                   #obtain app password from your gmail settings and add inside the string.

time_period = (date.today()-timedelta(days=4)).isoformat()
time_period = datetime.strptime(time_period, '%Y-%m-%d').strftime('%d-%b-%Y')

imap = imaplib.IMAP4_SSL(email_server)
imap.login(email_id, app_password)
imap.select('INBOX')

_, msg_nums = imap.search(None, 'SINCE ' + time_period, 'UnSeen')  # 'UnSeen' for viewing unseen messages
msg_nums = msg_nums[0].split() 

latest_msg = int(msg_nums[-1])
oldest_msg = int(msg_nums[0])

messages = []

m = 1
for i in range(latest_msg, oldest_msg, -1):

    decision = True
    _, data = imap.fetch(str(i), "(RFC822)")
    message = email.message_from_bytes(data[0][1])

    for j in range(len(unwanted_mails)):
        if unwanted_mails[j] in (message.get('From')).lower().split():
            decision = False
            

    if decision == True:

        messages.append(message)
        
        txt_area.insert(END, f'\nMessage number {m}')
        txt_area.insert(END,f"\nFrom: {message.get('From')}")
        txt_area.insert(END,f"\nDate: {message.get('Date')}")
        txt_area.insert(END,f"\nSubject: {message.get('Subject')}")
        txt_area.insert(END, '\n')
        m += 1

        root.update()
        

imap.close()
root.mainloop()

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import sys


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            try:
              msg_list.insert(tkinter.END, msg)
            except RuntimeError:
                break
        except OSError:
            break


def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{close}":
        client_socket.close()
        top.quit()

def send_close(event=None):
    client_socket.sendall(bytes("{close}", "utf8"))
   # client_socket.close()
    top.quit()

def on_closing(event=None):
    my_msg.set("{close}")
    send()
    top.quit()

top = tkinter.Tk()
top.title("Chat Client")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
login_details = tkinter.Label(text="First message is username;\nwhitespace for anonimous.")
login_details.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, width=50, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
leave_button = tkinter.Button(top, text="Exit",command=send_close)
leave_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)
if len(sys.argv) == 3:
    print(sys.argv)
    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])
    print("Connecting to ip",HOST,", port",PORT)
else:
    print("Running with default settings: localhost,9009")
    PORT = 9009
    HOST = "localhost"
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()

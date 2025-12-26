from tkinter import *
from tkinter import messagebox
from random import randint
from captcha.image import ImageCaptcha
import time

# --- CAPTCHA generator ---
image = ImageCaptcha(fonts=['fonts/arial.ttf'])

def generate_captcha():
    global captcha_text
    captcha_text = str(randint(100000, 999999))
    image.write(captcha_text, "out.png")

# --- Shake window on wrong input ---
def shake_window():
    x = root.winfo_x()
    y = root.winfo_y()
    for _ in range(10):
        root.geometry(f"+{x+10}+{y}")
        root.update()
        time.sleep(0.02)
        root.geometry(f"+{x-10}+{y}")
        root.update()
        time.sleep(0.02)
    root.geometry(f"+{x}+{y}")

# --- Text spinner setup ---
loading = False
spinner_count = 0

def start_spinner():
    global loading, spinner_count
    loading = True
    spinner_count = 0
    spinner_label.pack(pady=5)
    animate_spinner()

def stop_spinner():
    global loading
    loading = False
    spinner_label.pack_forget()

def animate_spinner():
    global spinner_count
    if loading:
        dots = (spinner_count % 4)
        spinner_label.config(text="Loading" + "." * dots)
        spinner_count += 1
        root.after(300, animate_spinner)

# --- Verify input ---
def verify():
    user_input = entry.get().strip()
    if user_input == captcha_text:
        messagebox.showinfo("Success", "Captcha Verified")
        refresh()
    else:
        shake_window()
        messagebox.showerror("Error", "Incorrect Captcha")
        refresh()

# --- Refresh CAPTCHA ---
def refresh():
    global photo
    start_spinner()

    def finish_refresh():
        global photo
        generate_captcha()
        photo = PhotoImage(file="out.png")
        captcha_label.config(image=photo)
        captcha_label.image = photo
        entry.delete(0, END)
        entry.focus_set()
        stop_spinner()

    root.after(800, finish_refresh)  # simulate loading delay

# --- Tkinter UI ---
root = Tk()
root.title("Captcha Verification")
root.geometry("330x280")
root.resizable(False, False)

main_frame = Frame(root, padx=20, pady=20)
main_frame.pack(expand=True)

# Initial CAPTCHA
generate_captcha()
photo = PhotoImage(file="out.png")
captcha_label = Label(main_frame, image=photo)
captcha_label.image = photo
captcha_label.pack(pady=10)

# Entry widget
entry = Entry(
    main_frame,
    font=("Arial", 14),
    justify="center",
    relief="solid",
    bd=1
)
entry.pack(pady=10, fill=X)
entry.focus_set()

# Spinner label
spinner_label = Label(main_frame, text="", font=("Arial", 10), fg="gray")
spinner_label.pack_forget()

# Buttons
button_frame = Frame(main_frame)
button_frame.pack(pady=10)

verify_btn = Button(
    button_frame,
    text="Verify",
    width=10,
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    command=verify
)

refresh_btn = Button(
    button_frame,
    text="Refresh",
    width=10,
    bg="#2196F3",
    fg="white",
    activebackground="#1e88e5",
    command=refresh
)

verify_btn.grid(row=0, column=0, padx=5)
refresh_btn.grid(row=0, column=1, padx=5)

root.mainloop()

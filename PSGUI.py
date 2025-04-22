import re
from tkinter import Tk, Label, Entry, Button, Checkbutton, BooleanVar, messagebox


def check_password_strength(password):
    strength_criteria = {
        "length": len(password) >= 8,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digits": bool(re.search(r"\d", password)),
        "special": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    }
    
    strength_score = sum(strength_criteria.values())
    strength = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
    
    character_set_size = 0
    if strength_criteria["uppercase"]:
        character_set_size += 26
    if strength_criteria["lowercase"]:
        character_set_size += 26
    if strength_criteria["digits"]:
        character_set_size += 10
    if strength_criteria["special"]:
        character_set_size += 32  
    
    combinations = character_set_size ** len(password)
    attempts_per_second = 1e10  # Assume 10 billion attempts per second
    time_to_crack_seconds = combinations / attempts_per_second
    
    seconds_per_year = 60 * 60 * 24 * 365.25
    time_to_crack_years = time_to_crack_seconds / seconds_per_year
    
    feedback = f"Password strength: {strength[max(0, strength_score - 1)]}"
    feedback += f"\nEstimated time to crack: {time_to_crack_years:.2e} years"
    
    missing_criteria = [key for key, value in strength_criteria.items() if not value]
    if missing_criteria:
        feedback += "\nConsider adding the following to improve strength: " + ", ".join(missing_criteria)
    
    return feedback


def toggle_password_visibility():
    """Toggle between showing and hiding the password."""
    if show_password_var.get():
        entry.config(show="")
    else:
        entry.config(show="*")


def on_check_button_click():
    password = entry.get()
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password to check.")
        return
    
    feedback = check_password_strength(password)
    result_label.config(text=feedback, justify="left")


root = Tk()
root.title("Password Strength Checker")
root.geometry("500x400")
root.resizable(False, False)


banner_label = Label(root, text="PASSWORD STRENGTH CHECKER", font=("Helvetica", 16, "bold"), fg="green")
banner_label.pack(pady=10)


entry_label = Label(root, text="Enter Password:", font=("Helvetica", 12))
entry_label.pack(pady=5)

entry = Entry(root, width=40, show="*", font=("Helvetica", 12))
entry.pack(pady=5)


show_password_var = BooleanVar()
show_password_check = Checkbutton(
    root,
    text="Show Password",
    variable=show_password_var,
    command=toggle_password_visibility,
    font=("Helvetica", 10)
)
show_password_check.pack(pady=5)


check_button = Button(root, text="Check Strength", command=on_check_button_click, font=("Helvetica", 12), bg="blue", fg="white")
check_button.pack(pady=10)


result_label = Label(root, text="", font=("Helvetica", 12), fg="dark blue", wraplength=450)
result_label.pack(pady=10)


root.mainloop()

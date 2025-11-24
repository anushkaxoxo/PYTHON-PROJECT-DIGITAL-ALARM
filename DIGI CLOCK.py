import tkinter as tk
from tkinter import messagebox
from time import strftime
import winsound
import threading

class DigitalClockAlarm:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Clock with Alarm")
        self.root.geometry("450x350")
        self.root.resizable(False, False)
        self.root.configure(bg='black')
        
        self.alarm_time = None
        self.alarm_active = False
        
        # Time display
        self.time_label = tk.Label(
            root,
            font=('Arial', 48, 'bold'),
            background='black',
            foreground='cyan'
        )
        self.time_label.pack(pady=10)
        
        # Date display
        self.date_label = tk.Label(
            root,
            font=('Arial', 14),
            background='black',
            foreground='white'
        )
        self.date_label.pack()
        
        # Alarm section
        alarm_frame = tk.Frame(root, bg='black')
        alarm_frame.pack(pady=20)
        
        tk.Label(
            alarm_frame,
            text="Set Alarm (HH:MM:SS):",
            font=('Arial', 12),
            bg='black',
            fg='white'
        ).grid(row=0, column=0, columnspan=3, pady=5)
        
        # Hour input
        self.hour_var = tk.StringVar(value="00")
        self.hour_entry = tk.Entry(
            alarm_frame,
            textvariable=self.hour_var,
            width=5,
            font=('Arial', 16),
            justify='center'
        )
        self.hour_entry.grid(row=1, column=0, padx=2)
        
        tk.Label(alarm_frame, text=":", font=('Arial', 16), bg='black', fg='white').grid(row=1, column=1)
        
        # Minute input
        self.minute_var = tk.StringVar(value="00")
        self.minute_entry = tk.Entry(
            alarm_frame,
            textvariable=self.minute_var,
            width=5,
            font=('Arial', 16),
            justify='center'
        )
        self.minute_entry.grid(row=1, column=2, padx=2)
        
        tk.Label(alarm_frame, text=":", font=('Arial', 16), bg='black', fg='white').grid(row=1, column=3)
        
        # Second input
        self.second_var = tk.StringVar(value="00")
        self.second_entry = tk.Entry(
            alarm_frame,
            textvariable=self.second_var,
            width=5,
            font=('Arial', 16),
            justify='center'
        )
        self.second_entry.grid(row=1, column=4, padx=2)
        
        # Buttons
        button_frame = tk.Frame(root, bg='black')
        button_frame.pack(pady=10)
        
        self.set_button = tk.Button(
            button_frame,
            text="Set Alarm",
            font=('Arial', 12),
            bg='green',
            fg='white',
            command=self.set_alarm,
            width=12
        )
        self.set_button.grid(row=0, column=0, padx=5)
        
        self.cancel_button = tk.Button(
            button_frame,
            text="Cancel Alarm",
            font=('Arial', 12),
            bg='red',
            fg='white',
            command=self.cancel_alarm,
            width=12,
            state='disabled'
        )
        self.cancel_button.grid(row=0, column=1, padx=5)
        
        # Alarm status
        self.status_label = tk.Label(
            root,
            text="No alarm set",
            font=('Arial', 11),
            bg='black',
            fg='yellow'
        )
        self.status_label.pack(pady=5)
        
        # Start clock
        self.update_time()
    
    def update_time(self):
        time_string = strftime('%H:%M:%S')
        date_string = strftime('%A, %B %d, %Y')
        
        self.time_label.config(text=time_string)
        self.date_label.config(text=date_string)
        
        # Check alarm
        if self.alarm_active and time_string == self.alarm_time:
            self.trigger_alarm()
        
        self.time_label.after(1000, self.update_time)
    
    def set_alarm(self):
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            second = int(self.second_var.get())
            
            if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
                messagebox.showerror("Invalid Time", "Please enter valid time values!")
                return
            
            self.alarm_time = f"{hour:02d}:{minute:02d}:{second:02d}"
            self.alarm_active = True
            
            self.status_label.config(text=f"Alarm set for: {self.alarm_time}", fg='lime')
            self.set_button.config(state='disabled')
            self.cancel_button.config(state='normal')
            
            messagebox.showinfo("Alarm Set", f"Alarm set for {self.alarm_time}")
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter numeric values!")
    
    def cancel_alarm(self):
        self.alarm_active = False
        self.alarm_time = None
        
        self.status_label.config(text="No alarm set", fg='yellow')
        self.set_button.config(state='normal')
        self.cancel_button.config(state='disabled')
        
        messagebox.showinfo("Alarm Cancelled", "Alarm has been cancelled")
    
    def trigger_alarm(self):
        self.alarm_active = False
        
        def play_sound():
            try:
                # Play system beep sound (works on Windows)
                for _ in range(5):
                    winsound.Beep(1000, 500)
            except:
                # Fallback for other systems
                print('\a' * 5)
        
        # Play sound in separate thread
        threading.Thread(target=play_sound, daemon=True).start()
        
        messagebox.showwarning("ALARM!", f"Alarm ringing!\nTime: {self.alarm_time}")
        
        self.status_label.config(text="Alarm triggered!", fg='red')
        self.set_button.config(state='normal')
        self.cancel_button.config(state='disabled')

# Create and run application
root = tk.Tk()
app = DigitalClockAlarm(root)
root.mainloop()
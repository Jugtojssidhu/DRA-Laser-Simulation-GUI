import customtkinter as ctk
from tkinter import filedialog

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light") 
        ctk.set_default_color_theme("blue")
        self.delayed_write_schedules = {}
        self.setup_ui()

    def setup_ui(self):
        # Window Config
        self.title("GUI DRA")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        
        # Sections
        self.create_laser_properties_section()
        self.create_material_properties_section()
        self.create_appearance_mode_toggle()
        self.create_simulation_length_section()
        self.create_submit_button()
        self.create_file_selection_section()
    
    def delayed_write(self, key, value):
        delay = 1000  # Delay in milliseconds
        if key in self.delayed_write_schedules:
            self.after_cancel(self.delayed_write_schedules[key])
        self.delayed_write_schedules[key] = self.after(delay, lambda: self.write_to_file("simulation_data.txt", f"{key}; {value}"))

    def setup_variable_trace(self, var, key):
        callback = lambda *args: self.delayed_write(key, var.get())
        var.trace_add("write", callback)

    def create_appearance_mode_toggle(self):
        section_label = ctk.CTkLabel(self, text="Appearance Mode", font=("Arial", 16, 'bold'))
        section_label.grid(row=19, column=0, columnspan=2, pady=(20, 5))
        self.mode_switch = ctk.CTkSwitch(self, text="Dark Mode", command=self.toggle_appearance_mode)
        self.mode_switch.grid(row=20, column=0, columnspan=2, pady=(5, 20))

    def toggle_appearance_mode(self):
        if self.mode_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def create_laser_properties_section(self):
        section_label = ctk.CTkLabel(self, text="Laser Properties", font=("Arial", 16, 'bold'))
        section_label.grid(row=0, column=0, columnspan=2, pady=(5, 5)) 

        self.create_laser_wavelength_entry(row=1)
        self.create_laser_power_entry(row=2)
        self.create_laser_position_entries(row=3)

    def create_material_properties_section(self):
        section_label = ctk.CTkLabel(self, text="Material Properties", font=("Arial", 16, 'bold'))
        section_label.grid(row=7, column=0, columnspan=2, pady=(5, 5))
        self.create_material_combobox(row=8)
        self.create_material_dimension_entries(row=9)

    def create_material_combobox(self, row):
        label = ctk.CTkLabel(self, text="Material")
        label.grid(row=row, column=0, padx=(40,20), pady=10)
        combobox = ctk.CTkComboBox(self, values=["Pick one", "copper", "titanium", "aluminium", "etc"], command=self.callback_material)
        combobox.grid(row=row, column=1, padx=(20,40), pady=10)

    def create_material_dimension_entries(self, row):
        labels = ["Length", "Width", "Depth"]
        self.material_dimensions_vars = []

        for i, label_text in enumerate(labels, start=row):
            label = ctk.CTkLabel(self, text=label_text)
            label.grid(row=i, column=0, padx=(40,20), pady=10)
            var = ctk.StringVar()
            self.setup_variable_trace(var, f"Material {label_text}")
            entry = ctk.CTkEntry(self, textvariable=var, placeholder_text=f"Enter {label_text}")
            entry.grid(row=i, column=1, padx=(20,40), pady=10)
            self.material_dimensions_vars.append(var)

    def create_laser_wavelength_entry(self, row):
        label = ctk.CTkLabel(self, text="Wavelength")
        label.grid(row=row, column=0, padx=(40,20), pady=10)
        self.entry_size_var = ctk.StringVar()
        self.setup_variable_trace(self.entry_size_var, "Laser Wavelength")
        entry = ctk.CTkEntry(self, textvariable=self.entry_size_var, placeholder_text="Enter Wavelength")
        entry.grid(row=row, column=1, padx=(20,40), pady=10)

    def create_laser_power_entry(self, row):
        label = ctk.CTkLabel(self, text="Power")
        label.grid(row=row+1, column=0, padx=(40,20), pady=10)
        self.entry_power_var = ctk.StringVar()
        self.setup_variable_trace(self.entry_power_var, "Laser Power")
        entry = ctk.CTkEntry(self, textvariable=self.entry_power_var, placeholder_text="Enter Power")
        entry.grid(row=row+1, column=1, padx=(20,40), pady=10)

    def create_laser_position_entries(self, row):
        labels = ["Position X", "Position Y"]
        self.laser_position_vars = [ctk.StringVar(), ctk.StringVar()]

        for i, label_text in enumerate(labels, start=row):
            label = ctk.CTkLabel(self, text=label_text)
            label.grid(row=i+2, column=0, padx=(40,20), pady=10)
            var = ctk.StringVar()
            self.setup_variable_trace(var, f"Laser {label_text}")
            entry = ctk.CTkEntry(self, textvariable=var, placeholder_text=f"Enter {label_text}")
            entry.grid(row=i+2, column=1, padx=(20,40), pady=10)
            self.laser_position_vars.append(var)

    def create_simulation_length_section(self):
        section_label = ctk.CTkLabel(self, text="Length of Simulation", font=("Arial", 16, 'bold'))
        section_label.grid(row=13, column=0, columnspan=2, pady=(20, 5))
        self.create_simulation_time_entry(row=14)

    def create_simulation_time_entry(self, row):
        label = ctk.CTkLabel(self, text="Time (seconds)")
        label.grid(row=row, column=0, padx=(40, 20), pady=10)
        self.entry_simulation_time_var = ctk.StringVar()
        self.setup_variable_trace(self.entry_simulation_time_var, "Simulation Time")
        entry = ctk.CTkEntry(self, textvariable=self.entry_simulation_time_var, placeholder_text="Enter Time")
        entry.grid(row=row, column=1, padx=(20, 40), pady=10)

    def write_to_file(self, filename, content):
        mode = 'a' if hasattr(self, 'file_initialized') else 'w'
        with open(filename, mode) as file:
            file.write(content + "\n")
        self.file_initialized = True  # Mark file as initialized after first write
    
    def callback_material(self, choice):
        self.write_to_file("simulation_data.txt", f"Material selected; {choice}")
    
    def create_submit_button(self):
        instruction_label = ctk.CTkLabel(self, text="Once all data is inputted and video selected, press Submit", font=("Arial", 12))
        instruction_label.grid(row=17, column=0, columnspan=2, pady=(10, 0)) 
        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.on_submit)
        self.submit_button.grid(row=18, column=0, columnspan=2, pady=(0, 0))

    def on_submit(self):
        self.destroy()

    def create_file_selection_section(self):
        section_label = ctk.CTkLabel(self, text="Select a File", font=("Arial", 16, 'bold'))
        section_label.grid(row=15, column=0, columnspan=2, pady=(10, 5))  
        self.file_path_var = ctk.StringVar()
        file_select_button = ctk.CTkButton(self, text="Browse", command=self.select_file)
        file_select_button.grid(row=16, column=0, columnspan=2, pady=(0, 30))  

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a video",
            filetypes=(
                ("MP4 files", "*.mp4"),
                ("AVI files", "*.avi"),
                ("MOV files", "*.mov"),
                ("All files", "*.*")
            )
        )
        if file_path:
            self.file_path_var.set(file_path)
            self.write_to_file("simulation_data.txt", f"Video selected; {file_path}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
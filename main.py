import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv

class FileEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("File Editor")
        
        # Initialize selected_courses list
        self.selected_courses = []
        
        # Set background color and padding
        bg_color = '#333333'  # Dark gray background
        fg_color = '#FFFFFF'  # White text
        input_bg = '#F3F4F6'  # Light gray (bg-gray-100 equivalent)
        
        # Create main container with padding
        main_container = tk.Frame(root, bg=bg_color, padx=20, pady=20)
        main_container.pack(fill='both', expand=True)
        
        # Center container for content
        center_container = tk.Frame(main_container, bg=bg_color)
        center_container.pack(fill='both', expand=True, padx=50)
        
        # File path frame
        file_frame = tk.Frame(center_container, bg=bg_color)
        file_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(file_frame, text="Enter the file path:", bg=bg_color, fg=fg_color).pack(side='left')
        self.file_path = tk.Entry(file_frame, width=40, bg=input_bg)
        self.file_path.pack(side='left', padx=5)
        tk.Button(file_frame, text="Browse", command=self.browse_file).pack(side='left')
        
        # Year and Department frame
        input_frame = tk.Frame(center_container, bg=bg_color)
        input_frame.pack(fill='x', pady=10)
        
        tk.Label(input_frame, text="Year:", bg=bg_color, fg=fg_color).pack(side='left')
        self.year = ttk.Combobox(input_frame, width=5, state='readonly', background=input_bg)
        self.year['values'] = ['All', '1', '2', '3', '4', '5']
        self.year.set('All')
        self.year.pack(side='left', padx=5)
        
        tk.Label(input_frame, text="Department:", bg=bg_color, fg=fg_color).pack(side='left')
        self.dept_entry = ttk.Combobox(input_frame, width=27, state='readonly', background=input_bg)
        self.dept_entry.pack(side='left', padx=5)
        
        # Buttons frame
        button_frame = tk.Frame(center_container, bg=bg_color)
        button_frame.pack(fill='x', pady=10)
        
        # Center the buttons
        button_container = tk.Frame(button_frame, bg=bg_color)
        button_container.pack(expand=True)
        tk.Button(button_container, text="Display", command=self.display_courses).pack(side='left', padx=5)
        tk.Button(button_container, text="Clear", command=self.clear_fields).pack(side='left', padx=5)
        tk.Button(button_container, text="Save", command=self.save_timetable).pack(side='left', padx=5)
        tk.Button(button_container, text="View my schedule", 
                 command=self.open_schedule_viewer).pack(side='left', padx=5)
        
        # Warning and Course labels
        warning_course_frame = tk.Frame(center_container, bg=bg_color)
        warning_course_frame.pack(fill='x', pady=10)
        
        tk.Label(warning_course_frame, text="Warnings:", bg=bg_color, fg=fg_color).pack(side='left')
        tk.Label(warning_course_frame, text="Courses:", bg=bg_color, fg=fg_color).pack(side='right')
        
        # Text areas frame
        text_frame = tk.Frame(center_container, bg=bg_color)
        text_frame.pack(fill='both', expand=True, pady=10)
        
        # Warning text area
        self.warnings = tk.Text(text_frame, height=10, width=40, bg=input_bg)
        self.warnings.pack(side='left', padx=5)
        
        # Courses listbox
        self.courses = tk.Listbox(text_frame, height=10, width=40, bg=input_bg)
        self.courses.bind('<<ListboxSelect>>', self.on_select_course)
        self.courses.pack(side='left', padx=5)
        
        # Selected courses frame
        selected_frame = tk.Frame(center_container, bg=bg_color)
        selected_frame.pack(fill='x', pady=10)
        
        tk.Label(selected_frame, text="Selected Courses:", bg=bg_color, fg=fg_color).pack(side='left')
        self.selected_listbox = tk.Listbox(selected_frame, height=6, width=50, bg=input_bg)
        self.selected_listbox.pack(expand=True, padx=5)

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select a CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.delete(0, tk.END)
            self.file_path.insert(0, filename)
            self.update_departments()  # Update department list when file is selected
            
    def update_departments(self):
        try:
            departments = set()
            filepath = self.file_path.get()
            
            with open(filepath, 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if row:  # Skip empty rows
                        course_code = row[0].strip()
                        dept = course_code.split()[0]  # Get department code
                        departments.add(dept)
            
            # Sort departments alphabetically and add "All" option
            sorted_departments = ['All'] + sorted(list(departments))
            
            # Update the combobox values
            self.dept_entry['values'] = sorted_departments
            
            # Set default selection to "All"
            self.dept_entry.set('All')
                
        except Exception as e:
            self.warnings.delete(1.0, tk.END)
            self.warnings.insert(tk.END, f"Error loading departments: {str(e)}")

    def on_select_course(self, event):
        if not self.courses.curselection():
            return
            
        selected_index = self.courses.curselection()[0]
        selected_course = self.courses.get(selected_index)
        
        # Check if course is already selected
        if selected_course in self.selected_courses:
            self.warnings.delete(1.0, tk.END)
            self.warnings.insert(tk.END, "Course already selected!")
            return
            
        # Check if already 6 courses are selected
        if len(self.selected_courses) >= 6:
            self.warnings.delete(1.0, tk.END)
            self.warnings.insert(tk.END, "Cannot select more than 6 courses!")
            return
            
        # Add course to selected courses
        self.selected_courses.append(selected_course)
        self.selected_listbox.insert(tk.END, selected_course)
        
        # Clear any previous warnings
        self.warnings.delete(1.0, tk.END)

    def display_courses(self):
        try:
            filepath = self.file_path.get()
            department = self.dept_entry.get()
            year = self.year.get()
            
            if not filepath:
                self.warnings.delete(1.0, tk.END)
                self.warnings.insert(tk.END, "Please select a file")
                return
            
            # Clear previous content
            self.courses.delete(0, tk.END)  # Changed from 1.0 to 0
            self.warnings.delete(1.0, tk.END)
            
            matching_courses = []
            
            with open(filepath, 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if not row or len(row) < 4:  # Skip empty rows or invalid entries
                        continue
                    
                    course_code = row[0].strip()
                    course_name = row[1].strip()
                    days = row[2].strip() if row[2].strip() else "N/A"
                    hours = row[3].strip() if row[3].strip() else "N/A"
                    
                    # Split course code into department and number
                    parts = course_code.split()
                    if len(parts) != 2:
                        continue
                        
                    dept, number = parts
                    
                    # Apply filters based on what's selected
                    matches_department = True if department == 'All' else dept == department
                    matches_year = True if year == 'All' else number[0] == year
                    
                    if matches_department and matches_year:
                        course_info = f"{course_code}: {course_name}\n   Schedule: {days} {hours}"
                        self.courses.insert(tk.END, course_info)  # Add directly to listbox
            
            if self.courses.size() == 0:
                filter_desc = []
                if department != 'All':
                    filter_desc.append(f"department '{department}'")
                if year != 'All':
                    filter_desc.append(f"year {year}")
                
                filter_text = " and ".join(filter_desc) if filter_desc else "no filters"
                self.warnings.insert(tk.END, f"No courses found for {filter_text}")
                
        except FileNotFoundError:
            self.warnings.insert(tk.END, "File not found. Please select a valid CSV file.")
        except Exception as e:
            self.warnings.insert(tk.END, f"Error: {str(e)}")

    def clear_fields(self):
        self.dept_entry.set('All')  # Use set() for Combobox
        self.year.set('All')  # Use set() for Combobox
        self.warnings.delete(1.0, tk.END)  # Text widget uses 1.0
        self.courses.delete(0, tk.END)  # Listbox uses 0
        self.selected_listbox.delete(0, tk.END)  # Clear selected courses
        self.selected_courses = []  # Reset selected courses list

    def save_timetable(self):
        try:
            if not self.selected_courses:
                self.warnings.delete(1.0, tk.END)
                self.warnings.insert(tk.END, "No courses selected to save!")
                return

            with open("timetable.csv", "w", newline='') as file:
                writer = csv.writer(file)
                # Write header
                writer.writerow(["Course Code", "Course Name", "Days", "Hours"])
                
                for course in self.selected_courses:
                    # Parse the course string to extract information
                    # Format is "CODE: Name\n   Schedule: Days Hours"
                    course_parts = course.split("\n")
                    
                    # Split the first part into code and name
                    code_name = course_parts[0].split(": ", 1)
                    code = code_name[0]
                    name = code_name[1]
                    
                    # Get schedule information
                    schedule = course_parts[1].replace("   Schedule: ", "").split(" ", 1)
                    days = schedule[0] if len(schedule) > 0 else "N/A"
                    hours = schedule[1] if len(schedule) > 1 else "N/A"
                    
                    # Write to CSV
                    writer.writerow([code, name, days, hours])
            
            self.warnings.delete(1.0, tk.END)
            self.warnings.insert(tk.END, "Timetable saved successfully!")
            
        except Exception as e:
            self.warnings.delete(1.0, tk.END)
            self.warnings.insert(tk.END, f"Error saving timetable: {str(e)}")

    def open_schedule_viewer(self):
        # Create modal window
        self.schedule_window = tk.Toplevel(self.root)
        self.schedule_window.title("Schedule Viewer")
        self.schedule_window.configure(bg='#333333')
        
        # Make it modal
        self.schedule_window.transient(self.root)
        self.schedule_window.grab_set()
        
        # Center the window
        window_width = 800
        window_height = 600
        screen_width = self.schedule_window.winfo_screenwidth()
        screen_height = self.schedule_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.schedule_window.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Create main container
        main_container = tk.Frame(self.schedule_window, bg='#333333', padx=20, pady=20)
        main_container.pack(fill='both', expand=True)
        
        # File selection frame
        file_frame = tk.Frame(main_container, bg='#333333')
        file_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(file_frame, text="Select timesheet:", 
                bg='#333333', fg='#FFFFFF').pack(side='left')
        self.timesheet_path = tk.Entry(file_frame, width=40, bg='#F3F4F6')
        self.timesheet_path.pack(side='left', padx=5)
        tk.Button(file_frame, text="Browse", 
                 command=self.browse_timesheet).pack(side='left')
        
        # Schedule display frame
        self.schedule_frame = tk.Frame(main_container, bg='#333333')
        self.schedule_frame.pack(fill='both', expand=True)
        
        # Create schedule grid
        self.create_schedule_grid()

    def browse_timesheet(self):
        filename = filedialog.askopenfilename(
            title="Select timesheet file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.timesheet_path.delete(0, tk.END)
            self.timesheet_path.insert(0, filename)
            self.load_schedule()

    def create_schedule_grid(self):
        # Clear existing schedule
        for widget in self.schedule_frame.winfo_children():
            widget.destroy()
            
        # Time slots (9 AM to 8 PM)
        times = [f"{h:02d}:00" for h in range(9, 21)]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        
        # Configure grid
        for i in range(len(times) + 1):  # +1 for header row
            self.schedule_frame.grid_rowconfigure(i, weight=1)
        for i in range(len(days) + 1):  # +1 for time column
            self.schedule_frame.grid_columnconfigure(i, weight=1)
        
        # Create headers
        tk.Label(self.schedule_frame, width=8, bg='#333333', 
                fg='#FFFFFF').grid(row=0, column=0)
        
        # Add day headers
        for i, day in enumerate(days):
            tk.Label(self.schedule_frame, text=day, bg='#333333', 
                    fg='#FFFFFF', padx=10).grid(row=0, column=i+1)
        
        # Add time slots and create grid cells
        for i, time in enumerate(times):
            tk.Label(self.schedule_frame, text=time, bg='#333333', 
                    fg='#FFFFFF').grid(row=i+1, column=0)
            
            # Create empty cells
            for j in range(len(days)):
                frame = tk.Frame(self.schedule_frame, bg='#F3F4F6', 
                               width=120, height=30)
                frame.grid(row=i+1, column=j+1, padx=2, pady=1, sticky='nsew')
                frame.grid_propagate(False)

    def load_schedule(self):
        try:
            with open(self.timesheet_path.get(), 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                
                # Clear existing schedule
                self.create_schedule_grid()
                
                # Process each course
                for row in reader:
                    if len(row) >= 4:  # Ensure row has enough columns
                        code, name, days_str, times_str = row
                        if days_str and times_str:  # Skip empty schedules
                            self.add_course_to_grid(code, name, days_str, times_str)
                            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading schedule: {str(e)}")

    def add_course_to_grid(self, code, name, days_str, times_str):
        # Map full day names to column numbers (1-based as column 0 is for times)
        days_map = {
            'Monday': 1,
            'Tuesday': 2,
            'Wednesday': 3,
            'Thursday': 4,
            'Friday': 5
        }
        
        # Split days and times
        days = days_str.split()
        times = times_str.split()
        
        for day in days:
            if day not in days_map:
                continue
                
            col = days_map[day]
            
            # Process each time slot
            for time_slot in times:
                if '-' not in time_slot:
                    continue
                    
                start_time, end_time = time_slot.split('-')
                
                # Convert times to grid rows (9:00 = row 1, 10:00 = row 2, etc.)
                try:
                    start_hour = int(start_time.split(':')[0])
                    end_hour = int(end_time.split(':')[0])
                    start_minute = int(start_time.split(':')[1])
                    end_minute = int(end_time.split(':')[1])
                    
                    # Calculate row positions (grid starts at 9:00)
                    row_start = (start_hour - 9) + 1  # +1 because row 0 is header
                    row_end = (end_hour - 9) + 1
                    
                    if end_minute > 0:
                        row_end += 1
                    
                    # Create course block
                    if row_start >= 1 and row_end <= 12:  # Ensure within grid bounds
                        course_frame = tk.Frame(self.schedule_frame, bg='#4F46E5')
                        course_frame.grid(row=row_start, column=col, 
                                        rowspan=row_end-row_start,
                                        padx=2, pady=1, sticky='nsew')
                        
                        # Add course information
                        label_text = f"{code}\n{name}"
                        tk.Label(course_frame, text=label_text,
                                bg='#4F46E5', fg='#FFFFFF',
                                wraplength=100, font=('Arial', 8)).pack(expand=True)
                        
                except ValueError as e:
                    print(f"Error processing time for {code}: {e}")
                    continue

if __name__ == "__main__":
    root = tk.Tk()
    app = FileEditor(root)
    root.mainloop()
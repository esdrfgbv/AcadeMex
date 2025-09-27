import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from PIL import Image, ImageTk
import os

# Updated Color Scheme
BG_COLOR = "#1D6F6F"  # Teal background color
FRAME_COLOR = "#FFFFFF"  # White for frames
BUTTON_COLOR = "#000000"  # Black for buttons
ACCENT_COLOR = "#000000"  # Black for accents
TEXT_COLOR = "#37474F"  # Dark blue-gray for text
HIGHLIGHT_COLOR = "#42A5F5"  # Bright blue for highlights
SECONDARY_COLOR = "#66BB8A"  # Bright green for secondary elements
WARNING_COLOR = "#EF5350"  # Bright red for warnings
BUTTON_TEXT_COLOR = "#FFFFFF"  # White text for buttons
ENTRY_BG_COLOR = "#a58255"  # Light cyan color for entry fields

# Path to the logo file - update this to your logo path
LOGO_PATH = "gitam-logo-new.png"  # Replace with your actual logo file name

# Paths for the calculator button images - update these to your image paths
GRADE_CALC_IMG_PATH = "Grade.png"  # Replace with your grade calculator image
GPA_CALC_IMG_PATH = "GPA.png"  # Replace with your GPA calculator image

def absolute_grading(subject_entry, name_entry, marks_entry, result_text):
    try:
        subject = subject_entry.get()
        names = name_entry.get().split()
        marks = list(map(int, marks_entry.get().split()))
        if len(names) != len(marks):
            messagebox.showerror("Input Error", "Number of students and marks should be the same")
            return
        max_marks = simpledialog.askinteger("Input", "Enter Maximum Marks:")
        result_text.insert(tk.END, f"{subject}\n")
        for i in range(len(names)):
            p = (marks[i] / max_marks) * 100
            if p >= 90:
                grade = "O"
            elif p >= 80:
                grade = "A+"
            elif p >= 70:
                grade = "A"
            elif p >= 60:
                grade = "B+"
            elif p >= 50:
                grade = "B"
            elif p >= 45:
                grade = "C"
            elif p >= 40:
                grade = "P"
            else:
                grade = "F"
            result_text.insert(tk.END, f"{names[i]:<10}: {grade}\n")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for marks")

def relative_grading(subject_entry, name_entry, marks_entry, result_text):
    try:
        subject = subject_entry.get()
        names = name_entry.get().split()
        marks = list(map(int, marks_entry.get().split()))
        if len(names) != len(marks):
            messagebox.showerror("Input Error", "Number of students and marks should be the same")
            return
        mean = sum(marks) / len(marks)
        variance = sum((x - mean) ** 2 for x in marks) / len(marks)
        std_dev = variance ** 0.5
        max_marks = max(marks)
        result_text.insert(tk.END, f"{subject}\n")
        for i in range(len(names)):
            if marks[i] == max_marks or marks[i] >= mean + 1.5 * std_dev:
                grade = "O"
            elif marks[i] >= mean + std_dev:
                grade = "A+"
            elif marks[i] >= mean + 0.5 * std_dev:
                grade = "A"
            elif marks[i] >= mean - 0.5 * std_dev:
                grade = "B+"
            elif marks[i] >= mean - std_dev:
                grade = "B"
            elif marks[i] >= mean - 1.5 * std_dev:
                grade = "C"
            else:
                grade = "F"
            result_text.insert(tk.END, f"{names[i]:<10}: {grade}\n")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for marks")

def calculate_gpa(grades_entry, credits_entry, result_label):
    try:
        grades = grades_entry.get().split(' ')
        credits = list(map(float, credits_entry.get().split(' ')))
        grade_points = {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'P': 4, 'F': 0}
        total_points = sum(grade_points.get(g.strip(), 0) * c for g, c in zip(grades, credits))
        total_credits = sum(credits)
        gpa = total_points / total_credits if total_credits > 0 else 0
        result_label.config(text=f"GPA: {gpa:.2f}")
    except ValueError:
        result_label.config(text="Please enter valid grades and credit values.")
    except Exception as e:
        result_label.config(text=f"An unexpected error occurred: {e}")

def add_student():
    frame = tk.Frame(sub_frame, bg=FRAME_COLOR, bd=2, relief=tk.GROOVE)
    frame.pack(side=tk.TOP, pady=5, padx=5, fill=tk.X)
    font_style = ("Arial", 12)
    tk.Label(frame, text="Student Name:", font=font_style, bg=FRAME_COLOR, fg=TEXT_COLOR).pack(fill=tk.X)
    student_entry = tk.Entry(frame, font=font_style, bg="#f0e0c1", fg=TEXT_COLOR)
    student_entry.pack(fill=tk.X, expand=True)
    tk.Label(frame, text="Grades (comma-separated):", font=font_style, bg=FRAME_COLOR, fg=TEXT_COLOR).pack(fill=tk.X)
    grades_entry = tk.Entry(frame, font=font_style, bg="#f0e0c1", fg=TEXT_COLOR)
    grades_entry.pack(fill=tk.X, expand=True)
    tk.Label(frame, text="Credits (comma-separated):", font=font_style, bg=FRAME_COLOR, fg=TEXT_COLOR).pack(fill=tk.X)
    credits_entry = tk.Entry(frame, font=font_style, bg="#f0e0c1", fg=TEXT_COLOR)
    credits_entry.pack(fill=tk.X, expand=True)
    result_label = tk.Label(frame, font=font_style, bg="#f0e0c1", fg=TEXT_COLOR)
    result_label.pack(pady=10)
    calculate_button = tk.Button(frame, text="Calculate GPA", command=lambda: calculate_gpa(grades_entry, credits_entry, result_label), font=("Arial", 14, "bold"), bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, activebackground=HIGHLIGHT_COLOR, activeforeground="white")
    calculate_button.pack(pady=5)
    
    # We keep the add_button visibility management here
    if add_button:
        add_button.pack_forget()
        add_button.pack(pady=5)
    
    sub_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

# Define global variables
subject_count = 0
add_button = None
student_count = 0

def add_subject():
    global subject_count, add_button
    subject_count += 1
    frame = tk.Frame(sub_frame, bg=FRAME_COLOR, bd=2, relief=tk.GROOVE)
    frame.pack(side=tk.TOP, pady=5, padx=5, fill=tk.X)
    font_style = ("Arial", 12)
    subject_label = tk.Label(frame, text=f"Subject {subject_count}", font=("Arial", 14, "bold"), bg=FRAME_COLOR, fg=TEXT_COLOR)
    subject_label.pack(anchor="w")
    tk.Label(frame, text="Subject Name:", font=font_style, bg=FRAME_COLOR, fg=TEXT_COLOR).pack(fill=tk.X)
    subject_entry = tk.Entry(frame, font=font_style, bg="#f0e0c1", fg=TEXT_COLOR)
    subject_entry.pack(fill=tk.X, expand=True)
    tk.Label(frame, text="Student Names (space-separated):", font=font_style, bg=FRAME_COLOR, fg=TEXT_COLOR).pack(fill=tk.X)
    name_entry = tk.Entry(frame, font=font_style, bg="#f0e0c1", fg=TEXT_COLOR)
    name_entry.pack(fill=tk.X, expand=True)
    tk.Label(frame, text="Marks (space-separated):", font=font_style, bg=FRAME_COLOR, fg=TEXT_COLOR).pack(fill=tk.X)
    marks_entry = tk.Entry(frame, font=font_style, bg="#f0e0c1", fg=TEXT_COLOR)
    marks_entry.pack(fill=tk.X, expand=True)
    result_text = scrolledtext.ScrolledText(frame, height=6, font=font_style, bg="#f0e0c1", fg=TEXT_COLOR)
    result_text.pack(fill=tk.BOTH, expand=True)
    button_frame = tk.Frame(frame, bg=FRAME_COLOR, height=2, relief=tk.GROOVE)
    button_frame.pack(fill=tk.X)
    tk.Radiobutton(button_frame, text="Absolute Grading", command=lambda: absolute_grading(subject_entry, name_entry, marks_entry, result_text), font=font_style, bg=HIGHLIGHT_COLOR, fg="white").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, pady=2)
    tk.Radiobutton(button_frame, text="Relative Grading", command=lambda: relative_grading(subject_entry, name_entry, marks_entry, result_text), font=font_style, bg=HIGHLIGHT_COLOR, fg="white").pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5, pady=2)
    def update_subject_label(*args):
        subject_label.config(text=subject_entry.get())
    subject_entry.bind("<KeyRelease>", update_subject_label)
    
    # Remove previous add button if it exists
    if add_button:
        add_button.pack_forget()
    
    # Create new add button
    add_button = tk.Button(frame, text="Add Subject", command=add_subject, font=("Arial", 14, "bold"), bg=ACCENT_COLOR, fg="white", activebackground=HIGHLIGHT_COLOR, activeforeground="white")
    add_button.pack(pady=5)
    
    sub_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_canvas_configure(event):
    canvas.itemconfig(window, width=event.width)

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def create_footer(visible=True):
    global footer_frame
    
    # If there's an existing footer frame, destroy it first
    if 'footer_frame' in globals() and footer_frame is not None:
        footer_frame.destroy()
    
    if visible:
        footer_frame = tk.Frame(root, bg=BG_COLOR, height=70)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Make sure it stays at the bottom
        footer_frame.pack_propagate(False)
        
        # Create centered text in the footer
        school_label = tk.Label(
            footer_frame, 
            text="Gitam School of Technology", 
            font=("Arial", 16, "bold"), 
            fg="#f3e5cb", 
            bg=BG_COLOR
        )
        school_label.pack(anchor="center")
        
        dept_label = tk.Label(
            footer_frame, 
            text="Computer Science Department", 
            font=("Arial", 16, "bold"), 
            fg="#f3e5cb", 
            bg=BG_COLOR
        )
        dept_label.pack(anchor="center")
    else:
        footer_frame = None

def show_grade_calculator():
    global subject_count, add_button
    
    # Reset the counter when entering this view
    subject_count = 0
    add_button = None
    
    # Clear the sub_frame
    for widget in sub_frame.winfo_children():
        widget.destroy()
    
    # Hide the footer
    create_footer(visible=False)
    
    # Add a back arrow at the top left corner
    back_arrow = tk.Label(sub_frame, text="←", font=("Arial", 20, "bold"), bg=BG_COLOR, fg="#f0e0c1", cursor="hand2")
    back_arrow.pack(anchor="nw", padx=10, pady=10)
    back_arrow.bind("<Button-1>", lambda e: reset_view())
    
    # Add the first subject
    add_subject()

def show_gpa_calculator():
    global add_button, student_count
    
    # Reset the counter when entering this view
    student_count = 0
    add_button = None
    
    # Clear the sub_frame
    for widget in sub_frame.winfo_children():
        widget.destroy()
    
    # Hide the footer
    create_footer(visible=False)
    
    # Add a back arrow at the top left corner
    back_arrow = tk.Label(sub_frame, text="←", font=("Arial", 20, "bold"), bg=BG_COLOR, fg="#f0e0c1", cursor="hand2")
    back_arrow.pack(anchor="nw", padx=10, pady=10)
    back_arrow.bind("<Button-1>", lambda e: reset_view())
    
    font_style = ("Arial", 12)
    
    # Create the initial add student button
    add_button = tk.Button(sub_frame, text="Add Student", command=add_student, font=("Arial", 14, "bold"), bg=ACCENT_COLOR, fg="white", activebackground=HIGHLIGHT_COLOR, activeforeground="white")
    add_button.pack(pady=5)
    
    # Add the first student
    add_student()

def load_image(path, width, height):
    try:
        if os.path.exists(path):
            img = Image.open(path)
            img = img.resize((width, height), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        else:
            print(f"Image file not found at: {path}")
            return None
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def create_default_button_images():
    """Create default images if button images are not found"""
    # Default Grade Calculator image
    grade_img = Image.new('RGB', (200, 120), color="#f3e5cb")
    # Add text to the image
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(grade_img)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()
    
    draw.text((40, 50), "Grade Calculator", fill="#007367", font=font)
    grade_photo = ImageTk.PhotoImage(grade_img)
    
    # Default GPA Calculator image
    gpa_img = Image.new('RGB', (200, 120), color="#f3e5cb")
    draw = ImageDraw.Draw(gpa_img)
    draw.text((50, 50), "GPA Calculator", fill="#007367", font=font)
    gpa_photo = ImageTk.PhotoImage(gpa_img)
    
    return grade_photo, gpa_photo

def load_logo(path):
    try:
        if os.path.exists(path):
            img = Image.open(path)
            # Increasing the logo size from 150x150 to a larger size
            img = img.resize((250, 125), Image.LANCZOS)  # Changed from (150, 150)
            return ImageTk.PhotoImage(img)
        else:
            print(f"Logo file not found at: {path}")
            return None
    except Exception as e:
        print(f"Error loading logo: {e}")
        return None

def reset_view():
    global add_button, subject_count, student_count
    
    # Reset the counters
    subject_count = 0
    student_count = 0
    add_button = None
    
    # Clear the sub_frame
    for widget in sub_frame.winfo_children():
        widget.destroy()
    
    # Create footer (visible by default)
    create_footer(visible=True)
    
    # Create a container for logo and text
    logo_container = tk.Frame(sub_frame, bg=BG_COLOR)
    logo_container.pack(fill=tk.X, pady=20)
    
    # Load and place the GITAM logo in the center
    logo_img = load_logo(LOGO_PATH)
    if logo_img:
        logo_label = tk.Label(logo_container, image=logo_img, bg=BG_COLOR)
        logo_label.image = logo_img  # Keep a reference to prevent garbage collection
        logo_label.pack(side=tk.TOP, anchor="center")
        
    else:
        # Fallback to text if image loading fails
        logo_label = tk.Label(logo_container, 
                               text="GITAM", 
                               font=("Arial", 20, "bold"), 
                               fg="white", 
                               bg=BG_COLOR)
        logo_label.pack(side=tk.TOP, anchor="center")
        
        univ_text = tk.Label(logo_container, 
                              text="DEEMED TO BE UNIVERSITY", 
                              font=("Arial", 10), 
                              fg="white", 
                              bg=BG_COLOR)
        univ_text.pack(side=tk.TOP, anchor="center")
    
    # Create a container for the calculator buttons
    buttons_container = tk.Frame(sub_frame, bg=BG_COLOR)
    buttons_container.pack(expand=True)
    
    # Try to load the button images
    grade_img = load_image(GRADE_CALC_IMG_PATH, 300, 150)
    gpa_img = load_image(GPA_CALC_IMG_PATH, 300, 150)
    
    # If image loading fails, create default buttons with text on colored background
    if not grade_img or not gpa_img:
        grade_img, gpa_img = create_default_button_images()
    
    # Grade Calculator image button
    grade_button_label = tk.Label(
        buttons_container,
        image=grade_img,
        bg=BG_COLOR,
        cursor="hand2"
    )
    grade_button_label.image = grade_img  # Keep a reference
    grade_button_label.pack(pady=(50, 20))  # Adjusted padding to account for removed text
    grade_button_label.bind("<Button-1>", lambda e: show_grade_calculator())
    
    # GPA Calculator image button
    gpa_button_label = tk.Label(
        buttons_container,
        image=gpa_img,
        bg=BG_COLOR,
        cursor="hand2"
    )
    gpa_button_label.image = gpa_img  # Keep a reference
    gpa_button_label.pack()
    gpa_button_label.bind("<Button-1>", lambda e: show_gpa_calculator())
    

def start_app():
    # Creating the main window
    global root, main_frame, canvas, sub_frame, window, footer_frame
    
    root = tk.Tk()
    root.title("AcademeX")
    root.geometry("750x750")
    root.configure(bg=BG_COLOR)
    
    main_frame = tk.Frame(root, bg=BG_COLOR)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Creating a Canvas and Scrollbar for dynamic subject entry
    canvas = tk.Canvas(main_frame, bg=BG_COLOR, highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    sub_frame = tk.Frame(canvas, bg=BG_COLOR)
    window = canvas.create_window((0, 0), window=sub_frame, anchor="nw", width=1500)
    
    # Initialize footer_frame as None
    footer_frame = None
    
    # Bind the canvas and sub_frame to automatically resize
    canvas.bind("<Configure>", on_canvas_configure)
    sub_frame.bind("<Configure>", on_frame_configure)
    
    # Initialize the main view with options for Grade Calculator and GPA Calculator
    reset_view()
    
    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    start_app()
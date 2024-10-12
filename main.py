import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk

# Function to load the sample image
def load_sample_image():
    global sample_image_path, sample_img_display
    sample_image_path = filedialog.askopenfilename(
        title="Select Sample Fingerprint Image",
        filetypes=[("BMP files", "*.BMP"), ("All files", "*.*")]
    )
    if sample_image_path:
        sample_img = Image.open(sample_image_path)
        sample_img = sample_img.resize((250, 250), Image.LANCZOS)  # Resize for display
        sample_img_display = ImageTk.PhotoImage(sample_img)
        sample_label.config(image=sample_img_display)
        sample_label.image = sample_img_display
        status_label.config(text="Sample Image Loaded!")

# Function to run the fingerprint matching process
def match_fingerprints():
    if not sample_image_path:
        messagebox.showerror("Error", "Please select a sample image first!")
        return

    # Check if the "Real" directory exists
    real_dir = "archive/SOCOFing/Real"
    if not os.path.exists(real_dir):
        messagebox.showerror("Error", f"Directory '{real_dir}' not found!")
        return

    # Load the sample image
    sample = cv2.imread(sample_image_path)

    # Initialize variables to track best match
    best_score = 0
    filename = None
    best_image = None
    kp1, kp2, mp = None, None, None

    # Create SIFT detector
    sift = cv2.SIFT_create()

    # Counter for progress tracking
    total_files = len(os.listdir(real_dir))
    counter = 0

    # Show the loading spinner
    loading_label.pack()
    progress_bar.pack(pady=10)
    
    # Loop through all fingerprint images in the "Real" folder
    for file in os.listdir(real_dir):
        counter += 1
        status_label.config(text=f"Processing image {counter}/{total_files}: {file}")
        root.update_idletasks()

        # Update the progress bar
        progress_bar['value'] = (counter / total_files) * 100

        # Load the current fingerprint image
        fingerprint_image = cv2.imread(os.path.join(real_dir, file))

        # Detect keypoints and descriptors
        keypoints_1, descriptors_1 = sift.detectAndCompute(sample, None)
        keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_image, None)

        # Ensure descriptors are not None (in case no keypoints are found)
        if descriptors_1 is None or descriptors_2 is None:
            continue

        # Use FLANN-based matcher
        flann = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10}, {})
        matches = flann.knnMatch(descriptors_1, descriptors_2, k=2)

        # Filter matches using Lowe's ratio test
        match_points = [p for p, q in matches if len(matches) > 1 and p.distance < 0.1 * q.distance]

        # Skip if no good matches were found
        if not match_points:
            continue

        # Calculate the minimum number of keypoints
        keypoints = min(len(keypoints_1), len(keypoints_2))

        # Update best match if current image has better score
        if len(match_points) / keypoints * 100 > best_score:
            best_score = len(match_points) / keypoints * 100
            filename = file
            best_image = fingerprint_image
            kp1, kp2, mp = keypoints_1, keypoints_2, match_points

    # Hide loading spinner and progress bar
    loading_label.pack_forget()
    progress_bar.pack_forget()

    # Display result
    if filename:
        status_label.config(text=f"BEST MATCH: {filename} | SCORE: {best_score:.2f}")
        print(f"BEST MATCH: {filename}")
        print(f"SCORE: {best_score}")
        result = cv2.drawMatches(sample, kp1, best_image, kp2, mp, None)

        # Resize the result image to a smaller size
        result = cv2.resize(result, None, fx=1.5, fy=1.5)  # Reduced scaling for smaller display

        # Convert the result to ImageTk format for displaying in Tkinter
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        result_img = Image.fromarray(result_rgb)
        result_img_display = ImageTk.PhotoImage(result_img)

        result_label.config(image=result_img_display)
        result_label.image = result_img_display

        # Display comparison message
        messagebox.showinfo("Result", f"Best match found: {filename}\nScore: {best_score:.2f}")
    else:
        messagebox.showinfo("Result", "No match found!")
        status_label.config(text="No match found.")

# Initialize the Tkinter window
root = tk.Tk()
root.title("Fingerprint Matching")
root.geometry("500x600")
root.config(bg='#F0F0F0')

# Global variables
sample_image_path = None
sample_img_display = None

# Style the widgets
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 12), background="#F0F0F0")

# Sample image section
sample_label = tk.Label(root, text="Sample Image", bg="#F0F0F0", font=("Helvetica", 14))
sample_label.pack(pady=10)

# Button to load sample image
load_button = ttk.Button(root, text="Load Sample Image", command=load_sample_image)
load_button.pack(pady=10)

# Button to run the matching algorithm
match_button = ttk.Button(root, text="Match Fingerprints", command=match_fingerprints)
match_button.pack(pady=10)

# Progress/status label
status_label = tk.Label(root, text="Waiting for input...", fg="blue", bg="#F0F0F0", font=("Helvetica", 12))
status_label.pack(pady=10)

# Loading spinner (hidden initially)
loading_img = Image.open("loading_spinner.gif")  # Ensure the spinner image exists
loading_img = loading_img.resize((50, 50), Image.LANCZOS)
loading_spinner = ImageTk.PhotoImage(loading_img)
loading_label = tk.Label(root, image=loading_spinner, bg="#F0F0F0")

# Progress bar (hidden initially)
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")

# Result image section
result_label = tk.Label(root, text="Best Match Result", bg="#F0F0F0", font=("Helvetica", 14))
result_label.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()

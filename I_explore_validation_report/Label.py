import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Directories
input_dir = r"."
output_dir = r"."

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Variables to store rectangle coordinates
start_x, start_y = None, None
drawing = False
current_image_name = None
image_list = []
current_image_index = 0

# Create the GUI window
root = tk.Tk()
root.title("Image Annotation Tool")

# Load all images in the directory
def load_images_from_directory():
    global image_list, current_image_index
    image_list = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not image_list:
        messagebox.showinfo("Info", "No images found in the directory!")
        root.destroy()
        return
    current_image_index = 0
    load_image()

# Load and display the current image
def load_image():
    global img, img_tk, canvas, current_image_name, current_image_index

    if current_image_index >= len(image_list):
        messagebox.showinfo("Info", "All images have been labeled!")
        root.destroy()
        return

    # Load the current image
    current_image_name = os.path.splitext(image_list[current_image_index])[0]
    img_path = os.path.join(input_dir, image_list[current_image_index])
    img = Image.open(img_path)
    img_tk = ImageTk.PhotoImage(img)

    # Clear the canvas and display the new image
    canvas.delete("all")
    canvas.create_image(0, 0, image=img_tk, anchor="nw")

# Start drawing a rectangle
def start_rectangle(event):
    global start_x, start_y, drawing
    start_x, start_y = event.x, event.y
    drawing = True

# Draw the rectangle as the mouse moves
def draw_rectangle(event):
    global start_x, start_y, drawing
    if drawing:
        canvas.delete("temp_rectangle")  # Remove the previous temporary rectangle
        canvas.create_rectangle(start_x, start_y, event.x, event.y, outline="red", width=2, tags="temp_rectangle")

# Dialog to select the label
def label_selection_dialog():
    """
    Open a dialog to select 'dirty' or 'clean' label.
    Returns the selected label as a string or None if canceled.
    """
    def set_label(label):
        nonlocal selected_label
        selected_label = label
        dialog.destroy()

    selected_label = None
    dialog = tk.Toplevel(root)
    dialog.title("Select Label")
    dialog.geometry("200x100")
    dialog.transient(root)  # Make the dialog modal
    dialog.grab_set()

    tk.Label(dialog, text="Select a label for this region:").pack(pady=10)
    tk.Button(dialog, text="Dirty", command=lambda: set_label("dirty")).pack(side="left", padx=10, pady=10)
    tk.Button(dialog, text="Clean", command=lambda: set_label("clean")).pack(side="right", padx=10, pady=10)

    root.wait_window(dialog)  # Wait until the dialog is closed
    return selected_label

# Finish drawing the rectangle and prompt for a label
def end_rectangle(event):
    global start_x, start_y, drawing
    if drawing:
        x1, y1, x2, y2 = start_x, start_y, event.x, event.y
        drawing = False
        canvas.delete("temp_rectangle")  # Remove the temporary rectangle
        canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)  # Finalize the rectangle

        # Ensure coordinates are positive and sorted correctly
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])

        # Prompt the user to select the label
        label = label_selection_dialog()
        if label in ["dirty", "clean"]:
            # Save cropped region to appropriate directory
            cropped_region = img.crop((x1, y1, x2, y2))
            region_output_dir = os.path.join(output_dir, label)
            os.makedirs(region_output_dir, exist_ok=True)
            region_filename = f"{current_image_name}_{label}_{x1}_{y1}_{x2}_{y2}.png"
            cropped_region.save(os.path.join(region_output_dir, region_filename))
            print(f"Saved labeled region as {region_filename}")
        else:
            messagebox.showerror("Invalid Label", "Please select a valid label.")

# Move to the next image
def save_annotations_and_next():
    global current_image_index
    current_image_index += 1
    if current_image_index < len(image_list):
        load_image()
    else:
        messagebox.showinfo("Info", "All images have been labeled!")
        canvas.delete("all")
        canvas.create_text(400, 300, text="All images labeled!", font=("Arial", 24), fill="green")

# GUI components
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

# Buttons and event bindings
btn_next = tk.Button(root, text="Save and Next", command=save_annotations_and_next)
btn_next.pack()

canvas.bind("<ButtonPress-1>", start_rectangle)
canvas.bind("<B1-Motion>", draw_rectangle)
canvas.bind("<ButtonRelease-1>", end_rectangle)

# Load images from the directory at the start
load_images_from_directory()

# Run the GUI
root.mainloop()

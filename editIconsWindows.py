import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
from PIL import Image, ImageTk

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        input_path.set(file_path)

def select_output():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        output_path.set(file_path)

def choose_target_color():
    color_code = colorchooser.askcolor(title="Choose Target Color")[0]
    if color_code:
        target_color.set(f"RGB({int(color_code[0])}, {int(color_code[1])}, {int(color_code[2])})")
        target_color_rgb.set((int(color_code[0]), int(color_code[1]), int(color_code[2])))

def choose_replacement_color():
    color_code = colorchooser.askcolor(title="Choose Replacement Color")[0]
    if color_code:
        replacement_color.set(f"RGB({int(color_code[0])}, {int(color_code[1])}, {int(color_code[2])})")
        replacement_color_rgb.set((int(color_code[0]), int(color_code[1]), int(color_code[2])))

def process_image():
    try:
        image = Image.open(input_path.get()).convert("RGBA")
        datas = image.getdata()
        new_data = []

        target = target_color_rgb.get()
        replacement = replacement_color_rgb.get()

        for item in datas:
            if (item[0], item[1], item[2]) == target and item[3] > 0:
                new_data.append((*replacement, item[3]))
            else:
                new_data.append(item)

        image.putdata(new_data)
        image.save(output_path.get(), "PNG")
        messagebox.showinfo("Success", f"Image saved at: {output_path.get()}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Image Color Editor")
root.configure(bg="#2e2e2e")

# Apply dark theme
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#2e2e2e", foreground="#ffffff")
style.configure("TButton", background="#444444", foreground="#ffffff", borderwidth=1)
style.map("TButton", background=[("active", "#555555")])
style.configure("TEntry", fieldbackground="#444444", foreground="#ffffff", insertcolor="#ffffff")

# Variables
input_path = tk.StringVar()
output_path = tk.StringVar()
target_color = tk.StringVar(value="No target color selected")
replacement_color = tk.StringVar(value="No replacement color selected")
target_color_rgb = tk.Variable(value=(255, 255, 255))
replacement_color_rgb = tk.Variable(value=(255, 255, 255))

# Layout
ttk.Label(root, text="Input Image:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
ttk.Entry(root, textvariable=input_path, width=40).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(root, text="Browse", command=select_image).grid(row=0, column=2, padx=5, pady=5)

ttk.Label(root, text="Output Image:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
ttk.Entry(root, textvariable=output_path, width=40).grid(row=1, column=1, padx=5, pady=5)
ttk.Button(root, text="Save As", command=select_output).grid(row=1, column=2, padx=5, pady=5)

ttk.Label(root, text="Target Color:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
ttk.Label(root, textvariable=target_color).grid(row=2, column=1, padx=5, pady=5)
ttk.Button(root, text="Choose Target Color", command=choose_target_color).grid(row=2, column=2, padx=5, pady=5)

ttk.Label(root, text="Replacement Color:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
ttk.Label(root, textvariable=replacement_color).grid(row=3, column=1, padx=5, pady=5)
ttk.Button(root, text="Choose Replacement Color", command=choose_replacement_color).grid(row=3, column=2, padx=5, pady=5)

ttk.Button(root, text="Process Image", command=process_image).grid(row=4, column=0, columnspan=3, pady=10)

# Run the application
root.mainloop()
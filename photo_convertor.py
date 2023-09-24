import tkinter as tk
from tkinter import filedialog
import cv2
from tkinter import messagebox

def convert_to_sketch(image_path, background_color, output_path):
    image = cv2.imread(image_path)
    if image is None:
        tk.messagebox.showerror("Erreur", f"Impossible de lire l'image {image_path}")
        return

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred_image = cv2.GaussianBlur(gray_image, (21, 21), 0)

    sketched_image = cv2.adaptiveThreshold(
        blurred_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=15, C=2)

    if background_color.lower() == 'noir':
        sketched_image = 255 - sketched_image

    cv2.imwrite(output_path, sketched_image)
    tk.messagebox.showinfo("Succès", f"Image sauvegardée sous {output_path}")

def on_open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        image_path.set(file_path)

def on_convert():
    background_color = bg_color_var.get()
    output_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                               filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
    if output_path:
        convert_to_sketch(image_path.get(), background_color, output_path)

root = tk.Tk()

image_path = tk.StringVar()
bg_color_var = tk.StringVar(value='blanc')

tk.Label(root, text="Sélectionnez votre image :").pack(padx=10, pady=5)
open_file_button = tk.Button(root, text="Ouvrir l'image", command=on_open_file)
open_file_button.pack(pady=5)

file_path_label = tk.Label(root, textvar=image_path)
file_path_label.pack(padx=10, pady=5)

tk.Radiobutton(root, text="Fond blanc", variable=bg_color_var, value='blanc').pack()
tk.Radiobutton(root, text="Fond noir", variable=bg_color_var, value='noir').pack()

convert_button = tk.Button(root, text="Convertir en dessin", command=on_convert)
convert_button.pack(pady=10)

root.mainloop()

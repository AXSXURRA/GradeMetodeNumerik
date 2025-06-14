import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def hitung_nilai():
    try:
        nilaihadir = int(entry_kehadiran.get())
        nilaitugas = int(entry_tugas.get())
        nilaiquizz = int(entry_quiz.get())
        nilaiuts = int(entry_uts.get())
        nilaiuas = int(entry_uas.get())

        bobot = {
            "Kehadiran": 0.15,
            "Tugas": 0.20,
            "Quiz": 0.15,
            "UTS": 0.25,
            "UAS": 0.25
        }

        nilaiakhir = (
            bobot["Kehadiran"] * nilaihadir +
            bobot["Tugas"] * nilaitugas +
            bobot["Quiz"] * nilaiquizz +
            bobot["UTS"] * nilaiuts +
            bobot["UAS"] * nilaiuas
        )

        if nilaiakhir >= 85:
            grade = "A"
        elif 80 <= nilaiakhir < 85:
            grade = "AB"
        elif 75 <= nilaiakhir < 80:
            grade = "B"
        elif 70 <= nilaiakhir < 75:
            grade = "BC"
        elif 65 <= nilaiakhir < 70:
            grade = "C"
        elif 60 <= nilaiakhir < 65:
            grade = "D"
        else:
            grade = "E"

        hasil_var.set(f"🎓 Nilai Akhir: {nilaiakhir:.2f} | Grade: {grade}")

        for row in tree.get_children():
            tree.delete(row)
        tree.insert("", "end", values=(nilaihadir, nilaitugas, nilaiquizz, nilaiuts, nilaiuas, f"{nilaiakhir:.2f}", grade))

        tampilkan_grafik(
            [nilaihadir, nilaitugas, nilaiquizz, nilaiuts, nilaiuas],
            list(bobot.keys())
        )

    except ValueError:
        messagebox.showerror("Input Error", "Masukkan semua nilai dengan angka bulat!")

def tampilkan_grafik(nilai_list, label_list):
    win = tk.Toplevel()
    win.title("Visualisasi Nilai Mahasiswa")
    win.configure(bg="#ecf0f1")
    win.geometry("1100x450")

    fig, axs = plt.subplots(1, 3, figsize=(15, 4))
    fig.subplots_adjust(wspace=0.4)

    colors = ['#F1948A', '#F7DC6F', '#82E0AA', '#85C1E9', '#D2B4DE']

    axs[0].bar(label_list, nilai_list, color=colors, edgecolor='black')
    axs[0].set_title("Diagram Batang", fontsize=12)
    axs[0].set_ylim(0, 100)
    axs[0].grid(axis='y', linestyle='--', alpha=0.4)
    axs[0].tick_params(axis='x', rotation=45)

    axs[1].pie(nilai_list, labels=label_list, autopct='%1.1f%%', startangle=90,
               explode=[0.1 if i == max(nilai_list) else 0 for i in nilai_list],
               shadow=True, colors=colors)
    axs[1].set_title("Diagram Lingkaran", fontsize=12)

    axs[2].plot(label_list, nilai_list, color="#e74c3c", marker="o", linewidth=2)
    axs[2].set_title("Diagram Garis", fontsize=12)
    axs[2].set_ylim(0, 100)
    axs[2].grid(True, linestyle='--', alpha=0.3)
    axs[2].tick_params(axis='x', rotation=45)

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')


root = tk.Tk()
root.title("Sistem Penilaian Mahasiswa")
root.geometry("780x580")
root.configure(bg="#fdfdfd")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)


tab_input = tk.Frame(notebook, bg="#f8f9fa")
notebook.add(tab_input, text="📝 Penilaian Akhir")

header = tk.Label(tab_input, text="Form Penilaian Akhir Mahasiswa", bg="#f8f9fa",
                  fg="#2c3e50", font=("Helvetica", 18, "bold"))
header.pack(pady=20)

form_card = tk.Frame(tab_input, bg="#ffffff", bd=2, relief="groove")
form_card.pack(padx=20, pady=10)

labels = ["Kehadiran", "Tugas", "Quiz", "UTS", "UAS"]
entries = []

for i, label in enumerate(labels):
    tk.Label(form_card, text=f"{label}:", font=("Segoe UI", 11), bg="white", anchor="w", width=15).grid(row=i, column=0, padx=15, pady=8, sticky="e")
    entry = tk.Entry(form_card, font=("Segoe UI", 11), width=12)
    entry.grid(row=i, column=1, padx=15, pady=8)
    entries.append(entry)

entry_kehadiran, entry_tugas, entry_quiz, entry_uts, entry_uas = entries

btn_hitung = tk.Button(tab_input, text="Hitung Nilai", command=hitung_nilai,
                       bg="#3498db", fg="white", font=("Segoe UI", 12, "bold"), width=20, bd=0)
btn_hitung.pack(pady=20)

hasil_var = tk.StringVar()
label_hasil = tk.Label(tab_input, textvariable=hasil_var, font=("Segoe UI", 13, "bold"),
                       bg="#f8f9fa", fg="#2d3436")
label_hasil.pack()


tab_tabel = tk.Frame(notebook, bg="#f8f9fa")
notebook.add(tab_tabel, text="📊 Tabel Nilai")

tree = ttk.Treeview(tab_tabel, columns=("Kehadiran", "Tugas", "Quiz", "UTS", "UAS", "Akhir", "Grade"), show="headings")
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=90)
tree.pack(pady=30, padx=20, fill='x')

root.mainloop()

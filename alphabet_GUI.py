# alphabet_GUI.py

#3.Use the artificial intelligence to design an application with a graphical user interface that is able to integrate your 
#  algorithm from assignment 1 and 2.
# -Your application must have a button which allows the user to choose a 'Fasta' file.
# -'Fasta' files contain a specific biological format.
# -The output should be shown on he main window by using a text box object or something similar.

# 'Fasta' files have the following format:
# 1) The 1st line is the information line that show the ID of the sequence, the species and other types of informations.
# 2) Starting from the second line, we have the row sequence, which can be DNA, ARN or proteins that is split 
# in 80 character lines until the  end of the file. Use the AI to simulate a 'Fasta' file for the input.

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from collections import Counter
import textwrap
import tempfile
from pathlib import Path

def parse_fasta(path: Path):
    """Return (header_or_none, sequence_str). Accept plain sequence files too."""
    with path.open("r", encoding="utf-8") as fh:
        lines = [l.rstrip("\n") for l in fh]
    if not lines:
        return (None, "")
    if lines[0].startswith(">"):
        header = lines[0][1:].strip()
        seq_lines = [ln.strip() for ln in lines[1:] if ln and not ln.startswith(">")]
        seq = "".join(seq_lines)
    else:
        header = None
        seq = "".join(l.strip() for l in lines)
    return (header, seq.upper())

def alphabet_of(seq: str):
    return "".join(sorted(set(seq)))

def freqs(seq: str):
    length = len(seq)
    if length == 0:
        return {}
    c = Counter(seq)
    return {sym: c[sym] / length for sym in sorted(c.keys())}

def show_result(header, seq):
    out.delete("1.0", tk.END)
    if header:
        out.insert(tk.END, f"Header: {header}\n")
    out.insert(tk.END, f"Length: {len(seq)}\n")
    out.insert(tk.END, f"Alphabet: {list(alphabet_of(seq))}\n\n")
    out.insert(tk.END, "Relative frequencies:\n")
    for sym, fr in freqs(seq).items():
        out.insert(tk.END, f"{sym}: {fr:.3f}\n")

def open_fasta():
    fp = filedialog.askopenfilename(
        title="Open FASTA or sequence file",
        filetypes=[("FASTA / text", "*.fa *.fasta *.txt *.seq"), ("All files", "*.*")]
    )
    if not fp:
        return
    try:
        header, seq = parse_fasta(Path(fp))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {e}")
        return
    seq = "".join(seq.split())  # remove whitespace/newlines if any left
    show_result(header, seq)

def simulate_fasta_and_load():
    user_seq = seq_entry.get("1.0", tk.END).strip().replace(" ", "").replace("\n", "")
    if not user_seq:
        messagebox.showwarning("Input required", "Enter a sequence to simulate a FASTA file.")
        return
    # create a simple AI-like header and wrap sequence to 80 chars
    header = "simulated|AI_generated|example"
    wrapped = textwrap.fill(user_seq, width=80)
    try:
        tf = tempfile.NamedTemporaryFile("w", delete=False, suffix=".fa", encoding="utf-8")
        tf.write(f">{header}\n")
        tf.write(wrapped + "\n")
        tf.flush()
        tf.close()
        # parse back to ensure same logic as real FASTA
        h, seq = parse_fasta(Path(tf.name))
        show_result(h, seq)
        messagebox.showinfo("Simulated FASTA", f"Simulated FASTA written to:\n{tf.name}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to simulate FASTA: {e}")

def clear_all():
    seq_entry.delete("1.0", tk.END)
    out.delete("1.0", tk.END)

root = tk.Tk()
root.title("Alphabet & Frequency (FASTA)")

frm = ttk.Frame(root, padding=10)
frm.grid(row=0, column=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

btn_open = ttk.Button(frm, text="Open FASTA...", command=open_fasta)
btn_open.grid(row=0, column=0, padx=5, pady=5, sticky="w")

btn_sim = ttk.Button(frm, text="Simulate FASTA from Input", command=simulate_fasta_and_load)
btn_sim.grid(row=0, column=1, padx=5, pady=5, sticky="w")

btn_clear = ttk.Button(frm, text="Clear", command=clear_all)
btn_clear.grid(row=0, column=2, padx=5, pady=5, sticky="w")

ttk.Label(frm, text="Paste sequence (or edit) and click 'Simulate FASTA':").grid(row=1, column=0, columnspan=3, sticky="w", pady=(10,0))
seq_entry = tk.Text(frm, height=4, width=70)
seq_entry.grid(row=2, column=0, columnspan=3, pady=5, sticky="we")

ttk.Label(frm, text="Output:").grid(row=3, column=0, columnspan=3, sticky="w", pady=(10,0))
out = tk.Text(frm, height=12, width=70)
out.grid(row=4, column=0, columnspan=3, pady=5, sticky="we")

# make UI expand nicely
for i in range(3):
    frm.columnconfigure(i, weight=1)
frm.rowconfigure(4, weight=1)

root.mainloop()
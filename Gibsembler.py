import re
import sys
import subprocess
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from Bio import SeqIO

# Ensure missing libraries are installed
def install_missing_libraries():
    """Checks for missing libraries and installs them if necessary."""
    required_libraries = ["pandas", "openpyxl", "biopython", "tkinter"]
    missing_libraries = []
    
    for lib in required_libraries:
        try:
            __import__(lib)
        except ImportError:
            missing_libraries.append(lib)
    
    if missing_libraries:
        messagebox.showinfo("Installing Libraries", f"The following libraries are missing and will be installed: {', '.join(missing_libraries)}")
        for lib in missing_libraries:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
        messagebox.showinfo("Installation Complete", "All required libraries have been installed. The program will now proceed.")

install_missing_libraries()

# DNA analysis functions
def calculate_gc_content(sequence):
    """Calculate the GC content of a given DNA sequence."""
    return (sequence.count("G") + sequence.count("C")) / len(sequence) * 100 if sequence else 0

def calculate_tm(sequence):
    """Calculate the melting temperature (Tm) using Wallace rule: Tm = 2(A+T) + 4(G+C)."""
    return (2 * (sequence.count("A") + sequence.count("T"))) + (4 * (sequence.count("G") + sequence.count("C"))) if sequence else 0

def read_sequence(file_path):
    """Reads a FASTA or GenBank file and returns the sequence as a string."""
    file_extension = file_path.split(".")[-1].lower()
    try:
        record = SeqIO.read(file_path, "genbank" if file_extension in ["gb", "gbk"] else "fasta")
        return str(record.seq)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {e}")
        return ""

# Gibson Assembly segmentation
def optimize_segment(dna_seq, start, min_length=20, max_length=50, target_gc=(40, 60), target_tm=(57, 60)):
    """Finds the optimal segment size within the given constraints."""
    best_segment, best_gc, best_tm, best_length = None, None, None, None
    for length in range(min_length, max_length + 1):
        end = (start + length) % len(dna_seq)
        segment = dna_seq[start:end] if end > start else dna_seq[start:] + dna_seq[:end]
        gc, tm = calculate_gc_content(segment), calculate_tm(segment)
        if target_gc[0] <= gc <= target_gc[1] and target_tm[0] <= tm <= target_tm[1]:
            return segment, length, gc, tm
        if best_tm is None or abs(tm - sum(target_tm) / 2) < abs(best_tm - sum(target_tm) / 2):
            best_segment, best_gc, best_tm, best_length = segment, gc, tm, length
    return best_segment, best_length, best_gc, best_tm

def segment_dna_for_gibson(dna_seq, min_length=20, max_length=50, overlap_min=10, overlap_max=15):
    """Segments a circular plasmid sequence with dynamic window size optimization."""
    segments, i, seq_length = [], 0, len(dna_seq)
    while i < seq_length:
        segment, segment_length, gc, tm = optimize_segment(dna_seq, i, min_length, max_length)
        overlap_length = min(overlap_max, max(overlap_min, segment_length // 2))
        overlap = dna_seq[i + segment_length - overlap_length:i + segment_length] if i + segment_length < seq_length else dna_seq[i + segment_length - overlap_length:] + dna_seq[:(i + segment_length) % seq_length]
        highlighted_segment = segment.replace(overlap, f'[{overlap}]')
        segments.append((highlighted_segment, segment_length, gc, tm, overlap, overlap_length))
        if i + segment_length >= seq_length:
            break
        i += segment_length - overlap_length
    return segments

# Save results
def save_segments(output_file, segments, file_format):
    """Saves the segmented DNA sequences to a chosen format."""
    if file_format == "Excel":
        wb = Workbook()
        ws = wb.active
        ws.append(["Segment Sequence", "Length", "GC Content (%)", "Tm (°C)", "Overlap Sequence", "Overlap Length"])
        red_fill = PatternFill(start_color="FF9999", end_color="FF9999", fill_type="solid")
        for row_idx, (segment, length, gc, tm, overlap, overlap_length) in enumerate(segments, start=2):
            ws.append([segment, length, gc, tm, overlap, overlap_length])
            segment_cell = ws.cell(row=row_idx, column=1)
            if overlap in segment:
                segment_cell.fill = red_fill
        wb.save(output_file)
    else:
        df = pd.DataFrame(segments, columns=["Segment Sequence", "Length", "GC Content (%)", "Tm (°C)", "Overlap Sequence", "Overlap Length"])
        df.to_csv(output_file, index=False)
    print(f"Segments saved to {output_file}")

# GUI
def main():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Welcome to Gibsembler", "Welcome to Gibsembler!\n\nThis program allows you to segment a plasmid DNA sequence for Gibson Assembly.\n\nClick OK to proceed.")
    input_file = filedialog.askopenfilename(title="Select DNA Sequence File", filetypes=[("FASTA or GenBank Files", "*.fasta;*.gb;*.gbk")])
    if not input_file:
        return
    save_path = filedialog.asksaveasfilename(title="Save File As", defaultextension=".csv", filetypes=[("CSV File", "*.csv"), ("Excel File", "*.xlsx")])
    if not save_path:
        return
    file_format = "Excel" if save_path.endswith(".xlsx") else "CSV"
    dna_sequence = read_sequence(input_file)
    gibson_segments = segment_dna_for_gibson(dna_sequence)
    save_segments(save_path, gibson_segments, file_format)
    messagebox.showinfo("Success", f"Segments saved successfully as {save_path}")

if __name__ == "__main__":
    main()

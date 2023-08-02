from tkinter import filedialog, simpledialog, messagebox, ttk
from collections import defaultdict
from datetime import datetime
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import csv
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image as rpImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import tkinter as tk
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.colors import black, red
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image as ReportLabImage
from PIL import Image as PILImage


class Tree:
    def __init__(self):
        self.tree = defaultdict(list)
        self.paths = []

    def add_edge(self, parent, child):
        self.tree[parent].append(child)

    def navigate(self, node):
        children = self.tree.get(node, [])
        return children

    def load_tree_from_csv(self, filename):
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            for path in reader:
                for i in range(len(path)-1):
                    self.add_edge(path[i], path[i+1])


    def get_all_paths(self, start_node):
        self.paths = []
        self._find_paths(start_node, [start_node])
        return self.paths

    def draw_tree(self):
        # here we will save the graph as png and return the png file path
        g = nx.DiGraph()
        for parent, children in self.tree.items():
            for child in children:
                g.add_edge(parent, child)
        plt.figure()
        nx.draw(g, with_labels=True, node_color='skyblue')
        png_file_path = "tree.png"
        plt.savefig(png_file_path)
        plt.close()
        return png_file_path


    def _find_paths(self, node, path):
        children = self.tree.get(node, [])
        if not children:
            self.paths.append(path)
        for child in children:
            self._find_paths(child, path + [child])

    def find_paths(self, node):
        self.paths = []
        self._find_paths(node, [node])
        return self.paths

    def save_paths_to_csv(self, start_node, filename):
        paths = self.find_paths(start_node)
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for path in paths:
                writer.writerow(path)

    

class TreeGUI:
    def __init__(self, master):
        self.master = master
        self.tree = Tree()
        self.master.geometry("1200x800")
        self.create_widgets()

        self.logo = ImageTk.PhotoImage(Image.open('logo_v3_small.png')) # Ensure the logo image is in the same directory as your script
        self.logo_label = tk.Label(master, image=self.logo)
        self.logo_label.grid(row=0, column=0)  # Adjust the placement as needed

        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=8, padx=10, pady=10)

    def create_widgets(self):
        frame = tk.Frame(self.master)
        frame.grid(row=1, column=0, padx=10, pady=10)

        self.load_csv_button = tk.Button(frame, text="Load Tree from CSV", command=self.load_csv, width=20, bg='#0052cc', fg='#ffffff')
        self.load_csv_button.pack(side="left")
        #adding the browsing capabilities here as well
        self.browse_button = tk.Button(frame, text="Browse", command=self.browse_file, width=20, bg='#0052cc', fg='#ffffff')
        self.browse_button.pack(side="left")


        self.load_csv_entry = tk.Entry(frame, bd=5)
        self.load_csv_entry.pack(side="right")

        frame = tk.Frame(self.master)
        frame.grid(row=2, column=0, padx=10, pady=10)

        self.add_node_button = tk.Button(frame, text="Add Node", command=self.add_node, width=20, bg='#0052cc', fg='#ffffff')
        self.add_node_button.pack(side="left")

        self.parent_entry = tk.Entry(frame, bd=5)
        self.parent_entry.pack(side="right")
        self.parent_entry.insert(0, 'Parent Node')

        self.child_entry = tk.Entry(frame, bd=5)
        self.child_entry.pack(side="right")
        self.child_entry.insert(0, 'Child Node')

        frame = tk.Frame(self.master)
        frame.grid(row=3, column=0, padx=10, pady=10)

        self.navigate_button = tk.Button(frame, text="Navigate Tree", command=self.navigate_tree, width=20, bg='#0052cc', fg='#ffffff')
        self.navigate_button.pack(side="left")

        self.navigate_entry = tk.Entry(frame, bd=5)
        self.navigate_entry.pack(side="right")
        self.navigate_entry.insert(0, 'Node to Navigate')

        frame = tk.Frame(self.master)
        frame.grid(row=4, column=0, padx=10, pady=10)

        self.find_paths_button = tk.Button(frame, text="Find Paths", command=self.find_paths, width=20, bg='#0052cc', fg='#ffffff')
        self.find_paths_button.pack(side="left")

        self.find_paths_entry = tk.Entry(frame, bd=5)
        self.find_paths_entry.pack(side="right")
        self.find_paths_entry.insert(0, 'Start Node for Paths')

        frame = tk.Frame(self.master)
        frame.grid(row=5, column=0, padx=10, pady=10)

        self.save_csv_button = tk.Button(frame, text="Save Paths to CSV", command=self.save_paths_to_csv, width=20, bg='#0052cc', fg='#ffffff')
        self.save_csv_button.pack(side="left")

        self.save_csv_entry = tk.Entry(frame, bd=5)
        self.save_csv_entry.pack(side="right")
        self.save_csv_entry.insert(0, 'CSV Filename')

        frame = tk.Frame(self.master)
        frame.grid(row=6, column=0, padx=10, pady=10, sticky='w')

        self.save_pdf_button = tk.Button(frame, text="Save Paths to PDF", command=self.save_paths_to_pdf, width=20,
                                         bg='#0052cc', fg='#ffffff')
        self.save_pdf_button.pack(side="left")

        self.save_pdf_entry = tk.Entry(frame, bd=5)
        self.save_pdf_entry.pack(side="right", fill="x", expand=True)
        self.save_pdf_entry.insert(0, 'PDF Filename')

        # include a browse button that allowes to browse for a file to save the pdf to and use is at pfd filename
        self.browse_button = tk.Button(frame, text="Browse", command=self.browse_file, width=20, bg='#0052cc', fg='#ffffff')
        self.browse_button.pack(side="right")
                





        self.quit_button = tk.Button(self.master, text="QUIT", command=self.master.quit, width=20, bg='red',
                                     fg='#ffffff')
        self.quit_button.grid(row=7, column=0, padx=10, pady=10)

    #solving 'TreeGUI' object has no attribute 'browse_file' error
    def browse_file(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetype=(("csv files", "*.csv"), ("all files", "*.*")))
        self.save_pdf_entry.insert(0, self.filename)


    def load_csv(self):
        filename = self.load_csv_entry.get()
        if filename:
            self.tree.load_tree_from_csv(filename)
            self.draw_tree()

    def add_node(self):
        parent = self.parent_entry.get()
        child = self.child_entry.get()
        if parent and child:
            self.tree.add_edge(parent, child)
            self.draw_tree()

    def navigate_tree(self):
        node = self.navigate_entry.get()
        if node:
            children = self.tree.navigate(node)
            messagebox.showinfo("Navigate Tree", "Children: " + ', '.join(children))

    def find_paths(self):
        node = self.find_paths_entry.get()
        if node:
            paths = self.tree.find_paths(node)
            paths_str = '\n'.join([' -> '.join(path) for path in paths])
            messagebox.showinfo("Find Paths", "Paths:\n" + paths_str)

    def save_paths_to_csv(self):
        node = self.find_paths_entry.get()
        filename = self.save_csv_entry.get()
        if node and filename:
            self.tree.save_paths_to_csv(node, filename)
            messagebox.showinfo("Save Paths to CSV", "Paths saved to " + filename)

    def draw_tree(self):
        G = self.tree.draw_tree()
        self.ax.clear()
        nx.draw(G, with_labels=True, ax=self.ax)
        self.canvas.draw()

    def save_paths_to_pdf(self):
        node = simpledialog.askstring("Input", "Enter start node for paths:")
        if node:
            filename = filedialog.asksaveasfilename(defaultextension=".pdf")
            if filename:
                # Find paths and convert them to data
                paths = self.tree.find_paths(node)
                data = [path for path in paths]

                # Set up the PDF document and styles
                doc = SimpleDocTemplate(filename, pagesize=letter)
                styles = getSampleStyleSheet()

                # Create the logo, title, and date Paragraph objects
                logo = Image('logo_v3_small.png', width=60, height=60)
                title = Paragraph("Tree Paths", styles["Title"])
                date = Paragraph(datetime.now().strftime("%Y-%m-%d"), styles["Normal"])

                # Draw the tree and save as PNG
                img_filename = "tree.png"
                self.tree.draw_tree(img_filename)
                img = Image.open(img_filename).resize((500, 500), Image.BICUBIC)
                
                # Create the table with paths
                table = Table(data)
                table_style = TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.green),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),

                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0,0), (-1,-1), 1, colors.black)
                    ]
                )
                table.setStyle(table_style)

                # Build the PDF
                elements = [logo, title, date, img, table]
                doc.build(elements)
                messagebox.showinfo("Info", "PDF successfully saved!")


if __name__ == "__main__":
    root = tk.Tk()
    app = TreeGUI(root)
    root.mainloop()
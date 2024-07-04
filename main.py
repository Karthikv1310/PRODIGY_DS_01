import time
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, filedialog, Button, Label, Frame, OptionMenu, StringVar, Spinbox, IntVar, Checkbutton, colorchooser, messagebox, Entry, ttk, Text, WORD, INSERT
import pandas as pd

class DataVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Visualizer")
        self.file_path = None
        self.data = None
        self.current_plot = None
        self.correlation_plot = None
        self.time_plot = None
        self.space_plot = None

        self.setup_ui()

    def setup_ui(self):
        # Create a tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # First tab - Data Loading
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Data Loading')

        self.setup_data_loading()

        # Second tab - Data Visualization
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='Data Visualization')

        # Third tab - Data Analysis
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='Data Analysis')

        self.setup_data_analysis()

    def setup_data_loading(self):
        main_frame = Frame(self.tab1, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)

        title_label = Label(main_frame, text="Excel Data Visualizer", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=20)

        load_button = Button(main_frame, text="Load Excel File", font=("Arial", 12), command=self.load_file)
        load_button.pack(pady=10)

        instructions = Label(main_frame, text="Load an Excel file to visualize data.", font=("Arial", 12))
        instructions.pack(pady=10)

    def setup_data_analysis(self):
        main_frame = Frame(self.tab3, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)

        title_label = Label(main_frame, text="Data Analysis", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=20)

        # Create a PanedWindow with horizontal orientation
        paned_window = ttk.PanedWindow(main_frame, orient='horizontal')
        paned_window.pack(expand=True, fill='both')

        # Left pane for buttons
        left_pane = Frame(paned_window, padx=10, pady=10)
        paned_window.add(left_pane)

        # Right pane for output
        right_pane = Frame(paned_window, padx=10, pady=10)
        paned_window.add(right_pane)

        # Buttons in the left pane
        correlation_button = Button(left_pane, text="Generate Correlation Matrix", font=("Arial", 12), command=self.generate_correlation_matrix)
        correlation_button.pack(pady=10, padx=10, fill='x')

        summary_button = Button(left_pane, text="Show Statistical Summary", font=("Arial", 12), command=self.show_statistical_summary)
        summary_button.pack(pady=10, padx=10, fill='x')

        time_button = Button(left_pane, text="Calculate Time Complexity", font=("Arial", 12), command=self.calculate_time_complexity)
        time_button.pack(pady=10, padx=10, fill='x')

        space_button = Button(left_pane, text="Calculate Space Complexity", font=("Arial", 12), command=self.calculate_space_complexity)
        space_button.pack(pady=10, padx=10, fill='x')

        # Reset button
        reset_button = Button(left_pane, text="Reset", font=("Arial", 12), command=self.reset_output)
        reset_button.pack(pady=10, padx=10, fill='x')

        # Output area in the right pane (initially placeholder message)
        self.correlation_plot = Label(right_pane, text="Select an analysis to display results.", font=("Arial", 12))
        self.correlation_plot.pack(expand=True)

        # Assigning to self for future reference
        self.right_pane = right_pane

    def reset_output(self):
        # Clear all output in the right pane
        for widget in self.right_pane.winfo_children():
            widget.destroy()

        # Reset any stored plots or data
        self.current_plot = None
        self.correlation_plot = None
        self.time_plot = None
        self.space_plot = None

        # Display a placeholder message
        placeholder_label = Label(self.right_pane, text="Select an analysis to display results.", font=("Arial", 12))
        placeholder_label.pack(expand=True)

    def clear_window(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls *.xlsx")])
        if self.file_path:
            try:
                if self.file_path.endswith('.xls'):
                    self.data = pd.read_excel(self.file_path, engine='xlrd')
                else:
                    self.data = pd.read_excel(self.file_path, engine='openpyxl')
                self.column_selection_window()
                messagebox.showinfo("Info", "File loaded successfully! Please go to the Data Visualization tab.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read the Excel file: {e}")

    def column_selection_window(self):
        self.clear_window(self.tab2)

        main_frame = Frame(self.tab2, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)

        control_frame = Frame(main_frame)
        control_frame.grid(row=0, column=0, padx=10, pady=10)

        plot_frame = Frame(main_frame)
        plot_frame.grid(row=0, column=1, padx=10, pady=10)

        Label(control_frame, text="Select the column to plot:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.column_var = StringVar(self.root)
        OptionMenu(control_frame, self.column_var, *self.data.columns).grid(row=0, column=1, padx=5, pady=5)

        Label(control_frame, text="Plot Type:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.plot_type_var = StringVar(self.root)
        OptionMenu(control_frame, self.plot_type_var, "Histogram", "Bar Chart", "Line Plot", "Scatter Plot").grid(row=1, column=1, padx=5, pady=5)

        Label(control_frame, text="Number of bins (for histogram):", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
        self.bins_var = IntVar(value=10)
        Spinbox(control_frame, from_=1, to=50, textvariable=self.bins_var).grid(row=2, column=1, padx=5, pady=5)

        self.normalize_var = IntVar()
        Checkbutton(control_frame, text="Normalize", variable=self.normalize_var, font=("Arial", 12)).grid(row=3, columnspan=2, padx=5, pady=5)

        self.color_var = StringVar(value="skyblue")
        Button(control_frame, text="Select Color", font=("Arial", 12), command=self.select_color).grid(row=4, column=0, padx=5, pady=5)

        self.plot_title = StringVar()
        Label(control_frame, text="Plot Title:", font=("Arial", 12)).grid(row=5, column=0, padx=5, pady=5)
        Entry(control_frame, textvariable=self.plot_title, font=("Arial", 12)).grid(row=5, column=1, padx=5, pady=5)

        plot_button = Button(control_frame, text="Plot", font=("Arial", 12), command=self.plot_data)
        plot_button.grid(row=6, columnspan=2, padx=5, pady=10)

        reset_button = Button(control_frame, text="Reset", font=("Arial", 12), command=self.reset_plot)
        reset_button.grid(row=7, columnspan=2, padx=5, pady=10)

        self.plot_frame = plot_frame  # Save reference to plot_frame

    def select_color(self):
        color_code = colorchooser.askcolor(title="Choose color")[1]
        if color_code:
            self.color_var.set(color_code)

    def plot_data(self):
        column = self.column_var.get()
        plot_type = self.plot_type_var.get()
        bins = self.bins_var.get()
        normalize = self.normalize_var.get()
        color = self.color_var.get()
        title = self.plot_title.get()

        if not column:
            messagebox.showerror("Error", "Please select a column.")
            return

        fig, ax = plt.subplots(figsize=(8, 6))

        if plot_type == "Histogram":
            self.data[column].hist(bins=bins, ax=ax, color=color, alpha=0.7, density=normalize)
        elif plot_type == "Bar Chart":
            self.data[column].value_counts().plot(kind='bar', ax=ax, color=color)
        elif plot_type == "Line Plot":
            self.data.plot(x=self.data.index, y=column, kind='line', ax=ax, color=color)
        elif plot_type == "Scatter Plot":
            ax.scatter(self.data.index, self.data[column], color=color)

        ax.set_title(title)
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency' if plot_type == "Histogram" else column)

        # Clear previous plot if exists
        if self.current_plot:
            self.current_plot.get_tk_widget().destroy()

        self.current_plot = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.current_plot.draw()
        self.current_plot.get_tk_widget().pack()

    def reset_plot(self):
        if self.current_plot:
            self.current_plot.get_tk_widget().destroy()
            self.current_plot = None

    def generate_correlation_matrix(self):
        if self.data is None:
            messagebox.showerror("Error", "Please load data first.")
            return

        numeric_data = self.data.select_dtypes(include=['float64', 'int64'])
        correlation_matrix = numeric_data.corr()

        # Plotting correlation matrix using seaborn heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title('Correlation Matrix')
        plt.tight_layout()

        # Clear previous plot if exists
        if self.correlation_plot:
            self.correlation_plot.destroy()

        self.correlation_plot = FigureCanvasTkAgg(plt.gcf(), master=self.right_pane)
        self.correlation_plot.draw()
        self.correlation_plot.get_tk_widget().pack(fill='both', expand=True)

    def show_statistical_summary(self):
        if self.data is None:
            messagebox.showerror("Error", "Please load data first.")
            return

        summary = self.data.describe().transpose()

        # Clear previous text area if exists
        for widget in self.right_pane.winfo_children():
            widget.destroy()

        summary_label = Label(self.right_pane, text="Statistical Summary", font=("Helvetica", 16, "bold"))
        summary_label.pack(pady=10)

        text_area = Text(self.right_pane, wrap=WORD, height=10, width=60)
        text_area.insert(INSERT, summary.to_string())
        text_area.pack(fill='both', expand=True)

    def calculate_time_complexity(self):
        sizes = [10, 100, 1000, 10000]
        times = []

        for size in sizes:
            start_time = time.time()

            # Replace with your algorithm or operation
            _ = [n * 2 for n in range(size)]

            end_time = time.time()
            elapsed_time = end_time - start_time
            times.append(elapsed_time)

        plt.figure(figsize=(8, 6))
        plt.plot(sizes, times, marker='o', linestyle='-', color='b')
        plt.xlabel('Input Size')
        plt.ylabel('Time (seconds)')
        plt.title('Time Complexity')
        plt.grid(True)
        plt.tight_layout()

        # Clear previous plot if exists
        if self.time_plot:
            self.time_plot.destroy()

        self.time_plot = FigureCanvasTkAgg(plt.gcf(), master=self.right_pane)
        self.time_plot.draw()
        self.time_plot.get_tk_widget().pack(fill='both', expand=True)

    def calculate_space_complexity(self):
        sizes = [10, 100, 1000, 10000]
        space = []

        for size in sizes:
            # Replace with your algorithm or operation
            # Example: space required to store a list of size `size`
            space_required = size * 4  # Assuming each element takes 4 bytes

            space.append(space_required)

        plt.figure(figsize=(8, 6))
        plt.plot(sizes, space, marker='o', linestyle='-', color='g')
        plt.xlabel('Input Size')
        plt.ylabel('Space (bytes)')
        plt.title('Space Complexity')
        plt.grid(True)
        plt.tight_layout()

        # Clear previous plot if exists
        if self.space_plot:
            self.space_plot.destroy()

        self.space_plot = FigureCanvasTkAgg(plt.gcf(), master=self.right_pane)
        self.space_plot.draw()
        self.space_plot.get_tk_widget().pack(fill='both', expand=True)

if __name__ == "__main__":
    root = Tk()
    app = DataVisualizer(root)
    root.mainloop()

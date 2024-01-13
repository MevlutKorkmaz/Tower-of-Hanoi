import tkinter as tk
import time # Used to handle time-related tasks.
import threading # Allows for the creation of threads and enables the application to run long-running tasks

class TowerOfHanoi:
    def __init__(self, master):
        self.master = master # main window
        self.master.title("Tower of Hanoi")
        self.master.configure(bg='#ADD8E6')
        self.num_disks = tk.IntVar(value=3)    # Default number of disks
        self.recursive_var = tk.BooleanVar()
        self.iterative_var = tk.BooleanVar()
        self.movements = []
        self.stop_flag = False  # Flag to stop the algorithm
        self.start_time = 0
        self.positions = {'A': [], 'B': [], 'C': []}
        self.create_widgets()   # Create the widgets
        self.runtimes = []  # List to store runtimes

    def create_widgets(self):   # Create the widgets for the GUI and place them in the window
        self.recursive_checkbox = tk.Checkbutton(self.master, text="Recursive", variable=self.recursive_var, onvalue=True, offvalue=False, bg='#87CEEB')
        self.recursive_checkbox.grid(row=0, column=0, padx=10, pady=10)
        self.iterative_checkbox = tk.Checkbutton(self.master, text="Iterative", variable=self.iterative_var, onvalue=True, offvalue=False, bg='#87CEEB')
        self.iterative_checkbox.grid(row=0, column=1, padx=10, pady=10)
        self.disks_entry_label = tk.Label(self.master, text="Number of Disks:", bg='#ADD8E6')
        self.disks_entry_label.grid(row=1, column=0, padx=10, pady=10)
        self.disks_entry = tk.Entry(self.master, textvariable=self.num_disks)
        self.disks_entry.grid(row=1, column=1, padx=10, pady=10)
        self.run_button = tk.Button(self.master, text="Run Algorithm", command=self.run_algorithm, bg='#90EE90')
        self.run_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.output_box = tk.Text(self.master, height=10, width=50)
        self.output_box.grid(row=3, column=0, columnspan=2, pady=10)
        self.stop_button = tk.Button(self.master, text="Stop Algorithm", command=self.stop_algorithm, state=tk.DISABLED, bg='#FF6347')
        self.stop_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.runtime_label = tk.Label(self.master, text="Runtime:", bg='#ADD8E6')
        self.runtime_label.grid(row=5, column=0, padx=10, pady=10)
        self.total_movements_label = tk.Label(self.master, text="Total Movements:", bg='#ADD8E6')
        self.total_movements_label.grid(row=6, column=0, padx=10, pady=10)
        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset, bg='#FFD700')
        self.reset_button.grid(row=7, column=0, columnspan=2, pady=10)
        self.canvas = tk.Canvas(self.master, width=640, height=320, bg='white')
        self.canvas.grid(row=8, column=0, columnspan=2, pady=10)
        # Add a runtime display box
        self.runtime_display_label = tk.Label(self.master, text="Previous Runtimes:", bg='#ADD8E6')
        self.runtime_display_label.grid(row=9, column=0, padx=10, pady=10)
        self.runtime_display = tk.Text(self.master, height=5, width=30)
        self.runtime_display.grid(row=10, column=0, columnspan=2, pady=10)
        self.reset_runtimes_button = tk.Button(self.master, text="Reset Runtimes", command=self.reset_runtimes, bg='#FFD700')
        self.reset_runtimes_button.grid(row=7, column=1, columnspan=2, pady=10)

    def run_algorithm(self):   # starts either the recursive or iterative algorithm in a separate thread
        self.movements = []
        num_disks = self.num_disks.get()
        self.stop_flag = False
        self.start_time = time.time()
        self.positions = {'A': list(range(num_disks, 0, -1)), 'B': [], 'C': []}
        self.output_box.delete(1.0, tk.END)
        self.draw_towers()

        if self.recursive_var.get():
            threading.Thread(target=self.move_recursive, args=(num_disks, 'A', 'C', 'B')).start()
        if self.iterative_var.get():
            threading.Thread(target=self.move_iterative, args=(num_disks, 'A', 'C', 'B')).start()

    def move_recursive(self, n, source, target, auxiliary):    # prepares for the running of recursive algorithm and updates GUI
        self.stop_button.config(state=tk.NORMAL)
        self._move_recursive(n, source, target, auxiliary)
        self.stop_button.config(state=tk.DISABLED)

        elapsed_time = time.time() - self.start_time
        self.runtime_label.config(text=f"Runtime: {elapsed_time:.2f} seconds")
        self.total_movements_label.config(text=f"Total Movements: {len(self.movements)}")
        self.runtimes.append(elapsed_time)   # Append runtime
        self.update_runtime_display()   # Update runtime display

    def _move_recursive(self, n, source, target, auxiliary):  # Moves disks recursively
        if n > 0 and not self.stop_flag:
            self._move_recursive(n - 1, source, auxiliary, target)
            disk = self.positions[source].pop()
            self.positions[target].append(disk)
            self.movements.append(f"Move disk {disk} from {source} to {target}")
            self.update_movements()
            self.master.after(0, self.draw_towers)
            self._move_recursive(n - 1, auxiliary, target, source)

    def move_iterative(self, n, source, target, auxiliary):  # prepares for the running of iterative algorithm and updates GUI
        self.stop_button.config(state=tk.NORMAL)
        self._move_iterative(n, source, target, auxiliary)
        self.stop_button.config(state=tk.DISABLED)

        elapsed_time = time.time() - self.start_time
        self.runtime_label.config(text=f"Runtime: {elapsed_time:.2f} seconds")
        self.total_movements_label.config(text=f"Total Movements: {len(self.movements)}")
        self.runtimes.append(elapsed_time)   # Append runtime
        self.update_runtime_display()   # Update runtime display

    def _move_iterative(self, n, source, target, auxiliary):  # Moves disks iteratively
        s, t, a = source, target, auxiliary
        total_moves = 2**n - 1
        for i in range(1, total_moves + 1):
            if self.stop_flag:
                break

            if i % 3 == 1:
                self.move_disk(s, t)
            elif i % 3 == 2:
                self.move_disk(s, a)
            else:
                self.move_disk(a, t)
            self.update_movements()
            self.master.after(0, self.draw_towers)

    def move_disk(self, from_peg, to_peg):  # Moves a disk from one peg to another
        if not self.positions[from_peg]:
            disk = self.positions[to_peg].pop()
            self.positions[from_peg].append(disk)
            move = f"Move disk {disk} from {to_peg} to {from_peg}"
        elif not self.positions[to_peg] or self.positions[from_peg][-1] < self.positions[to_peg][-1]:
            disk = self.positions[from_peg].pop()
            self.positions[to_peg].append(disk)
            move = f"Move disk {disk} from {from_peg} to {to_peg}"
        else:
            disk = self.positions[to_peg].pop()
            self.positions[from_peg].append(disk)
            move = f"Move disk {disk} from {to_peg} to {from_peg}"
        self.movements.append(move)

    def draw_towers(self):  # Draws the current state of towers and disks
        self.canvas.delete("all")
        canvas_width = 640
        canvas_height = 320
        tower_width = 20
        disk_height = 20
        base_height = canvas_height - 10
        tower_spacing = canvas_width // 4
        max_disk_width = 200
        num_disks = self.num_disks.get()

        for i in range(3):
            x = tower_spacing * (i + 1)
            self.canvas.create_rectangle(x - tower_width // 2, 20, x + tower_width // 2, base_height, fill="gray")

        for i, tower in enumerate(['A', 'B', 'C']):
            x = tower_spacing * (i + 1)
            for j, disk in enumerate(self.positions[tower]):
                disk_width = (disk / num_disks) * max_disk_width  # Calculate disk width based on its size
                y = base_height - disk_height * (j + 1)
                self.canvas.create_rectangle(x - disk_width // 2, y, x + disk_width // 2, y + disk_height, fill="blue")

    def update_movements(self):  # Updates the output box with the current list of movements
        def update_text():
            self.output_box.delete(1.0, tk.END)
            for move in self.movements:
                self.output_box.insert(tk.END, move + '\n')

        self.master.after(0, update_text)

    def update_runtime_display(self):  # Updates the runtime display box with the current list of runtimes
        self.runtime_display.delete(1.0, tk.END)
        for idx, runtime in enumerate(self.runtimes, 1):
            self.runtime_display.insert(tk.END, f"Run {idx}: {runtime:.2f} seconds\n")

    def stop_algorithm(self):  # Stops the algorithm
        self.stop_flag = True

    def reset(self):  # Resets the GUI to its initial state
        self.output_box.delete(1.0, tk.END)
        self.num_disks.set(3)
        self.recursive_var.set(False)
        self.iterative_var.set(False)
        self.runtime_label.config(text="Runtime:")
        self.total_movements_label.config(text="Total Movements:")
        self.positions = {'A': [], 'B': [], 'C': []}
        self.canvas.delete("all")

    def reset_runtimes(self):  # Resets the runtime display box
        self.runtimes.clear()
        self.update_runtime_display()

if __name__ == "__main__":   # Create the main window and run the application
    root = tk.Tk()
    app = TowerOfHanoi(root)
    root.mainloop()

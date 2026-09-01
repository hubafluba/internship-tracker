import tkinter as tk
from tkinter import ttk, messagebox
import database

COLUMNS = ("id", "company", "role", "date_applied", "status", "link")
FIELDS = ("company", "role", "date_applied", "link")
STATUSES = ("Applied", "OA", "Interview", "Offer", "Rejected")


class TrackerApp:
    """Tkinter window for viewing and editing internship applications."""

    def __init__(self, conn):
        self.conn = conn
        self.root = tk.Tk()
        self.root.title("Internship Tracker")
        self.root.geometry("1220x600")

        style = ttk.Style()
        try:
            style.theme_use("aqua")
        except tk.TclError:
            style.theme_use("clam")

        self._build_table()
        self._build_form()
        self.refresh()

    def _build_table(self):
        self.tree = ttk.Treeview(self.root, columns=COLUMNS, show="headings")
        for col in COLUMNS:
            self.tree.heading(col, text=col.replace("_", " ").title())
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("company", width=180)
        self.tree.column("role", width=200)
        self.tree.column("date_applied", width=100, anchor="center")
        self.tree.column("status", width=90, anchor="center")
        self.tree.column("link", width=180)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.tag_configure("odd", background="#f7f7f7")

    def _build_form(self):
        form = ttk.Frame(self.root)
        form.pack(fill="x", padx=10, pady=(0, 10))

        self.entries = {}
        for i, field in enumerate(FIELDS):
            ttk.Label(form, text=field.replace("_", " ").title()).grid(row=0, column=i, sticky="w")
            entry = ttk.Entry(form, width=18)
            entry.grid(row=1, column=i, padx=(0, 8))
            self.entries[field] = entry

        self.status = ttk.Combobox(form, values=STATUSES, width=12, state="readonly")
        self.status.set("Applied")
        ttk.Label(form, text="Status").grid(row=0, column=len(FIELDS), sticky="w")
        self.status.grid(row=1, column=len(FIELDS), padx=(0, 8))

        ttk.Button(form, text="Add", command=self.handle_add).grid(row=1, column=len(FIELDS) + 1)
        ttk.Button(form, text="Update Status", command=self.handle_update).grid(row=1, column=len(FIELDS) + 2)
        ttk.Button(form, text="Delete", command=self.handle_delete).grid(row=1, column=len(FIELDS) + 3)

    def refresh(self):
        """Clear the table and reload every application from the database."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for i, app in enumerate(database.get_all(self.conn)):
            tag = "odd" if i % 2 else "even"
            self.tree.insert("", "end", values=[app[c] for c in COLUMNS], tags=(tag,))

    def selected_id(self):
        """Return the id of the selected row, or None if nothing is selected."""
        selection = self.tree.selection()
        if not selection:
            return None
        return self.tree.item(selection[0])["values"][0]

    def handle_add(self):
        database.add_application(
            self.conn,
            self.entries["company"].get(),
            self.entries["role"].get(),
            self.entries["date_applied"].get(),
            self.status.get(),
            self.entries["link"].get(),
            None,
        )
        self.refresh()
        for entry in self.entries.values():
            entry.delete(0, "end")

    def handle_update(self):
        app_id = self.selected_id()
        if app_id is None:
            return
        database.update_status(self.conn, app_id, self.status.get())
        self.refresh()

    def handle_delete(self):
        app_id = self.selected_id()
        if app_id is None:
            return
        if messagebox.askyesno("Delete", "Delete this application?"):
            database.delete_application(self.conn, app_id)
            self.refresh()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    conn = database.init_db()
    TrackerApp(conn).run()
    
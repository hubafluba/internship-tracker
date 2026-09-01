import tkinter as tk
from tkinter import ttk
import database
from tkinter import messagebox

COLUMNS = ("id", "company", "role", "date_applied", "status", "link")

def build_window(conn):
    root = tk.Tk()
    root.title("Internship Tracker")
    root.geometry("1220x600")
    style = ttk.Style()
    try:
        style.theme_use("aqua")
    except tk.TclError:
        style.theme_use("clam")

    tree = ttk.Treeview(root, columns=COLUMNS, show="headings")
    for col in COLUMNS:
        tree.heading(col, text=col.replace("_", " ").title())
    tree.column("id", width=40, anchor="center")
    tree.column("company", width=180)
    tree.column("role", width=200)
    tree.column("date_applied", width=100, anchor="center")
    tree.column("status", width=90, anchor="center")
    tree.column("link", width=180)

    tree.pack(fill="both", expand=True, padx=10, pady=10)
    tree.tag_configure("odd", background="#f7f7f7")

    form = ttk.Frame(root)
    form.pack(fill="x", padx=10, pady=(0, 10))

    def handle_add():
        database.add_application(
            conn,
            entries["company"].get(),
            entries["role"].get(),
            entries["date_applied"].get(),
            status.get(),
            entries["link"].get(),
            None,
        )
        refresh(tree, conn)
        for e in entries.values():
            e.delete(0, "end")

    def handle_delete():
        app_id = selected_id(tree)
        if app_id is None:
            return
        if messagebox.askyesno("Delete", "Delete this application?"):
            database.delete_application(conn, app_id)
            refresh(tree, conn)

    def handle_update():
        app_id = selected_id(tree)
        if app_id is None:
            return
        database.update_status(conn, app_id, status.get())
        refresh(tree, conn)

    entries = {}
    fields = ("company", "role", "date_applied", "link")
    for i, field in enumerate(fields):
        ttk.Label(form, text=field.replace("_", " ").title()).grid(row=0, column=i, sticky="w")
        entry = ttk.Entry(form, width=18)
        entry.grid(row=1, column=i, padx=(0, 8))
        entries[field] = entry

    status = ttk.Combobox(form, values=["Applied", "OA", "Interview", "Offer", "Rejected"],
                          width=12, state="readonly")
    status.set("Applied")
    ttk.Label(form, text="Status").grid(row=0, column=len(fields), sticky="w")
    status.grid(row=1, column=len(fields), padx=(0, 8))

    add_btn = ttk.Button(form, text="Add", command=handle_add)
    update_btn = ttk.Button(form, text="Update Status", command=handle_update)
    delete_btn = ttk.Button(form, text="Delete", command=handle_delete)
    add_btn.grid(row=1, column=len(fields) + 1)
    update_btn.grid(row=1, column=len(fields) + 2)
    delete_btn.grid(row=1, column=len(fields) + 3)
    return root, tree

def refresh(tree, conn):
    """Clear the table and reload every application from the database."""
    for row in tree.get_children():
        tree.delete(row)
    for i, app in enumerate(database.get_all(conn)):
        tag = "odd" if i % 2 else "even"
        tree.insert("", "end", values=[app[c] for c in COLUMNS], tags=(tag,))

def selected_id(tree):
    """Return the id of the selected row, or None if nothing is selected."""
    selection = tree.selection()
    if not selection:
        return None
    return tree.item(selection[0])["values"][0]

if __name__ == "__main__":
    conn = database.init_db()
    root, tree = build_window(conn)
    refresh(tree, conn)
    root.mainloop()
from tkinter import BOTH, END, messagebox, StringVar
from tkinter.ttk import Frame, Button, Label, Entry, Style, Combobox
from decimal import Decimal, InvalidOperation
import json
import csv
import os

class MyFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.history = []  # in-memory calculation history
        self.history_file = os.path.join(os.path.dirname(__file__), "loan_history.json")

    def initUI(self):
        self.parent.title("Loan Calculator")
        self.style = Style()
        self.style.theme_use("default")  # default
        self.pack(fill=BOTH, expand=1)

        xpos = 30
        ypos = 25
        xpos2 = xpos + 140

        # Styles
        style = Style()
        style.configure("Exit.TButton", foreground="red", background="white")
        style.configure("MainButton.TButton", foreground="yellow", background="red")

        Label(self, text="Amount", foreground="#ff0000", background="light blue", font="Arial 9").place(x=xpos, y=ypos)
        self.txtAmount = Entry(self)
        self.txtAmount.place(x=xpos2, y=ypos, width=170)

        ypos += 35
        Label(self, text="Rate (%)", foreground="#ff0000", background="light blue", font="Arial 9").place(x=xpos, y=ypos)
        self.txtRate = Entry(self)
        self.txtRate.place(x=xpos2, y=ypos, width=170)

        ypos += 35
        Label(self, text="Duration (months)", foreground="#ff0000", background="light blue", font="Arial 9").place(x=xpos, y=ypos)
        self.txtDuration = Entry(self)
        self.txtDuration.place(x=xpos2, y=ypos, width=170)

        # Currency dropdown
        ypos += 35
        Label(self, text="Currency", foreground="#333333", background="light blue", font="Arial 9").place(x=xpos, y=ypos)
        self.currency_var = StringVar(value="USD")
        self.ddCurrency = Combobox(self, textvariable=self.currency_var, values=["USD", "EUR", "GBP"], state="readonly")
        self.ddCurrency.place(x=xpos2, y=ypos, width=170)

        ypos += 35
        Label(self, text="Monthly Payment", foreground="#ff0000", background="yellow", font="Arial 9").place(x=xpos, y=ypos)
        self.txtMonthlyPayment = Entry(self, state="readonly")
        self.txtMonthlyPayment.place(x=xpos2, y=ypos, width=170)

        ypos += 35
        Label(self, text="Total Payment", foreground="#ff0000", background="yellow", font="Arial 9").place(x=xpos, y=ypos)
        self.txtTotalPayment = Entry(self, state="readonly")
        self.txtTotalPayment.place(x=xpos2, y=ypos, width=170)

        # Buttons row
        ypos += 40
        btnCalc = Button(self, text="Calculate", command=self.calcButtonClick)
        btnCalc.configure(style="MainButton.TButton")
        btnCalc.place(x=xpos, y=ypos)

        btnClear = Button(self, text="Clear", command=self.clearFields)
        btnClear.place(x=xpos + 110, y=ypos)

        btnExit = Button(self, text="Exit", command=self.exitButtonClick)
        btnExit.configure(style="Exit.TButton")
        btnExit.place(x=xpos + 180, y=ypos)

        # Save/Load/Export row
        ypos += 40
        btnSave = Button(self, text="Save", command=self.saveHistory)
        btnSave.place(x=xpos, y=ypos)

        btnLoad = Button(self, text="Load", command=self.loadHistory)
        btnLoad.place(x=xpos + 70, y=ypos)

        btnExport = Button(self, text="Export CSV", command=self.exportCSV)
        btnExport.place(x=xpos + 140, y=ypos)

        # History display
        ypos += 40
        Label(self, text="History (last calc)", background="light blue", font="Arial 9").place(x=xpos, y=ypos)
        self.txtHistory = Entry(self, state="readonly")
        self.txtHistory.place(x=xpos + 140, y=ypos, width=170)

    def exitButtonClick(self):
        if messagebox.askokcancel("OK to close?", "Close application?"):
            self.parent.destroy()
            raise SystemExit

    def _get_decimal(self, widget, label):
        raw = widget.get().strip()
        try:
            value = Decimal(raw)
            return value
        except (InvalidOperation, ValueError):
            messagebox.showerror("Invalid Input", f"Please enter a valid number for {label}.")
            widget.focus_set()
            return None

    def calcButtonClick(self):
        amount = self._get_decimal(self.txtAmount, "Amount")
        rate_percent = self._get_decimal(self.txtRate, "Rate (%)")
        duration_months = self._get_decimal(self.txtDuration, "Duration (months)")

        if amount is None or rate_percent is None or duration_months is None:
            return

        if amount <= 0 or duration_months <= 0:
            messagebox.showerror("Invalid Input", "Amount and Duration must be positive.")
            return
        if rate_percent < 0:
            messagebox.showerror("Invalid Input", "Rate cannot be negative.")
            return

        r = (rate_percent / Decimal(100)) / Decimal(12)  # monthly rate
        n = int(duration_months)

        if r == 0:
            monthly_payment = amount / n
        else:
            # M = P * r * (1 + r)^n / ((1 + r)^n - 1)
            factor = (Decimal(1) + r) ** n
            monthly_payment = amount * r * factor / (factor - Decimal(1))

        total_payment = monthly_payment * n
        currency = self.currency_var.get()

        self._set_readonly(self.txtMonthlyPayment, f"{currency} {monthly_payment:.2f}")
        self._set_readonly(self.txtTotalPayment, f"{currency} {total_payment:.2f}")

        hist_item = {
            "amount": f"{amount}",
            "rate_percent": f"{rate_percent}",
            "duration_months": n,
            "monthly_payment": f"{monthly_payment:.2f}",
            "total_payment": f"{total_payment:.2f}",
            "currency": currency,
        }
        self.history.append(hist_item)
        self._set_readonly(self.txtHistory, f"{currency} M={hist_item['monthly_payment']} T={hist_item['total_payment']}")

    def clearFields(self):
        for w in [self.txtAmount, self.txtRate, self.txtDuration]:
            w.delete(0, END)
        self._set_readonly(self.txtMonthlyPayment, "")
        self._set_readonly(self.txtTotalPayment, "")
        self._set_readonly(self.txtHistory, "")

    def _set_readonly(self, widget, value):
        widget.configure(state="normal")
        widget.delete(0, END)
        widget.insert(0, value)
        widget.configure(state="readonly")

    def saveHistory(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2)
            messagebox.showinfo("Saved", f"History saved to {self.history_file}")
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to save: {ex}")

    def loadHistory(self):
        try:
            if not os.path.exists(self.history_file):
                messagebox.showinfo("No File", "No saved history file found yet.")
                return
            with open(self.history_file, "r", encoding="utf-8") as f:
                self.history = json.load(f)
            if self.history:
                last = self.history[-1]
                self._set_readonly(self.txtHistory, f"{last['currency']} M={last['monthly_payment']} T={last['total_payment']}")
                messagebox.showinfo("Loaded", f"Loaded {len(self.history)} history items.")
            else:
                messagebox.showinfo("Loaded", "History file was empty.")
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to load: {ex}")

    def exportCSV(self):
        csv_path = os.path.join(os.path.dirname(__file__), "loan_history.csv")
        try:
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["amount", "rate_percent", "duration_months", "monthly_payment", "total_payment", "currency"])
                writer.writeheader()
                for item in self.history:
                    writer.writerow(item)
            messagebox.showinfo("Exported", f"CSV exported to {csv_path}")
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to export: {ex}")
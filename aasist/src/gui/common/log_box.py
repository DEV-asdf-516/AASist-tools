from queue import Empty
import customtkinter as ctk
from aasist.src.gui.handler import QueueHandler


class LogBox(ctk.CTkFrame):
    MAX_LOG_LINE = 1000

    def __init__(
        self,
        parent: ctk.CTkFrame,
        log_queue: QueueHandler,
        width: int = 600,
        bg_color: str = "#F2F2F2",
    ):
        super().__init__(parent, bg_color=bg_color)
        self.log_line = 0
        self.log_queue = log_queue

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.output_box = ctk.CTkTextbox(
            self,
            state=ctk.DISABLED,
            width=width,
            font=ctk.CTkFont(size=16),
        )
        self.output_box.grid(row=0, column=0, sticky=ctk.NSEW)

        self.after(100, self._monitoring_logs)

    def _monitoring_logs(self):
        while True:
            try:
                if self.log_line > self.MAX_LOG_LINE:
                    self._remove_old_logs()

                log_message, log_level = self.log_queue.get()
                if not self.output_box:
                    return
                self.output_box.configure(state=ctk.NORMAL)
                start_index = self.output_box.index(f"{ctk.END}-1c")
                self.output_box.insert(ctk.END, log_message + "\n")
                last_index = self.output_box.index(f"{ctk.END}-1c")
                tag_name = f"{self.log_line}{log_level.name}"
                self.output_box.tag_add(tag_name, start_index, last_index)
                self.output_box.tag_config(tag_name, foreground=log_level.color)
                self.output_box.see(ctk.END)
                self.output_box.configure(state=ctk.DISABLED)
                self.log_line += 1
            except Empty:
                break

        self.after(100, self._monitoring_logs)

    def _remove_old_logs(self):
        old_lines = self.MAX_LOG_LINE // 4
        self.output_box.configure(state=ctk.NORMAL)
        for _ in range(old_lines):
            self.output_box.delete("1.0", "2.0")
        self.output_box.configure(state=ctk.DISABLED)

        self.log_line -= old_lines

    def clear(self):
        self.output_box.configure(state=ctk.NORMAL)
        self.output_box.delete("1.0", ctk.END)
        self.output_box.configure(state=ctk.DISABLED)
        self.current_lines = 0

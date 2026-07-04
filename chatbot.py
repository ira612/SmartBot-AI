# ============================================================
# SMARTBOT AI  
# DecodeLabs AI Internship - Project 1
# Rule-Based AI Chatbot using Tkinter
# ============================================================

import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# -----------------------------
# Palette
# -----------------------------
BG_COLOR      = "#EEF1F8"
HEADER_L      = "#5B4CFF"
HEADER_R      = "#3323C7"
CHAT_BG       = "#FFFFFF"
USER_BUBBLE   = "#4A3AFF"
USER_TEXT     = "#FFFFFF"
BOT_BUBBLE    = "#F1F3F9"
BOT_TEXT      = "#1E1E2E"
SHADOW_CLR    = "#DCE0EE"
TIMESTAMP_CLR = "#9AA0B4"
AVATAR_USER   = "#372CBF"
AVATAR_BOT    = "#2ED47A"
BUTTON2       = "#FF9F43"; BUTTON2_HOVER = "#E8890F"
BUTTON3       = "#FF5C5C"; BUTTON3_HOVER = "#E64545"
GREEN         = "#2ED47A"; GREEN_HOVER   = "#25B368"
PURPLE        = "#8C6EFF"; PURPLE_HOVER  = "#7457E6"
SEND_CLR      = "#4A3AFF"; SEND_HOVER    = "#372CBF"
STATUS_BG     = "#372CBF"

FONT_MAIN  = ("Calibri", 12)
FONT_BOLD  = ("Calibri", 12, "bold")
FONT_TITLE = ("Segoe UI", 19, "bold")
FONT_SMALL = ("Segoe UI", 9)
FONT_BTN   = ("Segoe UI", 10, "bold")

CANVAS_WIDTH   = 900
BUBBLE_MAXTXT  = 460   # max text wrap width inside a bubble
MARGIN         = 60    # room reserved for avatar on each side
PAD_X, PAD_Y   = 14, 10


def current_time():
    return datetime.now().strftime("%I:%M %p")


# ============================================================
# CHATBOT LOGIC — If-Else Control Flow
# (Per requirement: "Use if-else logic for responses")
# ============================================================

def get_response(user):
    user = user.lower().strip()

    if user in ["hi", "hello", "hey"]:
        return "Hello! 👋 Welcome to SmartBot."
    elif user == "good morning":
        return "Good Morning! ☀️"
    elif user == "good afternoon":
        return "Good Afternoon! 😊"
    elif user == "good evening":
        return "Good Evening! 🌇"
    elif user in ["assalam o alaikum", "salam"]:
        return "Walaikum Assalam! 😊"
    elif user == "how are you":
        return "I'm doing great. Thanks for asking."
    elif user == "your name":
        return "My name is SmartBot."
    elif user == "who made you":
        return "I was created for DecodeLabs AI Internship by Dua"
    elif user == "what can you do":
        return ("I can answer predefined questions, "
                "tell date and time and explain AI concepts.")
    elif user == "what is ai":
        return ("Artificial Intelligence enables machines to perform "
                "tasks that normally require human intelligence.")
    elif user == "what is python":
        return ("Python is a popular programming language used for "
                "AI, Data Science and Web Development.")
    elif user == "what is chatbot":
        return "A chatbot is software that communicates with users using predefined rules."
    elif user == "what is programming":
        return "Programming means writing instructions for a computer."
    elif user == "date":
        return "Today's Date : " + datetime.now().strftime("%d-%m-%Y")
    elif user == "time":
        return "Current Time : " + datetime.now().strftime("%I:%M:%S %p")
    elif user == "day":
        return datetime.now().strftime("Today is %A")
    elif user == "month":
        return datetime.now().strftime("Current Month : %B")
    elif user == "year":
        return datetime.now().strftime("Current Year : %Y")
    elif user in ["thanks", "thank you"]:
        return "You're Welcome! 😊"
    elif user == "nice":
        return "Thank you!"
    elif user == "awesome":
        return "I'm happy you liked it."
    elif user == "help":
        return ("Commands:\n\nHi\nHello\nHow are you\nYour name\nWho made you\n"
                "What is AI\nWhat is Python\nWhat is Chatbot\nWhat is Programming\n"
                "Date\nTime\nDay\nMonth\nYear\nThanks\nBye")
    elif user in ["bye", "exit", "quit"]:
        return "Goodbye! 👋 Have a wonderful day."
    else:
        return "Sorry, I don't understand that.\nType 'help' to see available commands."


# ============================================================
# ROOT WINDOW
# ============================================================

root = tk.Tk()
root.title("SmartBot AI | DecodeLabs Internship Project")
root.geometry("960x820")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

state = {"y": 20, "typing_ids": None, "typing_job": None, "dots": 1}


# ============================================================
# HEADER (gradient via thin vertical strips)
# ============================================================

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb


def lerp_color(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex((int(r1 + (r2 - r1) * t),
                        int(g1 + (g2 - g1) * t),
                        int(b1 + (b2 - b1) * t)))


header = tk.Canvas(root, width=960, height=78, highlightthickness=0, bd=0)
header.pack(fill=tk.X)

STRIPS = 96
for i in range(STRIPS):
    t = i / STRIPS
    color = lerp_color(HEADER_L, HEADER_R, t)
    x = i * (960 / STRIPS)
    header.create_rectangle(x, 0, x + (960 / STRIPS) + 1, 78, fill=color, outline=color)

header.create_text(52, 39, text="🤖", font=("Segoe UI Emoji", 26), fill="white")
header.create_text(90, 26, text="SmartBot AI", font=FONT_TITLE, fill="white", anchor="w")
header.create_text(90, 52, text="Rule-Based Chatbot · DecodeLabs Internship",
                    font=FONT_SMALL, fill="#E4E0FF", anchor="w")

clock_text = header.create_text(910, 39, text="", font=FONT_BOLD, fill="white", anchor="e")


def update_clock():
    header.itemconfig(clock_text, text=datetime.now().strftime("%I:%M:%S %p"))
    root.after(1000, update_clock)


# ============================================================
# CHAT CANVAS (scrollable, rounded bubbles)
# ============================================================

chat_frame = tk.Frame(root, bg=BG_COLOR)
chat_frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=(14, 8))

chat_canvas = tk.Canvas(chat_frame, bg=CHAT_BG, width=CANVAS_WIDTH, highlightthickness=0)
scrollbar = tk.Scrollbar(chat_frame, orient="vertical", command=chat_canvas.yview)
chat_canvas.configure(yscrollcommand=scrollbar.set)

chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


def on_mousewheel(event):
    chat_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


chat_canvas.bind_all("<MouseWheel>", on_mousewheel)


def rounded_rect(canvas, x1, y1, x2, y2, radius=16, **kwargs):
    points = [
        x1 + radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
        x2, y2 - radius, x2, y2, x2 - radius, y2, x1 + radius, y2,
        x1, y2, x1, y2 - radius, x1, y1 + radius, x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def add_message(sender, text, timestamp, is_user):
    y = state["y"]

    text_id = chat_canvas.create_text(
        0, y + PAD_Y, text=text, font=FONT_MAIN if not is_user else FONT_BOLD,
        width=BUBBLE_MAXTXT, anchor="nw",
        fill=(USER_TEXT if is_user else BOT_TEXT)
    )
    x1, y1, x2, y2 = chat_canvas.bbox(text_id)
    text_w, text_h = x2 - x1, y2 - y1

    bubble_w = text_w + 2 * PAD_X
    bubble_h = text_h + 2 * PAD_Y

    if is_user:
        bx2 = CANVAS_WIDTH - MARGIN
        bx1 = bx2 - bubble_w
    else:
        bx1 = MARGIN
        bx2 = bx1 + bubble_w

    by1, by2 = y, y + bubble_h

    chat_canvas.coords(text_id, bx1 + PAD_X, by1 + PAD_Y)

    # drop shadow
    shadow_id = rounded_rect(chat_canvas, bx1 + 2, by1 + 3, bx2 + 2, by2 + 3,
                              radius=16, fill=SHADOW_CLR, outline="")
    # bubble
    rect_id = rounded_rect(chat_canvas, bx1, by1, bx2, by2, radius=16,
                            fill=(USER_BUBBLE if is_user else BOT_BUBBLE), outline="")
    chat_canvas.tag_lower(shadow_id)
    chat_canvas.tag_raise(rect_id, shadow_id)
    chat_canvas.tag_raise(text_id, rect_id)

    # avatar
    r = 15
    acx = (bx2 + 26) if is_user else (bx1 - 26)
    acy = by1 + bubble_h / 2
    chat_canvas.create_oval(acx - r, acy - r, acx + r, acy + r,
                             fill=(AVATAR_USER if is_user else AVATAR_BOT), outline="")
    chat_canvas.create_text(acx, acy, text=("🧑" if is_user else "🤖"),
                             font=("Segoe UI Emoji", 13))

    # timestamp
    ts_y = by2 + 3
    ts_anchor = "ne" if is_user else "nw"
    ts_x = bx2 if is_user else bx1
    chat_canvas.create_text(ts_x, ts_y, text=f"{sender} · {timestamp}",
                             anchor=ts_anchor, font=FONT_SMALL, fill=TIMESTAMP_CLR)

    state["y"] = ts_y + 26
    chat_canvas.configure(scrollregion=(0, 0, CANVAS_WIDTH, state["y"] + 20))
    chat_canvas.yview_moveto(1.0)


def show_typing():
    y = state["y"]
    bubble_w, bubble_h = 90, 40
    bx1, bx2 = MARGIN, MARGIN + bubble_w
    by1, by2 = y, y + bubble_h

    shadow_id = rounded_rect(chat_canvas, bx1 + 2, by1 + 3, bx2 + 2, by2 + 3,
                              radius=18, fill=SHADOW_CLR, outline="")
    rect_id = rounded_rect(chat_canvas, bx1, by1, bx2, by2, radius=18,
                            fill=BOT_BUBBLE, outline="")
    text_id = chat_canvas.create_text((bx1 + bx2) / 2, (by1 + by2) / 2, text="•",
                                       font=("Segoe UI", 16, "bold"), fill=TIMESTAMP_CLR)

    r = 15
    acx, acy = bx1 - 26, (by1 + by2) / 2
    avatar_oval = chat_canvas.create_oval(acx - r, acy - r, acx + r, acy + r,
                                           fill=AVATAR_BOT, outline="")
    avatar_txt = chat_canvas.create_text(acx, acy, text="🤖", font=("Segoe UI Emoji", 13))

    state["typing_ids"] = (shadow_id, rect_id, text_id, avatar_oval, avatar_txt)
    state["dots"] = 1

    chat_canvas.configure(scrollregion=(0, 0, CANVAS_WIDTH, by2 + 20))
    chat_canvas.yview_moveto(1.0)

    def animate():
        if state["typing_ids"] is None:
            return
        dots = "•" * state["dots"] if state["dots"] <= 3 else "•"
        state["dots"] = state["dots"] + 1 if state["dots"] < 3 else 1
        chat_canvas.itemconfig(text_id, text=dots)
        state["typing_job"] = root.after(400, animate)

    animate()


def remove_typing():
    if state["typing_ids"]:
        for item_id in state["typing_ids"]:
            chat_canvas.delete(item_id)
        state["typing_ids"] = None
    if state["typing_job"]:
        root.after_cancel(state["typing_job"])
        state["typing_job"] = None


# Welcome message
add_message("SmartBot", "Welcome to SmartBot AI!\nType 'help' to see available commands.",
            current_time(), is_user=False)


# ============================================================
# SEND MESSAGE
# ============================================================

def send_message(event=None):
    user = entry.get().strip()
    if user == "" or user == PLACEHOLDER:
        return

    add_message("You", user, current_time(), is_user=True)

    entry.delete(0, tk.END)
    entry.insert(0, PLACEHOLDER)
    entry.config(fg="#9AA0B4")
    root.focus_set()
    status.config(text=f"Status : Last message at {current_time()}")

    show_typing()

    def respond():
        remove_typing()
        response = get_response(user)
        add_message("SmartBot", response, current_time(), is_user=False)
        if user.lower() in ["bye", "exit", "quit"]:
            root.after(1200, root.destroy)

    root.after(650, respond)


def clear_chat():
    chat_canvas.delete("all")
    state["y"] = 20
    state["typing_ids"] = None
    if state["typing_job"]:
        root.after_cancel(state["typing_job"])
        state["typing_job"] = None
    add_message("SmartBot", "Welcome to SmartBot AI!\nType 'help' to see all available commands.",
                current_time(), is_user=False)
    status.config(text="Status : Chat Cleared")


def show_help():
    messagebox.showinfo(
        "Help",
        """
Available Commands

Greetings
• Hi   • Hello   • Hey
• Good Morning / Afternoon / Evening

Questions
• How are you
• Your name
• Who made you
• What can you do

Learning
• What is AI
• What is Python
• What is Chatbot
• What is Programming

Utilities
• Date   • Time   • Day   • Month   • Year

Others
• Thanks   • Bye
"""
    )


def show_about():
    messagebox.showinfo(
        "About SmartBot",
        "SmartBot AI\n\nRule-Based AI Chatbot\n\n"
        "DecodeLabs AI Internship\nProject 1\n\n"
        "Developed using Python & Tkinter"
    )


def add_hover(button, normal_color, hover_color):
    button.bind("<Enter>", lambda e: button.config(bg=hover_color))
    button.bind("<Leave>", lambda e: button.config(bg=normal_color))


# ============================================================
# INPUT AREA (pill style)
# ============================================================

input_outer = tk.Frame(root, bg=BG_COLOR)
input_outer.pack(fill=tk.X, padx=18, pady=(0, 10))

input_pill = tk.Frame(input_outer, bg="white", highlightbackground="#D9DCEA", highlightthickness=1)
input_pill.pack(fill=tk.X, ipady=4)

PLACEHOLDER = "Type your message here..."

entry = tk.Entry(input_pill, font=("Calibri", 13), relief=tk.FLAT,
                  fg="#9AA0B4", highlightthickness=0, bd=0)
entry.insert(0, PLACEHOLDER)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(16, 8), ipady=8)


def clear_placeholder(event=None):
    if entry.get() == PLACEHOLDER:
        entry.delete(0, tk.END)
        entry.config(fg="#1E1E2E")


def add_placeholder(event=None):
    if entry.get().strip() == "":
        entry.delete(0, tk.END)
        entry.insert(0, PLACEHOLDER)
        entry.config(fg="#9AA0B4")


entry.bind("<FocusIn>", clear_placeholder)
entry.bind("<FocusOut>", add_placeholder)
entry.bind("<Return>", send_message)

send_btn = tk.Button(input_pill, text="➤  Send", bg=SEND_CLR, fg="white", font=FONT_BTN,
                      relief=tk.FLAT, width=10, command=send_message, cursor="hand2",
                      activebackground=SEND_HOVER, activeforeground="white")
send_btn.pack(side=tk.RIGHT, padx=(0, 10), pady=4)
add_hover(send_btn, SEND_CLR, SEND_HOVER)


# ============================================================
# ACTION BUTTONS
# ============================================================

button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=(0, 12))

btn_specs = [
    ("🗑  Clear Chat", BUTTON2, BUTTON2_HOVER, clear_chat),
    ("❓  Help", GREEN, GREEN_HOVER, show_help),
    ("ℹ️  About", PURPLE, PURPLE_HOVER, show_about),
    ("❌  Exit", BUTTON3, BUTTON3_HOVER, root.destroy),
]

for i, (text, color, hover, cmd) in enumerate(btn_specs):
    b = tk.Button(button_frame, text=text, bg=color, fg="white", font=FONT_BTN,
                  relief=tk.FLAT, width=15, height=1, command=cmd, cursor="hand2",
                  activebackground=hover, activeforeground="white")
    b.grid(row=0, column=i, padx=6)
    add_hover(b, color, hover)


# ============================================================
# STATUS BAR
# ============================================================

status = tk.Label(root, text="SmartBot AI | Rule-Based Chatbot | DecodeLabs AI Internship | Ready",
                   bg=STATUS_BG, fg="white", anchor="w", padx=14, pady=4, font=FONT_SMALL)
status.pack(side=tk.BOTTOM, fill=tk.X)

root.focus()
update_clock()
root.mainloop()
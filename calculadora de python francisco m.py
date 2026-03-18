import tkinter as tk

import tkinter as ttk
import tkinter.font as tkfont

# ── Janela principal ──────────────────────────────────────────────
root = ttk.Tk()
root.title("Calculadora")
root.resizable(True, True)
root.configure(bg="#0f0f0f")

# ── Cores e fontes ────────────────────────────────────────────────
BG         = "#0f0f0f"
CARD       = "#1a1a1a"
BORDER     = "#2a2a2a"
ACCENT     = "#f0c040"
TEXT_MAIN  = "#f5f5f5"
TEXT_SUB   = "#888888"
BTN_HOVER  = "#2e2b1f"
ERROR_CLR  = "#ff6b6b"

font_title  = ("Arial", 13, "bold")
font_label  = ("Courier New", 9)
font_input  = ("Courier New", 18, "bold")
font_btn    = ("Courier New", 16, "bold")
font_result = ("Courier New", 22, "bold")
font_small  = ("Courier New", 9)

# ── Funções ───────────────────────────────────────────────────────
def calcular(operacao):
    """Lê os dois valores e aplica a operação escolhida."""
    resultado_var.set("")
    resultado_label.config(fg=ACCENT)

    try:
        a = float(entry_a.get().replace(",", "."))
        b = float(entry_b.get().replace(",", "."))
    except ValueError:
        resultado_var.set("⚠  Insira números válidos")
        resultado_label.config(fg=ERROR_CLR)
        return

    try:
        if operacao == "+":
            res = a + b
        elif operacao == "−":
            res = a - b
        elif operacao == "×":
            res = a * b
        elif operacao == "**":
            res = a ** b
        elif operacao == "÷":
            if b == 0:
                resultado_var.set("Divisão por zero!")
                resultado_label.config(fg=ERROR_CLR)
                return
            res = a / b

        # Formata: inteiro se não tiver casas decimais
        if res == int(res) and abs(res) < 1e15:
            resultado_var.set(f"{int(res)}")
        else:
            resultado_var.set(f"{res:.10g}")

        operacao_label.config(
            text=f"{_fmt(a)}  {operacao}  {_fmt(b)}  =",
            fg=TEXT_SUB
        )

    except OverflowError:
        resultado_var.set("⚠  Número muito grande")
        resultado_label.config(fg=ERROR_CLR)

def _fmt(n):
    """Formata número para exibição na expressão."""
    if n == int(n) and abs(n) < 1e12:
        return str(int(n))
    return f"{n:.6g}"

def limpar():
    entry_a.delete(0, ttk.END)
    entry_b.delete(0, ttk.END)
    resultado_var.set("")
    operacao_label.config(text="")

# ── Hover nos botões ──────────────────────────────────────────────
def on_enter(btn, op):
    btn.config(bg=BTN_HOVER, fg=ACCENT)

def on_leave(btn, op):
    btn.config(bg=CARD, fg=TEXT_MAIN)

# ── Layout ────────────────────────────────────────────────────────
PAD = 28

# Título
header = ttk.Frame(root, bg=BG)
header.pack(fill="x", padx=PAD, pady=(PAD, 6))

ttk.Label(header, text="[ CALC ]", bg=BG, fg=ACCENT,
          font=font_title).pack(side="left")
ttk.Label(header, text="v1.0", bg=BG, fg=TEXT_SUB,
          font=font_small).pack(side="right", anchor="s", pady=2)

# Separador
ttk.Frame(root, bg=BORDER, height=1).pack(fill="x", padx=PAD)

# Card central
card = ttk.Frame(root, bg=CARD, bd=0, relief="flat")
card.pack(padx=PAD, pady=16, fill="both")

inner = ttk.Frame(card, bg=CARD)
inner.pack(padx=20, pady=20)

# Linha de inputs
row_inputs = ttk.Frame(inner, bg=CARD)
row_inputs.pack()

def make_input_block(parent, label_text):
    frame = ttk.Frame(parent, bg=CARD)
    ttk.Label(frame, text=label_text, bg=CARD, fg=TEXT_SUB,
              font=font_label).pack(anchor="w")
    e = ttk.Entry(frame, font=font_input, width=10,
                  bg="#111111", fg=TEXT_MAIN,
                  insertbackground=ACCENT,
                  relief="flat", bd=6,
                  justify="center",
                  highlightthickness=1,
                  highlightbackground=BORDER,
                  highlightcolor=ACCENT)
    e.pack()
    return frame, e

frame_a, entry_a = make_input_block(row_inputs, "  Número A")
frame_a.pack(side="left", padx=(0, 14))

frame_b, entry_b = make_input_block(row_inputs, "  Número B")
frame_b.pack(side="left", padx=(14, 0))

# Operações
ttk.Label(inner, text="OPERAÇÃO", bg=CARD, fg=TEXT_SUB,
          font=font_label).pack(pady=(18, 6))

btn_frame = ttk.Frame(inner, bg=CARD)
btn_frame.pack()

operacoes = ["+", "−", "×", "**", "÷"]

for op in operacoes:
    b = ttk.Button(
        btn_frame,
        text=op,
        font=font_btn,
        width=3,
        bg=CARD,
        fg=TEXT_MAIN,
        activebackground=BTN_HOVER,
        activeforeground=ACCENT,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=lambda o=op: calcular(o)
    )
    b.pack(side="left", padx=5)
    b.bind("<Enter>", lambda e, btn=b, o=op: on_enter(btn, o))
    b.bind("<Leave>", lambda e, btn=b, o=op: on_leave(btn, o))

# Separador
ttk.Frame(inner, bg=BORDER, height=1).pack(fill="x", pady=(18, 0))

# Resultado
result_frame = ttk.Frame(inner, bg=CARD)
result_frame.pack(pady=(12, 4), fill="x")

operacao_label = ttk.Label(result_frame, text="", bg=CARD,
                            fg=TEXT_SUB, font=font_small)
operacao_label.pack()

resultado_var = ttk.StringVar()
resultado_label = ttk.Label(result_frame,
                             textvariable=resultado_var,
                             bg=CARD, fg=ACCENT,
                             font=font_result)
resultado_label.pack()

# Botão limpar
ttk.Frame(inner, bg=BORDER, height=1).pack(fill="x", pady=(12, 10))

clear_btn = ttk.Button(inner, text="LIMPAR",
                       font=font_small,
                       bg=CARD, fg=TEXT_SUB,
                       activebackground=CARD,
                       activeforeground=ERROR_CLR,
                       relief="flat", bd=0,
                       cursor="hand2",
                       command=limpar)
clear_btn.pack()

# Rodapé
ttk.Frame(root, bg=BORDER, height=1).pack(fill="x", padx=PAD)
ttk.Label(root, text="por Francisco Medeiros  ·  python + tkinter",
          bg=BG, fg="#333333", font=font_label).pack(pady=(6, PAD))

# Foco inicial
entry_a.focus()

root.mainloop()
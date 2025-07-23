import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from pathlib import Path
import sys
import re

# Configurar paths
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "src"))

from src.lexer import lexer, reserved
from src.parser import parser

class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico/Sintáctico")
        self.root.geometry("1200x700")
        self.reserved_words = list(reserved.keys())  # ← Importa las palabras clave
        self.setup_ui()

    def setup_ui(self):
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(side=tk.TOP, fill=tk.X)

        self.load_btn = ttk.Button(button_frame, text="Cargar Archivo", command=self.load_file)
        self.load_btn.pack(side=tk.LEFT, padx=5)

        self.lex_btn = ttk.Button(button_frame, text="Análisis Léxico", command=self.lexical_analysis)
        self.lex_btn.pack(side=tk.LEFT, padx=5)

        self.syntax_btn = ttk.Button(button_frame, text="Análisis Sintáctico", command=self.syntax_analysis)
        self.syntax_btn.pack(side=tk.LEFT, padx=5)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.code_panel = ttk.Frame(main_frame)
        self.code_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(self.code_panel, text="Editor de Código").pack()
        self.code_text = scrolledtext.ScrolledText(
            self.code_panel,
            wrap=tk.WORD,
            font=('Consolas', 11),
            undo=True
        )
        self.code_text.pack(fill=tk.BOTH, expand=True)
        self.code_text.bind("<KeyRelease>", self.highlight_code)

        ttk.Separator(main_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)

        self.result_panel = ttk.Frame(main_frame, width=400)
        self.result_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        ttk.Label(self.result_panel, text="Tokens").pack()
        self.token_table = ttk.Treeview(self.result_panel, columns=("Texto", "Token", "Posición", "Lexema"), show="headings", height=15)
        for col in ("Texto", "Token", "Posición", "Lexema"):
            self.token_table.heading(col, text=col)
            self.token_table.column(col, width=100)
        self.token_table.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.result_panel, text="Resultados").pack()
        self.result_text = scrolledtext.ScrolledText(
            self.result_panel,
            wrap=tk.WORD,
            font=('Consolas', 11),
            state='disabled',
            height=10
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as file:
                self.code_text.delete(1.0, tk.END)
                self.code_text.insert(tk.END, file.read())
                self.highlight_code()
            self.show_result(f"Archivo cargado: {filepath}")

    def lexical_analysis(self):
        code = self.code_text.get(1.0, tk.END)
        self.token_table.delete(*self.token_table.get_children())

        if not code.strip():
            self.show_result("Error: No hay código para analizar")
            return

        lexer.input(code)
        try:
            for token in lexer:
                texto = token.value
                tipo = token.type
                posicion = f"[{token.lineno},{token.lexpos}]"
                lexema = texto
                self.token_table.insert("", "end", values=(texto, tipo, posicion, lexema))
            self.show_result("Análisis léxico completado")
        except Exception as e:
            self.show_result(f"ERROR EN ANÁLISIS LÉXICO:\n{str(e)}")

    def syntax_analysis(self):
        code = self.code_text.get(1.0, tk.END)
        if not code.strip():
            self.show_result("Error: No hay código para analizar")
            return

        try:
            result = parser.parse(code)
            ast_str = self.format_ast(result)
            self.show_result("=== ÁRBOL SINTÁCTICO ===\n" + ast_str)
        except Exception as e:
            self.show_result(f"ERROR DE SINTÁXIS:\n{str(e)}")

    def format_ast(self, node, indent=0):
        if isinstance(node, list):
            return "\n".join([self.format_ast(n, indent) for n in node])

        if not hasattr(node, '__dict__'):
            return " " * indent + str(node)

        node_str = " " * indent + node.__class__.__name__ + ":\n"
        for key, value in node.__dict__.items():
            if key.startswith('_') or key in ['lineno', 'lexpos']:
                continue
            node_str += " " * (indent + 2) + f"{key}: "
            if isinstance(value, (list, tuple)):
                node_str += "[\n" + self.format_ast(value, indent + 4) + "\n" + " " * (indent + 2) + "]\n"
            elif hasattr(value, '__dict__'):
                node_str += "\n" + self.format_ast(value, indent + 4)
            else:
                node_str += str(value) + "\n"
        return node_str

    def show_result(self, content):
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, content)
        self.result_text.config(state='disabled')

    def highlight_code(self, event=None):
        code = self.code_text.get("1.0", tk.END)
        self.code_text.tag_delete("highlight")
        for tag in self.code_text.tag_names():
            if tag.startswith("tok_"):
                self.code_text.tag_delete(tag)

        # Comentarios
        for match in re.finditer(r"#.*", code):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.code_text.tag_add("tok_comment", start, end)
        self.code_text.tag_configure("tok_comment", foreground="#008000")  # Verde

        # Palabras reservadas
        for word in self.reserved_words:
            for match in re.finditer(rf"\b{re.escape(word)}\b", code):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.code_text.tag_add("tok_keyword", start, end)
        self.code_text.tag_configure("tok_keyword", foreground="#0000AA")  # Azul oscuro

        # Cadenas
        for match in re.finditer(r"(['\"])(.*?)(\1)", code):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.code_text.tag_add("tok_string", start, end)
        self.code_text.tag_configure("tok_string", foreground="#008000")  # Verde

        # Signos de puntuación
        for match in re.finditer(r"[()\[\]{}]", code):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.code_text.tag_add("tok_punctuation", start, end)
        self.code_text.tag_configure("tok_punctuation", foreground="#FFD700")  # Amarillo
        

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeAnalyzerApp(root)
    root.mainloop()

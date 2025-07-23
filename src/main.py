import sys
from pathlib import Path

# Configuración robusta de paths
def configure_paths():
    # Obtener la ruta absoluta del directorio Taller
    taller_path = Path(__file__).parent.parent
    
    # Añadir ambas rutas necesarias
    sys.path.append(str(taller_path))
    sys.path.append(str(taller_path / "interfaz"))
    sys.path.append(str(taller_path / "src"))

    # Verificación (opcional para debug)
    print("Paths configurados:")
    for p in sys.path:
        print(p)

configure_paths()


def run_cli():
    """Versión de línea de comandos"""
    from lexer import lexer
    from parser import parser
    
    print("Analizador CLI - Ingrese código (Ctrl+C para salir)")
    while True:
        try:
            code = input(">>> ")
            if not code.strip():
                continue
                
            # Análisis léxico
            lexer.input(code)
            print("\nTokens:")
            for tok in lexer:
                print(f"{tok.type:15}: {tok.value}")
                
            # Análisis sintáctico
            result = parser.parse(code)
            print("\nAST:", result)
            
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break
        except Exception as e:
            print(f"Error: {e}")

def run_gui():
    """Versión gráfica"""
    try:
        from interfaz.aplicacion import CodeAnalyzerApp  # Cambiado de interfaz.aplicacion
        import tkinter as tk
        
        root = tk.Tk()
        app = CodeAnalyzerApp(root)
        root.mainloop()
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("Paths actuales:", sys.path)
        raise

if __name__ == "__main__":
    run_gui() 
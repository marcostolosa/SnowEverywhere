import tkinter as tk
import random
import math
from screeninfo import get_monitors # Biblioteca para detectar os monitores

class SnowWindow:
    def __init__(self, master, x, y, width, height):
        # Usamos Toplevel para criar janelas filhas da raiz principal
        self.window = tk.Toplevel(master)
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.attributes("-transparentcolor", "black")
        self.window.config(bg="black")
        
        # Define a geometria exata para "ESTE" monitor
        # Formato: "LARGURAxALTURA+POSICAO_X+POSICAO_Y"
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        self.width = width
        self.height = height
        area = width * height
        self.MAX_FLAKES = int(area / 50000)  # ajuste o divisor conforme o gosto
        
        self.canvas = tk.Canvas(self.window, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.flakes = []
        self.emoji_snow = ["❄️", "❅", "❆"] # Adicionei mais variações

        self.create_flake()
        self.update_flake()

    def create_flake(self):
        if len(self.flakes) < self.MAX_FLAKES:
            # Posição X aleatória dentro da largura deste monitor
            x_pos = random.randint(0, self.width)
            emoji = random.choice(self.emoji_snow)
            size = random.randint(15, 25)

            # Cria o texto no canvas
            flake_id = self.canvas.create_text(x_pos, -20, text=emoji, fill="white", font=("Arial", size))

            self.flakes.append({
                "id": flake_id,
                "speed": random.uniform(2, 4),
                "angle": random.uniform(0, math.pi * 2),
                "amplitude": random.uniform(1, 3),
            })

        # Agenda a criação do próximo floco nesta janela específica
        self.window.after(250, self.create_flake)

    def update_flake(self):
        for f in self.flakes:
            f["angle"] += 0.02
            drift = math.sin(f["angle"]) * f["amplitude"]
            
            self.canvas.move(f["id"], drift, f["speed"])
            
            pos = self.canvas.coords(f["id"])
            
            # Se o floco passar da altura deste monitor, reseta ele lá em cima
            if pos and pos[1] > self.height:
                self.canvas.coords(f["id"], random.randint(0, self.width), -20)
        
        # Atualiza a animação desta janela
        self.window.after(15, self.update_flake)

def main():
    # Cria a janela raiz oculta (necessária para o Tkinter rodar)
    root = tk.Tk()
    root.withdraw() # Esconde a janelinha principal vazia

    windows = []
    
    try:
        # Detecta todos os monitores conectados
        monitors = get_monitors()
        
        for m in monitors:
            print(f"Criando neve no monitor: {m.name} ({m.width}x{m.height} em {m.x},{m.y})")
            # Cria uma instância de neve para cada monitor
            snow = SnowWindow(root, m.x, m.y, m.width, m.height)
            windows.append(snow)
            
    except Exception as e:
        print(f"Erro ao detectar monitores: {e}")
        # Fallback: Se der erro na biblioteca, tenta criar um na tela principal
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        SnowWindow(root, 0, 0, screen_width, screen_height)

    # Inicia o loop principal que mantém todas as janelas vivas
    root.mainloop()

if __name__ == "__main__":
    main()

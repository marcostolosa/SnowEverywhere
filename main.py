import tkinter as tk
import random 
import math # Importante para o cálculo da onda

class SnowOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "black") # Mágica
        self.root.config(bg="black")
        self.MAX_FLAKES = 50 # Limite máximo de flocos na tela

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.flakes = []
        self.emoji_snow = ["❄️"]

        self.create_flake()
        self.update_flake()
        self.root.mainloop()

    def create_flake(self):
        if len(self.flakes) < self.MAX_FLAKES:
            x = random.randint(0, self.root.winfo_screenwidth())
            emoji = random.choice(self.emoji_snow)
            size = random.randint(15, 25)

            flake_id = self.canvas.create_text(x, -20, text=emoji, fill="white", font=("Arial", size))

            self.flakes.append({
                "id": flake_id,
                "speed": random.uniform(2, 4),
                "angle": random.uniform(0, math.pi * 2),
                "amplitude": random.uniform(1, 3),        
                "base_x": x                             
            })

        self.root.after(250, self.create_flake)
    
    def update_flake(self):
        for f in self.flakes:
            f["angle"] += 0.02 
            drift = math.sin(f["angle"]) * f["amplitude"]
            self.canvas.move(f["id"], drift, f["speed"])
            pos = self.canvas.coords(f["id"])
            if pos[1] > self.root.winfo_screenheight():
                self.canvas.coords(f["id"], random.randint(0, self.root.winfo_screenwidth()), -20)
            
        self.root.after(15, self.update_flake)

if __name__ == "__main__":
    SnowOverlay()
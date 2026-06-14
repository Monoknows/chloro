import math
import os
import random
import sys
import socket
import threading
import tkinter as tk

# Set up pathing back to the backend processing architecture
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))

class ChloroPremiumUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Strip standard window wrappers to make it an integrated desktop asset
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.title("CHLORO_CORE_MATRIX_v2.5")

        self.size = 400  
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        self.geometry(f"{self.size}x{self.size}+{screen_w - self.size - 40}+{screen_h - self.size - 80}")

        self.trans_color = "#010101"
        self.config(bg=self.trans_color)
        self.attributes("-transparentcolor", self.trans_color)

        self.canvas = tk.Canvas(self, width=self.size, height=self.size, bg=self.trans_color, bd=0, highlightthickness=0)
        self.canvas.pack()

        # ---- Dynamic State Engine Variables ----
        self.assistant_state = "listening" # Options: listening, thinking, answering
        self.angle_fast = 0.0
        self.angle_slow = 0.0
        self.pulse_val = 0.0
        self.voice_amplitude = 0.15  

        # Click-and-drag mouse bindings
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag_window)
        self.canvas.bind("<Button-3>", lambda e: self.destroy()) 

        # Start the background network thread to listen for state changes from the backend
        self.start_backend_listener()

        self.render_hud_frame()

    def start_drag(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def drag_window(self, event):
        x = self.winfo_x() + (event.x - self.x_offset)
        y = self.winfo_y() + (event.y - self.y_offset)
        self.geometry(f"+{x}+{y}")

    def update_state(self, new_state):
        """Updates the state securely and logs it to the terminal panel."""
        allowed_states = ["listening", "thinking", "answering"]
        if new_state in allowed_states:
            self.assistant_state = new_state
            print(f"📡 [TERMINAL INDICATOR]: State mutated -> {new_state.upper()}")

    def start_backend_listener(self):
        """Starts a background socket server on port 18788 to accept state commands."""
        def listen_for_backend():
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                server.bind(("127.0.0.1", 18788))
                server.listen(5)
                while True:
                    conn, addr = server.accept()
                    data = conn.recv(1024).decode('utf-8').strip().lower()
                    if data:
                        # Schedule state update on the main Tkinter thread safely
                        self.after(0, self.update_state, data)
                    conn.close()
            except Exception as e:
                print(f"⚠️ Listener socket error: {e}")

        threading.Thread(target=listen_for_backend, daemon=True).start()

    def render_hud_frame(self):
        """Advanced vector pipeline drawing multi-layered neon depth profiles with particle arrays."""
        self.canvas.delete("all")
        cx, cy = self.size / 2, self.size / 2

        self.pulse_val += 0.05
        pulse_glow = (math.sin(self.pulse_val) + 1.0) / 2.0 
        
        glitch_offset = 0
        if random.random() > 0.98:  
            glitch_offset = random.randint(-2, 2)

        # ---- State Engine Color Profiles ----
        if self.assistant_state == "listening":
            color_primary = "#00ffcc"    # Electric Cyan
            color_dark = "#00332a"       # Shadow Core Teal
            color_accent = "#80ffea"     # Highlight Core
            self.angle_slow += 0.012
            self.angle_fast -= 0.045
            
        elif self.assistant_state == "thinking":
            color_primary = "#0077ff"    # High-Energy Blue
            color_dark = "#001a33"       # Dark Void Blue
            color_accent = "#99ccff"     # Processing Ice Blue
            self.angle_slow += 0.04
            self.angle_fast -= 0.09
            
        elif self.assistant_state == "answering":
            color_primary = "#9400d3"    # JARVIS Purple / Neon Violet
            color_dark = "#2b003d"       # Deep Obsidian Purple
            color_accent = "#e0b0ff"     # Bright Orchid Highlight
            self.angle_slow += 0.02
            self.angle_fast -= 0.06
            
        else:
            color_primary = "#ff2a6d"    
            color_dark = "#330011"       
            color_accent = "#ff99bb"     
            self.angle_slow += 0.005
            self.angle_fast -= 0.01

        cx += glitch_offset

        # ─── LAYER 1: OUTER MEASUREMENT BOUNDS ───
        r_outer = 170
        self.canvas.create_oval(cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer, outline=color_dark, width=1)
        
        for angle in [0, math.pi/2, math.pi, 3*math.pi/2]:
            x_start = cx + (r_outer - 8) * math.cos(angle + self.angle_slow * 0.2)
            y_start = cy + (r_outer - 8) * math.sin(angle + self.angle_slow * 0.2)
            x_end = cx + (r_outer + 4) * math.cos(angle + self.angle_slow * 0.2)
            y_end = cy + (r_outer + 4) * math.sin(angle + self.angle_slow * 0.2)
            self.canvas.create_line(x_start, y_start, x_end, y_end, fill=color_primary, width=1)

        # Orbiting Satellite Telemetry Nodes
        for i in range(3):
            node_angle = self.angle_slow * 1.5 + (i * (2 * math.pi / 3))
            node_x = cx + r_outer * math.cos(node_angle)
            node_y = cy + r_outer * math.sin(node_angle)
            self.canvas.create_oval(node_x - 3, node_y - 3, node_x + 3, node_y + 3, fill=color_accent, outline=color_primary, width=1)

        # Dynamic Status Display Text
        display_status = f"SYS_MATRIX // {self.assistant_state.upper()}"
        self.canvas.create_text(cx, cy - r_outer - 14, text=display_status, fill=color_primary, font=("Consolas", 8, "bold"))
        
        hex_data = f"0x{int(abs(math.sin(self.angle_fast)*65535)):04X} // CLAW_LINK_18789"
        self.canvas.create_text(cx, cy + r_outer + 14, text=hex_data, fill=color_dark, font=("Consolas", 7, "bold"))

        # ─── LAYER 2: INTERIOR STRUCTURE ARCS ───
        r_arcs = 140 + (pulse_glow * 3 if self.assistant_state == "listening" else 0)
        deg_slow = math.degrees(self.angle_slow)
        
        self.canvas.create_arc(cx - r_arcs, cy - r_arcs, cx + r_arcs, cy + r_arcs, start=deg_slow, extent=140, outline=color_dark, style="arc", width=5)
        self.canvas.create_arc(cx - r_arcs, cy - r_arcs, cx + r_arcs, cy + r_arcs, start=deg_slow + 10, extent=120, outline=color_primary, style="arc", width=2)
        self.canvas.create_arc(cx - r_arcs, cy - r_arcs, cx + r_arcs, cy + r_arcs, start=deg_slow + 200, extent=80, outline=color_primary, style="arc", width=2)

        # ─── LAYER 3: AUDIO VISUALIZATION CORE RING ───
        r_wave_base = 112
        wave_points = []
        num_frequencies = 16
        
        for i in range(num_frequencies):
            angle = i * (2 * math.pi / num_frequencies) + self.angle_fast * 0.5
            # Maximize frequency spikes specifically during active listening or answering
            wave_mod = (random.random() * self.voice_amplitude * 22) if self.assistant_state in ["listening", "answering"] else (math.sin(self.pulse_val * 3 + i) * 2)
            r_current = r_wave_base + wave_mod
            
            wx = cx + r_current * math.cos(angle)
            wy = cy + r_current * math.sin(angle)
            wave_points.append((wx, wy))
            
        for i in range(len(wave_points)):
            p1 = wave_points[i]
            p2 = wave_points[(i + 1) % len(wave_points)]
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color_primary if self.assistant_state in ["listening", "answering"] else color_dark, width=1.5)

        self.canvas.create_oval(cx - 96, cy - 96, cx + 96, cy + 96, outline=color_dark, width=1, dash=(3, 9))

        # ─── LAYER 4: DETAILED CORE LATTICE GRID ───
        r_core = 74
        core_bg = "#010a0f" if self.assistant_state == "thinking" else "#000a08"
        self.canvas.create_oval(cx - r_core, cy - r_core, cx + r_core, cy + r_core, fill=core_bg, outline=color_primary, width=2)
        
        grid_lines = 6
        for i in range(1, grid_lines):
            offset = (i / grid_lines) * 2 * r_core - r_core
            chord = math.sqrt(max(0, r_core**2 - offset**2)) 
            self.canvas.create_line(cx - chord, cy + offset, cx + chord, cy + offset, fill=color_dark, width=1)
            self.canvas.create_line(cx + offset, cy - chord, cx + offset, cy + chord, fill=color_dark, width=1)

        # ─── LAYER 5: BIOLUMINESCENT ORB KINETICS ───
        r_glow = 28 + (pulse_glow * 2.5) + (self.voice_amplitude * 14)
        
        self.canvas.create_oval(cx - r_glow - 5, cy - r_glow - 5, cx + r_glow + 5, cy + r_glow + 5, fill="", outline=color_dark, width=1)
        self.canvas.create_oval(cx - r_glow, cy - r_glow, cx + r_glow, cy + r_glow, fill=color_primary, outline="")
        self.canvas.create_oval(cx - r_glow + 8, cy - r_glow + 8, cx + r_glow - 8, cy + r_glow - 8, fill=color_accent, outline="")

        self.after(16, self.render_hud_frame)

if __name__ == "__main__":
    app = ChloroPremiumUI()
    app.mainloop()
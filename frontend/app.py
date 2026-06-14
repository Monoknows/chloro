import math
import os
import random
import sys
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

        # UI Dimensional scale
        self.size = 400  # Bumped slightly to prevent text clipping
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        
        # Position cleanly above the Windows taskbar system tray area
        self.geometry(f"{self.size}x{self.size}+{screen_w - self.size - 40}+{screen_h - self.size - 80}")

        # Strict color-key alpha mask for transparent desktop widgets
        self.trans_color = "#010101"
        self.config(bg=self.trans_color)
        self.attributes("-transparentcolor", self.trans_color)

        # High-performance Vector Canvas
        self.canvas = tk.Canvas(self, width=self.size, height=self.size, bg=self.trans_color, bd=0, highlightthickness=0)
        self.canvas.pack()

        # ---- Dynamic State Engine Variables ----
        self.assistant_state = "listening" 
        self.angle_fast = 0.0
        self.angle_slow = 0.0
        self.pulse_val = 0.0
        self.voice_amplitude = 0.15  # Default baseline jump value for visualization

        # Click-and-drag mouse bindings
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag_window)
        self.canvas.bind("<Button-3>", lambda e: self.destroy()) # Right click close

        self.render_hud_frame()

    def start_drag(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def drag_window(self, event):
        x = self.winfo_x() + (event.x - self.x_offset)
        y = self.winfo_y() + (event.y - self.y_offset)
        self.geometry(f"+{x}+{y}")

    def render_hud_frame(self):
        """Advanced vector pipeline drawing multi-layered neon depth profiles with particle arrays."""
        self.canvas.delete("all")
        cx, cy = self.size / 2, self.size / 2

        # Step animation values
        self.pulse_val += 0.05
        pulse_glow = (math.sin(self.pulse_val) + 1.0) / 2.0  # Normalized 0.0 to 1.0
        
        # Simulated digital glitch noise matrix
        glitch_offset = 0
        if random.random() > 0.98:  # 2% chance per frame to generate a micro-flicker
            glitch_offset = random.randint(-2, 2)

        # State Engine Color Profiles
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
        else:
            color_primary = "#ff2a6d"    # Cyberpunk Red/Pink
            color_dark = "#330011"       # Deep Blood Burgundy
            color_accent = "#ff99bb"     # Overdrive White-Pink
            self.angle_slow += 0.005
            self.angle_fast -= 0.01

        # Apply glitch offset dynamically to center point
        cx += glitch_offset

        # ─── LAYER 1: OUTER MEASUREMENT BOUNDS & ORBIT NODES ───
        r_outer = 170
        self.canvas.create_oval(cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer, outline=color_dark, width=1)
        
        # Structural crosshair tick plates
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

        # Telemetry Text Streams
        display_status = f"SYS_MATRIX // {self.assistant_state.upper()}"
        self.canvas.create_text(cx, cy - r_outer - 14, text=display_status, fill=color_primary, font=("Consolas", 8, "bold"))
        
        # Rotating hexadecimal matrix indicator string
        hex_data = f"0x{int(abs(math.sin(self.angle_fast)*65535)):04X} // CLAW_LINK_18789"
        self.canvas.create_text(cx, cy + r_outer + 14, text=hex_data, fill=color_dark, font=("Consolas", 7, "bold"))

        # ─── LAYER 2: INTERIOR STRUCTURE ARCS ───
        r_arcs = 140 + (pulse_glow * 3 if self.assistant_state == "listening" else 0)
        deg_slow = math.degrees(self.angle_slow)
        
        self.canvas.create_arc(cx - r_arcs, cy - r_arcs, cx + r_arcs, cy + r_arcs, start=deg_slow, extent=140, outline=color_dark, style="arc", width=5)
        self.canvas.create_arc(cx - r_arcs, cy - r_arcs, cx + r_arcs, cy + r_arcs, start=deg_slow + 10, extent=120, outline=color_primary, style="arc", width=2)
        self.canvas.create_arc(cx - r_arcs, cy - r_arcs, cx + r_arcs, cy + r_arcs, start=deg_slow + 200, extent=80, outline=color_primary, style="arc", width=2)

        # ─── LAYER 3: AUDIO VISUALIZATION CORE RING (NEW) ───
        # This ring dynamically warps into multi-vertex waveform patterns when voice data triggers
        r_wave_base = 112
        wave_points = []
        num_frequencies = 16
        
        for i in range(num_frequencies):
            angle = i * (2 * math.pi / num_frequencies) + self.angle_fast * 0.5
            # Inject random sound frequencies scaled by voice amplitude
            wave_mod = (random.random() * self.voice_amplitude * 22) if self.assistant_state == "listening" else (math.sin(self.pulse_val * 3 + i) * 2)
            r_current = r_wave_base + wave_mod
            
            wx = cx + r_current * math.cos(angle)
            wy = cy + r_current * math.sin(angle)
            wave_points.append((wx, wy))
            
        # Draw the continuous sound loop pathing
        for i in range(len(wave_points)):
            p1 = wave_points[i]
            p2 = wave_points[(i + 1) % len(wave_points)]
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color_primary if self.assistant_state == "listening" else color_dark, width=1.5)

        # Fine telemetry divider line
        self.canvas.create_oval(cx - 96, cy - 96, cx + 96, cy + 96, outline=color_dark, width=1, dash=(3, 9))

        # ─── LAYER 4: DETAILED CORE LATTICE GRID ───
        r_core = 74
        core_bg = "#010a0f" if self.assistant_state == "thinking" else "#000a08"
        self.canvas.create_oval(cx - r_core, cy - r_core, cx + r_core, cy + r_core, fill=core_bg, outline=color_primary, width=2)
        
        grid_lines = 6
        for i in range(1, grid_lines):
            offset = (i / grid_lines) * 2 * r_core - r_core
            chord = math.sqrt(max(0, r_core**2 - offset**2)) # Cap out math limits
            self.canvas.create_line(cx - chord, cy + offset, cx + chord, cy + offset, fill=color_dark, width=1)
            self.canvas.create_line(cx + offset, cy - chord, cx + offset, cy + chord, fill=color_dark, width=1)

        # ─── LAYER 5: BIOLUMINESCENT ORB KINETICS ───
        r_glow = 28 + (pulse_glow * 2.5) + (self.voice_amplitude * 14)
        
        # Concentric light diffusion stacking
        self.canvas.create_oval(cx - r_glow - 5, cy - r_glow - 5, cx + r_glow + 5, cy + r_glow + 5, fill="", outline=color_dark, width=1)
        self.canvas.create_oval(cx - r_glow, cy - r_glow, cx + r_glow, cy + r_glow, fill=color_primary, outline="")
        self.canvas.create_oval(cx - r_glow + 8, cy - r_glow + 8, cx + r_glow - 8, cy + r_glow - 8, fill=color_accent, outline="")

        # Maintain a crisp 60 FPS update parameters cleanly (16ms refresh cadence)
        self.after(16, self.render_hud_frame)

if __name__ == "__main__":
    app = ChloroPremiumUI()
    app.mainloop()
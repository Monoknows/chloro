import math
import os
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
        self.title("CHLORO_CORE_MATRIX_v1.0")

        # UI Dimensional scale
        self.size = 380
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
        self.voice_amplitude = 0.0

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
        """Advanced vector pipeline that draws multi-layered neon depth profiles."""
        self.canvas.delete("all")
        cx, cy = self.size / 2, self.size / 2

        # Step animation values
        self.pulse_val += 0.05
        
        # Color palettes and dynamic speed profiles matching system behavior
        pulse_glow = (math.sin(self.pulse_val) + 1.0) / 2.0  # Normalized 0.0 to 1.0
        
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

        # ─── LAYER 1: OUTER MEASUREMENT BOUNDS ───
        r_outer = 170
        # Thin baseline boundary ring
        self.canvas.create_oval(cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer, outline=color_dark, width=1)
        
        # Structural crosshair tick plates at 0, 90, 180, and 270 degrees
        for angle in [0, math.pi/2, math.pi, 3*math.pi/2]:
            x_start = cx + (r_outer - 8) * math.cos(angle)
            y_start = cy + (r_outer - 8) * math.sin(angle)
            x_end = cx + (r_outer + 4) * math.cos(angle)
            y_end = cy + (r_outer + 4) * math.sin(angle)
            self.canvas.create_line(x_start, y_start, x_end, y_end, fill=color_primary, width=1)

        # Telemetry Data Text Overlays (Fixed: removed -letterspacing argument completely)
        display_status = f"INTERFACE_STATUS // {self.assistant_state.upper()}"
        self.canvas.create_text(cx, cy - r_outer - 12, text=display_status, 
                                fill=color_primary, font=("Consolas", 7, "bold"))
        self.canvas.create_text(cx, cy + r_outer + 12, text="CHLORO AUTOMATION CORE v2.0", 
                                fill=color_dark, font=("Consolas", 6, "bold"))

        # ─── LAYER 2: CHUNKY STRUCTURAL ARCS (SLOW ROTATION) ───
        r_arcs = 140 + (pulse_glow * 4 if self.assistant_state == "listening" else 0)
        deg_slow = math.degrees(self.angle_slow)
        
        # We sandwich a thick primary arc with thin bright core lines to simulate an internal neon glow
        # Heavy shadow backing lines
        self.canvas.create_arc(cx - r_arcs, cy - r_arcs, cx + r_arcs, cy + r_arcs, start=deg_slow, extent=140, outline=color_dark, style="arc", width=6)
        self.canvas.create_arc(cx - r_arcs, cy - r_arcs, cx + r_arcs, cy + r_arcs, start=deg_slow + 190, extent=100, outline=color_dark, style="arc", width=6)
        
        # Primary glowing cores
        self.canvas.create_arc(cx - r_arcs, cy - r_arcs, cx + r_arcs, cy + r_arcs, start=deg_slow + 10, extent=120, outline=color_primary, style="arc", width=3)
        self.canvas.create_arc(cx - r_arcs, cy - r_arcs, cx + r_arcs, cy + r_arcs, start=deg_slow + 200, extent=80, outline=color_primary, style="arc", width=3)

        # ─── LAYER 3: THE HIGH-SPEED RADAR TACHOMETER (COUNTER-SPIN) ───
        r_radar = 112
        deg_fast = math.degrees(self.angle_fast)
        
        # Creates a sweeping high-density radar segment with variable shading
        self.canvas.create_arc(cx - r_radar, cy - r_radar, cx + r_radar, cy + r_radar, start=deg_fast, extent=45, outline=color_primary, style="arc", width=1)
        self.canvas.create_arc(cx - r_radar, cy - r_radar, cx + r_radar, cy + r_radar, start=deg_fast + 5, extent=15, outline=color_accent, style="arc", width=2)
        self.canvas.create_arc(cx - r_radar, cy - r_radar, cx + r_radar, cy + r_radar, start=deg_fast + 180, extent=30, outline=color_dark, style="arc", width=1)

        # Fine telemetry divider line
        self.canvas.create_oval(cx - 96, cy - 96, cx + 96, cy + 96, outline=color_dark, width=1, dash=(4, 12))

        # ─── LAYER 4: CENTRAL LATTICE ORB MATRIX ───
        r_core = 70
        # Dark primary backing fill to give opacity depth against window backgrounds
        self.canvas.create_oval(cx - r_core, cy - r_core, cx + r_core, cy + r_core, fill="#010a0f" if self.assistant_state=="thinking" else "#000a08", outline=color_primary, width=2)
        
        # Complex circular grid line processing
        grid_lines = 5
        for i in range(1, grid_lines):
            offset = (i / grid_lines) * 2 * r_core - r_core
            chord = math.sqrt(r_core**2 - offset**2)
            # Horizontal Grids
            self.canvas.create_line(cx - chord, cy + offset, cx + chord, cy + offset, fill=color_dark, width=1)
            # Vertical Grids
            self.canvas.create_line(cx + offset, cy - chord, cx + offset, cy + chord, fill=color_dark, width=1)

        # ─── LAYER 5: THE INTERACTIVE BIO-LUMINESCENT ENGINE CORE ───
        # Scale core sphere diameter directly with voice amplitude spikes
        r_glow = 26 + (pulse_glow * 3) + (self.voice_amplitude * 18)
        
        # Triple-layer concentric orb stacking for artificial shadow blending
        self.canvas.create_oval(cx - r_glow - 6, cy - r_glow - 6, cx + r_glow + 6, cy + r_glow + 6, fill="", outline=color_dark, width=2)
        self.canvas.create_oval(cx - r_glow, cy - r_glow, cx + r_glow, cy + r_glow, fill=color_primary, outline="")
        self.canvas.create_oval(cx - r_glow + 8, cy - r_glow + 8, cx + r_glow - 8, cy + r_glow - 8, fill=color_accent, outline="")

        # Maintain 60 FPS update parameters cleanly
        self.after(16, self.render_hud_frame)

if __name__ == "__main__":
    app = ChloroPremiumUI()
    app.mainloop()
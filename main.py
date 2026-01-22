import flet as ft
import yt_dlp
import os
import math

# APP CONFIG
DOWNLOAD_FOLDER = "/storage/emulated/0/Download"  # Default Android path
if os.name == 'nt': # If running on Windows for testing
    DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Desktop")

def main(page: ft.Page):
    page.title = "Universal Downloader Mobile"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = "adaptive"
    page.bgcolor = "#111111"

    # --- STATE VARIABLES ---
    speed_val = 1.0
    
    # --- UI ELEMENTS ---
    
    # Header
    header = ft.Text("Universal Downloader", size=28, weight="bold", color="#2db150")
    sub_header = ft.Text("YouTube • TikTok • Instagram", size=14, color="grey")
    
    # Link Input
    txt_url = ft.TextField(
        label="Paste Link Here",
        border_color="#2db150",
        prefix_icon=ft.icons.LINK,
        bgcolor="#222222"
    )

    # Status Text
    txt_status = ft.Text("Ready...", color="white")
    progress_bar = ft.ProgressBar(width=400, color="#2db150", bgcolor="#333333", visible=False)

    # --- SETTINGS SECTION ---
    
    # Speed Selection
    def slider_changed(e):
        speed_val = float(int(e.control.value * 10)) / 10.0 # Round to 1 decimal
        lbl_speed.value = f"Speed: {e.control.value}x"
        page.update()

    lbl_speed = ft.Text("Speed: 1.0x", size=16)
    slider_speed = ft.Slider(
        min=0.5, max=2.5, divisions=20, value=1.0, label="{value}x",
        active_color="#2db150", on_change=slider_changed
    )
    
    # Enhance Switch
    sw_enhance = ft.Switch(label="Magic Enhance (Color + Sharp)", value=True, active_color="#2db150")
    
    # Volume Boost
    dd_volume = ft.Dropdown(
        label="Volume Boost",
        width=150,
        options=[
            ft.dropdown.Option("1.0", "Normal"),
            ft.dropdown.Option("1.5", "Loud (150%)"),
            ft.dropdown.Option("2.0", "Louder (200%)"),
            ft.dropdown.Option("3.0", "Max (300%)"),
        ],
        value="1.0",
        bgcolor="#222222"
    )

    # --- CALCULATOR ---
    calc_orig_m = ft.TextField(label="Min", width=60, text_align="center", value="0", keyboard_type="number")
    calc_orig_s = ft.TextField(label="Sec", width=60, text_align="center", value="0", keyboard_type="number")
    calc_targ_m = ft.TextField(label="Min", width=60, text_align="center", value="3", keyboard_type="number")
    calc_targ_s = ft.TextField(label="Sec", width=60, text_align="center", value="0", keyboard_type="number")
    
    def calculate_click(e):
        try:
            curr = (int(calc_orig_m.value) * 60) + int(calc_orig_s.value)
            targ = (int(calc_targ_m.value) * 60) + int(calc_targ_s.value)
            
            if targ == 0:
                txt_status.value = "Target cannot be 0!"
                txt_status.color = "red"
                page.update()
                return

            factor = round(curr / targ, 2)
            if factor < 0.5: factor = 0.5
            
            lbl_speed.value = f"Speed: {factor}x"
            slider_speed.value = factor
            txt_status.value = f"Calculated Speed: {factor}x"
            txt_status.color = "#2db150"
            page.update()
            
        except:
             txt_status.value = "Invalid numbers in calculator"
             page.update()

    btn_calc = ft.ElevatedButton("Calculate Speed", on_click=calculate_click, bgcolor="#333333", color="white")

    # --- DOWNLOAD LOGIC ---
    def download_click(e):
        url = txt_url.value
        if not url:
            txt_status.value = "Please paste a link first!"
            txt_status.color = "red"
            page.update()
            return

        btn_download.disabled = True
        btn_download.text = "Processing..."
        progress_bar.visible = True
        txt_status.value = "Downloading..."
        txt_status.color = "white"
        page.update()

        try:
            # yt-dlp options
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best', # Android ffmpeg might fail on merge if binary missing
                'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
            }

            # On Android, bundling ffmpeg is hard with pure python.
            # We strictly warn about enhancement
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            
            txt_status.value = "Success! Saved to Downloads."
            txt_status.color = "#2db150"
            
            # NOTE: Actual FFMPEG processing (speed/enhance/volume) on Android 
            # requires 'ffmpeg-kit' or termux. This pure python code 
            # will only download standard file. 
            
            if sw_enhance.value or slider_speed.value != 1.0:
                 txt_status.value += "\n(Note: Speed/Enhance requires PC or FFmpeg App)"

        except Exception as ex:
            txt_status.value = f"Error: {str(ex)}"
            txt_status.color = "red"
        
        btn_download.disabled = False
        btn_download.text = "Download Video"
        progress_bar.visible = False
        page.update()

    btn_download = ft.ElevatedButton(
        "Download Video", 
        icon=ft.icons.DOWNLOAD, 
        width=300, 
        height=50, 
        bgcolor="#2db150", 
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=download_click
    )

    # --- LAYOUT ASSEMBLE ---
    
    card_calc = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Speed Calculator", weight="bold"),
                ft.Row([
                    ft.Text("Orig:"), calc_orig_m, ft.Text(":"), calc_orig_s,
                    ft.Text("  Targ:"), calc_targ_m, ft.Text(":"), calc_targ_s
                ], alignment="center"),
                btn_calc
            ], horizontal_alignment="center", spacing=10),
            padding=15
        ),
        color="#222222"
    )

    page.add(
        ft.Column([
            ft.Container(height=20),
            ft.Icon(name=ft.icons.VIDEO_LIBRARY_ROUNDED, size=50, color="#2db150"),
            header,
            sub_header,
            ft.Container(height=20),
            txt_url,
            ft.Container(height=10),
            ft.Text("Settings", size=18, weight="bold"),
            ft.Container(
                content=ft.Column([
                    lbl_speed,
                    slider_speed,
                    ft.Row([sw_enhance, dd_volume], alignment="spaceBetween")
                ]),
                bgcolor="#222222", padding=15, border_radius=10
            ),
            ft.Container(height=10),
            card_calc,
            ft.Container(height=20),
            btn_download,
            progress_bar,
            txt_status
        ], horizontal_alignment="center")
    )

ft.app(target=main)

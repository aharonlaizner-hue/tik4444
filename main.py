import flet as ft
import yt_dlp
import os
import datetime
import time

def main(page: ft.Page):
    page.title = "TikDownloader Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#111111"
    page.scroll = "adaptive"
    page.padding = 20

    # UI Variables
    save_path = "/storage/emulated/0/Download"
    
    def log(msg, color="white"):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        status_text.value = f"[{timestamp}] {msg}"
        status_text.color = color
        page.update()

    # --- PROGRESS HOOK ---
    def progress_hook(d):
        if d['status'] == 'downloading':
            try:
                p = d.get('_percent_str', '0%').replace('%','')
                val = float(p) / 100
                progress_bar.value = val
                btn_dl.text = f"Downloading... {int(val*100)}%"
                page.update()
            except:
                pass
        elif d['status'] == 'finished':
            progress_bar.value = 1.0
            btn_dl.text = "Processing..."
            page.update()

    # --- LOGIC ---
    def calc_speed(e):
        try:
            m_orig = int(txt_orig_m.value or 0)
            s_orig = int(txt_orig_s.value or 0)
            m_targ = int(txt_targ_m.value or 3)
            s_targ = int(txt_targ_s.value or 0)

            total_curr = (m_orig * 60) + s_orig
            total_targ = (m_targ * 60) + s_targ
            
            if total_targ == 0: return

            factor = round(total_curr / total_targ, 2)
            if factor < 0.5: factor = 0.5
            
            lbl_calc.value = f"Need: {factor}x"
            slider_speed.value = factor if factor <= 3.0 else 3.0
            lbl_speed.value = f"Speed: {factor}x"
            page.update()
        except: pass

    def slider_changed(e):
        lbl_speed.value = f"Speed: {round(e.control.value, 2)}x"
        page.update()

    def download_click(e):
        url = txt_url.value
        if not url:
            log("No Link!", "red")
            return

        btn_dl.disabled = True
        progress_bar.visible = True
        progress_bar.value = 0
        log("Starting...", "yellow")
        page.update()
        
        try:
            # 1. Download
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': f'{save_path}/%(title)s.%(ext)s',
                'noplaylist': True,
                'ignoreerrors': True,
                'progress_hooks': [progress_hook],
                'nocheckcertificate': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                fname = ydl.prepare_filename(info)
            
            # 2. Check for Processing (Speed/Enhance)
            # NOTE: This requires ffmpeg binary on the device.
            # If missing, we skip and just warn.
            
            log("Saved! (Processing skipped on mobile)", "green")
            
        except Exception as ex:
            log(f"Error: {str(ex)}", "red")
        
        btn_dl.disabled = False
        btn_dl.text = "Download"
        progress_bar.visible = False
        page.update()

    # --- UI ELEMENTS ---
    
    # 1. Header
    header = ft.Text("TikDownloader Pro", size=28, weight="bold", color="#2db150")

    # 2. Input
    txt_url = ft.TextField(label="Paste Link Here", border_color="#2db150", text_size=14)

    # 3. Calculator
    txt_orig_m = ft.TextField(label="Min", width=50, value="0", text_align="center")
    txt_orig_s = ft.TextField(label="Sec", width=50, value="0", text_align="center")
    txt_targ_m = ft.TextField(label="Min", width=50, value="3", text_align="center")
    txt_targ_s = ft.TextField(label="Sec", width=50, value="0", text_align="center")
    lbl_calc = ft.Text("-", weight="bold", color="#2db150")
    btn_calc = ft.ElevatedButton("Calc", on_click=calc_speed, bgcolor="#333333")

    calc_row = ft.Container(
        content=ft.Column([
            ft.Text("Speed Calculator", size=12, color="grey"),
            ft.Row([ft.Text("Orig:"), txt_orig_m, txt_orig_s], alignment="center"),
            ft.Row([ft.Text("Targ:"), txt_targ_m, txt_targ_s], alignment="center"),
            ft.Row([btn_calc, lbl_calc], alignment="center", spacing=20)
        ]),
        bgcolor="#1a1a1a", padding=10, border_radius=10
    )

    # 4. Settings
    lbl_speed = ft.Text("Speed: 1.0x")
    slider_speed = ft.Slider(min=0.5, max=3.0, divisions=25, value=1.0, active_color="#2db150", on_change=slider_changed)
    sw_enhance = ft.Switch(label="Enhance Graphics", active_color="#2db150")
    
    settings_col = ft.Container(
        content=ft.Column([lbl_speed, slider_speed, sw_enhance]),
        bgcolor="#1a1a1a", padding=10, border_radius=10
    )

    # 5. Actions
    progress_bar = ft.ProgressBar(width=300, color="#2db150", bgcolor="#333333", visible=False)
    btn_dl = ft.ElevatedButton("Download", on_click=download_click, bgcolor="#2db150", color="white", width=300, height=45)
    status_text = ft.Text("Ready", size=12, text_align="center")

    page.add(
        ft.Column([
            ft.Container(height=10),
            header,
            ft.Container(height=15),
            txt_url,
            ft.Container(height=10),
            calc_row,
            ft.Container(height=10),
            settings_col,
            ft.Container(height=20),
            progress_bar,
            btn_dl,
            ft.Container(height=10),
            status_text
        ], horizontal_alignment="center")
    )

ft.app(target=main)

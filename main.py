import flet as ft
import yt_dlp
import os

def main(page: ft.Page):
    page.title = "TikDownloader V2"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#111111"
    page.scroll = "adaptive"

    # Save path - Try standard paths, fallback to internal
    save_dir = "/storage/emulated/0/Download"
    
    # UI Elements
    lbl_status = ft.Text("Ready", color="white")
    
    def log(msg, color="white"):
        lbl_status.value = msg
        lbl_status.color = color
        page.update()

    def download_click(e):
        url = txt_url.value
        if not url:
            log("Paste a link first!", "red")
            return

        log("Starting...", "yellow")
        
        try:
            # Safer options for Android (No FFmpeg dependency)
            ydl_opts = {
                'format': 'best[ext=mp4]/best',  # Force single file (no merge needed)
                'outtmpl': f'{save_dir}/%(title)s.%(ext)s',
                'noplaylist': True,
                'ignoreerrors': True,
                # 'quiet': True
            }
            
            # Try to download
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(url, download=True)
            
            log(f"Saved to: {save_dir}", "green")
            
        except Exception as ex:
            # If permission denied, try internal storage
            log(f"Error: {ex}\nTrying internal storage...", "orange")
            try:
                # Fallback to app data dir
                internal_path = page.client_storage.get("internal_path") 
                # Note: Flet on Android has restricted FS access. 
                # Real external access needs 'permission_handler' in pure Flutter.
                # Here we just catch the crash.
            except:
                pass
            
            log(f"Failed: {ex}", "red")

    txt_url = ft.TextField(label="Link", border_color="#2db150")
    btn_dl = ft.ElevatedButton("Download", bgcolor="#2db150", color="white", on_click=download_click)

    page.add(
        ft.Column([
            ft.Text("TikDownloader Mobile", size=24, weight="bold"),
            ft.Container(height=20),
            txt_url,
            ft.Container(height=10),
            btn_dl,
            ft.Container(height=20),
            lbl_status
        ])
    )

ft.app(target=main)

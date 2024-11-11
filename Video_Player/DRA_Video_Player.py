import customtkinter
from tkVideoPlayer import TkinterVideo

class VideoPlayer(customtkinter.CTk):
    def __init__(self, video_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1024x764")
        self.title("DRA Video Player")

        self.video_path = video_path
        self.setup_ui()
        self.load_video(self.video_path)

    def setup_ui(self):
        self.frame = customtkinter.CTkFrame(master=self, corner_radius=15)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Video player setup
        self.vid_player = TkinterVideo(master=self.frame, scaled=True, keep_aspect=True, bg="black")
        self.vid_player.pack(expand=True, fill="both", padx=10, pady=10)

        # Button to restart the video
        self.restart_btn = customtkinter.CTkButton(master=self.frame, text="Restart Video", command=self.restart_video)
        self.restart_btn.pack(pady=10)

    def load_video(self, video_path):
        self.vid_player.load(video_path)

    def restart_video(self):
        # Stop the current playback and seek to the start
        self.vid_player.stop()
        self.vid_player.load(self.video_path)  # Re-load the video to start from the beginning
        self.vid_player.play()  # Play the video

if __name__ == "__main__":
    video_path = r"C:\Users\Jugto\Desktop\DRA\CustomTkinter-master\merged_video.mp4"  # Change this to the path of your video file
    app = VideoPlayer(video_path)
    app.mainloop()
import os
import yt_dlp
import requests
from tqdm import tqdm
from colorama import Fore, Style, init
import time


init(autoreset=True)


def get_default_download_folder():
    home_dir = os.path.expanduser("~") 
    return os.path.join(home_dir, "Downloads")  

def download_youtube_video(url, path):
    try:
        qualities = {
            '1': 'best',
            '2': '720p',   
            '3': '480p',  
            '4': '360p',  
            '5': '240p',
            '6': '144p'    
        }

        print(Fore.BLUE + "\nSelect video quality:")
        for key, value in qualities.items():
            print(f"{Fore.MAGENTA}{key}. {value}")

        choice = input(Fore.CYAN + "Enter your choice (1-6): ").strip()
        selected_quality = qualities.get(choice, 'best')

        ydl_opts = {
            'format': f'best[height<={selected_quality}][ext=mp4]',  
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': False,
            'progress_hooks': [lambda d: handle_progress(d)],
        }

        def handle_progress(status):
            """Custom progress hook to handle download status."""
            if status['status'] == 'downloading':
                filename = status.get('filename', 'Unknown')
                downloaded_bytes = status.get('downloaded_bytes', 0)
                total_bytes = status.get('total_bytes', None)
                if total_bytes:
                    percent = (downloaded_bytes / total_bytes) * 100
                    print(f"\r{Fore.YELLOW}Downloading: {filename} - {percent:.2f}%", end="")
                else:
                    print(f"\r{Fore.YELLOW}Downloading: {filename} - {downloaded_bytes} bytes", end="")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(Fore.BLUE + "\nDownloading YouTube video...")
            ydl.download([url])
        print(Fore.GREEN + "\nDownload completed!")
    except Exception as e:
        print(Fore.RED + f"\nError downloading YouTube video: {e}")


def download_direct_video(video_url, path, filename_prefix):
    try:
        response = requests.get(video_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  
        filename = os.path.join(path, f"{filename_prefix}_{os.urandom(4).hex()}.mp4")
        
      
        print(Fore.BLUE + Style.BRIGHT + f"\nDownloading {filename_prefix} video...".center(80, " "))
        print(Fore.CYAN + "-" * 80) 
        
        
        with tqdm(
            total=total_size,
            unit='iB',
            unit_scale=True,
            desc=Fore.GREEN + f"Downloading {filename_prefix}".center(30),
            bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.YELLOW, Fore.RESET)
        ) as progress_bar:
            with open(filename, 'wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
        
       
        print(Fore.CYAN + "-" * 80)
        print(Fore.GREEN + Style.BRIGHT + "Download completed!".center(80, " "))
    except Exception as e:
     
        print(Fore.RED + Style.BRIGHT + f"Error downloading video: {e}".center(80, " "))


def print_ascii_art():
    """Print an ASCII art logo."""
    print(Fore.CYAN + r"""
     _______ _        _______           _______  _______ 
    (  ____ \ \      (  ___  )|\     /|(  ____ \(  ____ \
    | (    \/ /      | (   ) || )   ( || (    \/| (    \/
    | (__    /       | |   | || |   | || (__    | (_____ 
    |  __)  /        | |   | || |   | ||  __)   (_____  )
    | (    /         | |   | || |   | || (            ) |
    | )   /          | (___) || (___) || )       /\____) |
    |/   /           (_______)(_______)|/        \_______)
    """)


def loading_animation(message, duration=2):
    """Display a simple loading animation."""
    animation = "|/-\\"
    for i in range(duration * 10):  
        time.sleep(0.1)
        print(f"\r{Fore.YELLOW}{message} {animation[i % len(animation)]}", end="")
    print("\r" + " " * (len(message) + 2), end="\r")  


def main():
  
    print_ascii_art()
    print(Fore.YELLOW + "=" * 50)
    print(Fore.GREEN + " Welcome to the Awesome Video Downloader Tool! ".center(50, "="))
    print(Fore.YELLOW + "=" * 50 + "\n")


    print(Fore.BLUE + "Select the platform from which you want to download:")
    print(Fore.MAGENTA + "1. YouTube")
    print(Fore.MAGENTA + "2. Facebook Reels")
    print(Fore.MAGENTA + "3. TikTok Videos")
    print(Fore.MAGENTA + "4. Instagram Reels")


    while True:
        choice = input(Fore.CYAN + "\nEnter your choice (1-4): ").strip()
        if choice in ["1", "2", "3", "4"]:
            break
        else:
            print(Fore.RED + "Invalid choice! Please enter a number between 1 and 4.")

    
    while True:
        url = input(Fore.CYAN + "\nEnter the video URL: ").strip()
        if url:
            break
        else:
            print(Fore.RED + "Please enter a valid video URL!")

    
    default_path = get_default_download_folder()
    print(Fore.GREEN + f"\nDefault download folder: {default_path}")

    
    while True:
        change_path = input(Fore.CYAN + "\nDo you want to change the download folder? (y/n): ").strip().lower()
        if change_path == 'y':
            while True:
                path = input(Fore.CYAN + "Enter the new download path: ").strip()
                if path:
                    if not os.path.exists(path):
                        try:
                            os.makedirs(path)
                            print(Fore.GREEN + f"Created new folder: {path}")
                        except Exception as e:
                            print(Fore.RED + f"Error creating folder: {e}")
                            continue
                    break
                else:
                    print(Fore.RED + "Please enter a valid folder path!")
            break
        elif change_path == 'n':
            path = default_path
            break
        else:
            print(Fore.RED + "Please enter 'y' or 'n'.")

    
    print(Fore.YELLOW + "\nProcessing your request...")
    loading_animation("Loading...", duration=2)

    if choice == "1":
        print(Fore.BLUE + "\nDownloading from YouTube...")
        download_youtube_video(url, path)
    elif choice in ["2", "3", "4"]:
        platform_name = ""
        if choice == "2":
            platform_name = "Facebook_Reel"
        elif choice == "3":
            platform_name = "TikTok_Video"
        elif choice == "4":
            platform_name = "Instagram_Reel"
        print(Fore.BLUE + f"\nDownloading from {platform_name}...")
        download_direct_video(url, path, platform_name)
    else:
        print(Fore.RED + "Invalid choice! Exiting the program.")

 
    print(Fore.GREEN + "\nThank you for using the Awesome Video Downloader Tool!\n")
    print_ascii_art()

if __name__ == "__main__":
    main()
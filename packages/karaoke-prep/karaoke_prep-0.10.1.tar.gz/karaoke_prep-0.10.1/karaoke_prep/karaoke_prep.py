import os
import sys
import re
import glob
import yt_dlp
import logging
import lyricsgenius
import tempfile
import importlib.resources as pkg_resources
from PIL import Image, ImageDraw, ImageFont


class KaraokePrep:
    def __init__(
        self,
        url=None,
        artist=None,
        title=None,
        log_level=logging.DEBUG,
        log_formatter=None,
        model_name="UVR_MDXNET_KARA_2",
        model_name_2="UVR-MDX-NET-Inst_HQ_3",
        model_file_dir=os.path.join(tempfile.gettempdir(), "audio-separator-models"),
        output_dir=".",
        lossless_output_format="FLAC",
        lossy_output_format="MP3",
        use_cuda=False,
        use_coreml=False,
        normalization_enabled=True,
        denoise_enabled=True,
        create_track_subfolders=False,
        intro_background_color="#000000",
        intro_background_image=None,
        intro_font="Montserrat-Bold.ttf",
        intro_artist_color="#ffffff",
        intro_title_color="#ff7acc",
    ):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.log_level = log_level
        self.log_formatter = log_formatter

        self.log_handler = logging.StreamHandler()

        if self.log_formatter is None:
            self.log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")

        self.log_handler.setFormatter(self.log_formatter)
        self.logger.addHandler(self.log_handler)

        self.logger.debug(f"KaraokePrep instantiating with url: {url} artist: {artist} title: {title}")

        self.url = url
        self.artist = artist
        self.title = title
        self.model_name = model_name
        self.model_name_2 = model_name_2
        self.model_file_dir = model_file_dir
        self.output_dir = output_dir
        self.lossless_output_format = lossless_output_format.lower()
        self.lossy_output_format = lossy_output_format.lower()
        self.use_cuda = use_cuda
        self.use_coreml = use_coreml
        self.normalization_enabled = normalization_enabled
        self.denoise_enabled = denoise_enabled
        self.create_track_subfolders = create_track_subfolders

        # Path to the Windows PyInstaller frozen bundled ffmpeg.exe, or the system-installed FFmpeg binary on Mac/Linux
        ffmpeg_path = os.path.join(sys._MEIPASS, "ffmpeg.exe") if getattr(sys, "frozen", False) else "ffmpeg"

        self.ffmpeg_base_command = f"{ffmpeg_path} -hide_banner -nostats"

        if self.log_level == logging.DEBUG:
            self.ffmpeg_base_command += " -loglevel verbose"
        else:
            self.ffmpeg_base_command += " -loglevel fatal"

        self.title_format = {
            "background_color": intro_background_color,
            "background_image": intro_background_image,
            "intro_font": intro_font,
            "artist_color": intro_artist_color,
            "title_color": intro_title_color,
        }

        self.persistent_artist = None

        self.logger.debug(f"KaraokePrep lossless_output_format: {self.lossless_output_format}")

        if not os.path.exists(self.output_dir):
            self.logger.debug(f"Overall output dir {self.output_dir} did not exist, creating")
            os.makedirs(self.output_dir)
        else:
            self.logger.debug(f"Overall output dir {self.output_dir} already exists")

    def extract_metadata_from_url(self):
        """
        Extracts metadata from the YouTube URL.
        """
        if self.url:
            with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
                info = ydl.extract_info(self.url, download=False)
                self.artist, self.title = self.parse_metadata(info)
                if self.persistent_artist:
                    self.artist = self.persistent_artist
                if self.artist and self.title:
                    self.logger.info(f"Extracted artist: {self.artist}, title: {self.title}")
                else:
                    self.logger.error("Failed to extract artist and title from the YouTube URL.")

    def parse_metadata(self, info):
        """
        Parses the metadata to extract artist and title.

        :param info: The metadata information extracted from yt_dlp.
        :return: A tuple containing the artist and title.
        """
        # Default values if parsing fails
        artist = ""
        title = ""

        # Example: "Artist - Title"
        if "title" in info and "-" in info["title"]:
            artist, title = info["title"].split("-", 1)
            artist = artist.strip()
            title = title.strip()
        elif "uploader" in info:
            # Fallback to uploader as artist if title parsing fails
            artist = info["uploader"]
            if "title" in info:
                title = info["title"].strip()

        # If unable to parse, log an appropriate message
        if not artist or not title:
            self.logger.warning("Could not parse artist and title from the video metadata.")

        return artist, title

    def get_youtube_id_for_top_search_result(self, query):
        ydl_opts = {"quiet": "True", "format": "bestaudio", "noplaylist": "True", "extract_flat": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video = ydl.extract_info(f"ytsearch1:{query}", download=False)["entries"][0]

            if video:
                youtube_id = video.get("id")
                return youtube_id
            else:
                self.logger.warning(f"No YouTube results found for query: {query}")
                return None

    def download_video(self, youtube_id, output_filename_no_extension):
        self.logger.debug(f"Downloading YouTube video {youtube_id} to filename {output_filename_no_extension} + (as yet) unknown extension")

        downloaded_file_name = output_filename_no_extension
        actual_file_extension = None

        # TODO: fix file extension for example karaoke-prep --log_level debug "Ken Ashcorp" "Dare You To Love Me"

        def ydl_progress_hook(d):
            nonlocal actual_file_extension
            actual_file_extension = d["filename"].split(".")[-1]

        ydl_opts = {
            "quiet": True,
            "format": "bv*+ba/b",  # if a combined video + audio format is better than the best video-only format use the combined format
            "outtmpl": f"{output_filename_no_extension}",
            "progress_hooks": [ydl_progress_hook],
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as youtube_dl_instance:
            youtube_dl_instance.download([f"https://www.youtube.com/watch?v={youtube_id}"])
            downloaded_file_name += f".{actual_file_extension}"
            self.logger.info(f"Download finished, returning downloaded filename: {downloaded_file_name}")
            return downloaded_file_name

    def extract_still_image_from_video(self, input_filename, output_filename_no_extension):
        output_filename = output_filename_no_extension + ".png"
        self.logger.info(f"Extracting still image from position 30s YouTube video")
        ffmpeg_command = f'{self.ffmpeg_base_command} -i "{input_filename}" -ss 00:00:30 -vframes 1 "{output_filename}"'
        self.logger.debug(f"Running command: {ffmpeg_command}")
        os.system(ffmpeg_command)
        return output_filename

    def convert_to_wav(self, input_filename, output_filename_no_extension):
        output_filename = output_filename_no_extension + ".wav"
        self.logger.info(f"Converting input video to audio WAV file")
        ffmpeg_command = f'{self.ffmpeg_base_command} -i "{input_filename}" "{output_filename}"'
        self.logger.debug(f"Running command: {ffmpeg_command}")
        os.system(ffmpeg_command)
        return output_filename

    def write_lyrics_from_genius(self, artist, title, filename):
        genius = lyricsgenius.Genius(access_token=os.environ["GENIUS_API_TOKEN"], verbose=False, remove_section_headers=True)
        song = genius.search_song(title, artist)
        if song:
            lyrics = self.clean_genius_lyrics(song.lyrics)

            with open(filename, "w") as f:
                f.write(lyrics)

            self.logger.info("Lyrics for %s by %s fetched successfully", title, artist)
            return lyrics.split("\n")
        else:
            self.logger.warning("Could not find lyrics for %s by %s", title, artist)

    def clean_genius_lyrics(self, lyrics):
        lyrics = lyrics.replace("\\n", "\n")
        lyrics = re.sub(r"You might also like", "", lyrics)
        lyrics = re.sub(
            r".*?Lyrics([A-Z])", r"\1", lyrics
        )  # Remove the song name and word "Lyrics" if this has a non-newline char at the start
        lyrics = re.sub(r"^[0-9]* Contributors.*Lyrics", "", lyrics)  # Remove this example: 27 ContributorsSex Bomb Lyrics
        lyrics = re.sub(
            r"See.*Live.*Get tickets as low as \$[0-9]+", "", lyrics
        )  # Remove this example: See Tom Jones LiveGet tickets as low as $71
        lyrics = re.sub(r"[0-9]+Embed$", "", lyrics)  # Remove the word "Embed" at end of line with preceding numbers if found
        lyrics = re.sub(r"(\S)Embed$", r"\1", lyrics)  # Remove the word "Embed" if it has been tacked onto a word at the end of a line
        lyrics = re.sub(r"^Embed$", r"", lyrics)  # Remove the word "Embed" if it has been tacked onto a word at the end of a line
        lyrics = re.sub(r".*?\[.*?\].*?", "", lyrics)  # Remove lines containing square brackets
        # add any additional cleaning rules here
        return lyrics

    def find_best_split_point(self, line):
        """
        Find the best split point in a line based on the specified criteria.
        """

        self.logger.debug(f"Finding best_split_point for line: {line}")
        words = line.split()
        mid_word_index = len(words) // 2

        # Check for a comma within one or two words of the middle word
        if "," in line:
            mid_point = len(" ".join(words[:mid_word_index]))
            comma_indices = [i for i, char in enumerate(line) if char == ","]

            for index in comma_indices:
                if abs(mid_point - index) < 20 and len(line[: index + 1].strip()) <= 36:
                    self.logger.debug(
                        f"Found comma at index {index} which is within 20 characters of mid_point {mid_point} and results in a suitable line length, accepting as split point"
                    )
                    return index + 1  # Include the comma in the first line

        # Check for 'and'
        if " and " in line:
            mid_point = len(line) // 2
            and_indices = [m.start() for m in re.finditer(" and ", line)]
            for index in sorted(and_indices, key=lambda x: abs(x - mid_point)):
                if len(line[: index + len(" and ")].strip()) <= 36:
                    self.logger.debug(f"Found 'and' at index {index} which results in a suitable line length, accepting as split point")
                    return index + len(" and ")

        # Split at the middle word
        self.logger.debug(f"No comma or suitable 'and' found, using middle word as split point")
        return len(" ".join(words[:mid_word_index]))

    def process_line(self, line):
        """
        Process a single line to ensure it's within the maximum length,
        and handle parentheses.
        """
        processed_lines = []
        while len(line) > 36:
            # Check if the line contains parentheses
            if "(" in line and ")" in line:
                start_paren = line.find("(")
                end_paren = line.find(")") + 1
                if end_paren < len(line) and line[end_paren] == ",":
                    end_paren += 1

                if start_paren > 0:
                    processed_lines.append(line[:start_paren].strip())
                processed_lines.append(line[start_paren:end_paren].strip())
                line = line[end_paren:].strip()
            else:
                split_point = self.find_best_split_point(line)
                processed_lines.append(line[:split_point].strip())
                line = line[split_point:].strip()

        if line:  # Add the remaining part if not empty
            processed_lines.append(line)

        return processed_lines

    def write_processed_lyrics(self, lyrics, processed_lyrics_file):
        self.logger.info(f"Writing processed lyrics to {processed_lyrics_file}")

        with open(processed_lyrics_file, "w") as outfile:
            all_processed = False
            while not all_processed:
                all_processed = True
                new_lyrics = []
                for line in lyrics:
                    line = line.strip()
                    processed = self.process_line(line)
                    new_lyrics.extend(processed)
                    if any(len(l) > 36 for l in processed):
                        all_processed = False
                lyrics = new_lyrics

            # Write the processed lyrics to file
            for line in lyrics:
                outfile.write(line + "\n")

    def sanitize_filename(self, filename):
        """Replace or remove characters that are unsafe for filenames."""
        # Replace problematic characters with underscores
        for char in ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]:
            filename = filename.replace(char, "_")
        # Remove any trailing periods or spaces
        filename = filename.rstrip(". ")
        return filename

    def separate_audio(self, audio_file, model_name, instrumental_path, vocals_path):
        if audio_file is None or not os.path.isfile(audio_file):
            raise Exception("Error: Invalid audio source provided.")

        self.logger.debug(f"audio_file is valid file: {audio_file}")

        self.logger.debug(
            f"instantiating Separator with model_name: {model_name} instrumental_path: {instrumental_path} and lossless_output_format: {self.lossless_output_format}"
        )

        from audio_separator.separator import Separator

        separator = Separator(
            log_level=self.log_level,
            log_formatter=self.log_formatter,
            model_file_dir=self.model_file_dir,
            output_format=self.lossless_output_format,
            primary_stem_path=instrumental_path,
            secondary_stem_path=vocals_path,
        )

        separator.load_model(model_name)
        output_files = separator.separate(audio_file)

        self.logger.info(f"Separation complete! Output file(s): {' '.join(output_files)}")

    def setup_output_paths(self, artist, title):
        sanitized_artist = self.sanitize_filename(artist)
        sanitized_title = self.sanitize_filename(title)
        artist_title = f"{sanitized_artist} - {sanitized_title}"

        track_output_dir = self.output_dir
        if self.create_track_subfolders:
            track_output_dir = os.path.join(self.output_dir, f"{artist_title}")

        if not os.path.exists(track_output_dir):
            self.logger.debug(f"Output dir {track_output_dir} did not exist, creating")
            os.makedirs(track_output_dir)

        return track_output_dir, artist_title

    def calculate_text_size_and_position(self, draw, text, font_path, start_size, resolution, padding):
        font_size = start_size
        font = ImageFont.truetype(font_path, size=font_size) if os.path.exists(font_path) else ImageFont.load_default()

        # Initial position for calculating the text bounding box
        temp_position = (padding, padding)
        bbox = draw.textbbox(temp_position, text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        while text_width + 2 * padding > resolution[0] or text_height + 2 * padding > resolution[1]:
            font_size -= 10
            if font_size <= 0:
                raise ValueError("Cannot fit text within screen bounds.")
            font = ImageFont.truetype(font_path, size=font_size) if os.path.exists(font_path) else ImageFont.load_default()
            bbox = draw.textbbox(temp_position, text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

        text_position = ((resolution[0] - text_width) // 2, (resolution[1] - text_height) // 2)
        return font, text_position

    def calculate_text_position(self, draw, text, font, resolution, vertical_offset):
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (resolution[0] - text_width) // 2
        text_y = vertical_offset
        return (text_x, text_y), text_height

    def create_title_video(self, artist, title, format, output_image_filepath, output_video_filepath):
        duration = 5  # Duration in seconds
        resolution = (3840, 2160)  # 4K resolution

        # Load or create background image
        if format["background_image"] and os.path.exists(format["background_image"]):
            self.logger.info(f"Using title screen background image file: {format['background_image']}")
            background = Image.open(format["background_image"])
        else:
            self.logger.info(f"Using title screen background color: {format['background_color']}")
            background = Image.new("RGB", resolution, color=self.hex_to_rgb(format["background_color"]))

        # Resize background to match resolution
        background = background.resize(resolution)

        title = title.upper()
        artist = artist.upper()

        initial_font_size = 500
        top_padding = 950
        title_padding = 400
        artist_padding = 700
        fixed_gap = 150

        draw = ImageDraw.Draw(background)

        # Accessing the font file from the package resources
        with pkg_resources.path("karaoke_prep.resources", format["intro_font"]) as font_path:
            # Calculate positions and sizes for title and artist
            title_font, _ = self.calculate_text_size_and_position(draw, title, str(font_path), initial_font_size, resolution, title_padding)
            artist_font, _ = self.calculate_text_size_and_position(
                draw, artist, str(font_path), initial_font_size, resolution, artist_padding
            )

        # Calculate vertical positions with consistent gap
        title_text_position, title_height = self.calculate_text_position(draw, title, title_font, resolution, top_padding)
        artist_text_position, _ = self.calculate_text_position(
            draw, artist, artist_font, resolution, title_text_position[1] + title_height + fixed_gap
        )

        draw.text(title_text_position, title, fill=format["title_color"], font=title_font)
        draw.text(artist_text_position, artist, fill=format["artist_color"], font=artist_font)

        # Save static background image
        background.save(output_image_filepath)

        # Use ffmpeg to create video
        ffmpeg_command = f'{self.ffmpeg_base_command} -y -loop 1 -framerate 30 -i "{output_image_filepath}" -f lavfi -i anullsrc '
        ffmpeg_command += f'-c:v libx264 -r 30 -t {duration} -pix_fmt yuv420p -vf scale={resolution[0]}:{resolution[1]} -c:a aac -shortest "{output_video_filepath}"'

        self.logger.info("Generating title video...")
        self.logger.debug(f"Running command: {ffmpeg_command}")
        os.system(ffmpeg_command)

    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    def prep_single_track(self):
        if self.artist is None or self.title is None:
            self.logger.warn(f"Artist or Title nor specified manually, guessing from YouTube metadata...")
            self.extract_metadata_from_url()

        artist = self.artist
        title = self.title

        self.logger.info(f"Preparing output path for track: {title} by {artist}")
        track_output_dir, artist_title = self.setup_output_paths(artist, title)
        processed_track = {
            "track_output_dir": track_output_dir,
            "artist": artist,
            "title": title,
        }

        self.logger.info(f"Creating title video...")
        processed_track["title_image"] = os.path.join(track_output_dir, f"{artist_title} (Title).png")
        processed_track["title_video"] = os.path.join(track_output_dir, f"{artist_title} (Title).mov")
        self.create_title_video(artist, title, self.title_format, processed_track["title_image"], processed_track["title_video"])

        lyrics_file = os.path.join(track_output_dir, f"{artist_title} (Lyrics).txt")
        processed_lyrics_file = os.path.join(track_output_dir, f"{artist_title} (Lyrics Processed).txt")
        if os.path.exists(lyrics_file):
            self.logger.debug(f"Lyrics file already exists, skipping fetch: {lyrics_file}")
        else:
            self.logger.info("Fetching lyrics from Genius...")
            lyrics = self.write_lyrics_from_genius(artist, title, lyrics_file)
            self.write_processed_lyrics(lyrics, processed_lyrics_file)

        processed_track["lyrics"] = lyrics_file
        processed_track["processed_lyrics"] = processed_lyrics_file

        # WebM may not always be the output format from YouTubeDL, but it's the most common and this is just a convenience cache
        yt_webm_filename_pattern = os.path.join(track_output_dir, f"{artist_title} (YouTube *.webm")
        yt_webm_glob = glob.glob(yt_webm_filename_pattern)

        yt_png_filename_pattern = os.path.join(track_output_dir, f"{artist_title} (YouTube *.png")
        yt_png_glob = glob.glob(yt_png_filename_pattern)

        yt_wav_filename_pattern = os.path.join(track_output_dir, f"{artist_title} (YouTube *.wav")
        yt_wav_glob = glob.glob(yt_wav_filename_pattern)

        processed_track["youtube_video"] = None
        processed_track["youtube_still_image"] = None
        processed_track["youtube_audio"] = None

        if yt_webm_glob and yt_png_glob and yt_wav_glob:
            processed_track["youtube_video"] = yt_webm_glob[0]
            processed_track["youtube_still_image"] = yt_png_glob[0]
            processed_track["youtube_audio"] = yt_wav_glob[0]

            self.logger.info(f"YouTube output files already exist, skipping download: {processed_track['youtube_video']} + .wav + .png")
        else:
            if self.url is None:
                self.logger.warn(f"No URL specified - the top result from YouTube will be used.")
                self.logger.info("Searching YouTube for video ID...")
                query = f"{artist} {title}"
                youtube_id = self.get_youtube_id_for_top_search_result(query)
            else:
                self.logger.info("Parsing YouTube video ID from URL...")
                youtube_id = self.url.split("watch?v=")[1]
            if youtube_id:
                output_filename_no_extension = os.path.join(track_output_dir, f"{artist_title} (YouTube {youtube_id})")

                self.logger.info("Downloading original video from YouTube...")
                processed_track["youtube_video"] = self.download_video(youtube_id, output_filename_no_extension)

                self.logger.info("Extracting still image from downloaded video...")
                processed_track["youtube_still_image"] = self.extract_still_image_from_video(
                    processed_track["youtube_video"], output_filename_no_extension
                )

                self.logger.info("Converting downloaded video to WAV for audio processing...")
                processed_track["youtube_audio"] = self.convert_to_wav(processed_track["youtube_video"], output_filename_no_extension)
            else:
                self.logger.warning(f"Skipping {title} by {artist} due to missing YouTube ID.")

        self.logger.info(f"Separating audio twice for track: {title} by {artist}")

        instrumental_path = os.path.join(track_output_dir, f"{artist_title} (Instrumental {self.model_name}).{self.lossless_output_format}")
        vocals_path = os.path.join(track_output_dir, f"{artist_title} (Vocals {self.model_name}).{self.lossless_output_format}")

        instrumental_path_lossy = os.path.join(
            track_output_dir, f"{artist_title} (Instrumental {self.model_name}).{self.lossy_output_format}"
        )
        vocals_path_lossy = os.path.join(track_output_dir, f"{artist_title} (Vocals {self.model_name}).{self.lossy_output_format}")

        if os.path.isfile(instrumental_path) and os.path.isfile(vocals_path):
            self.logger.debug(f"Separated audio files already exist in output paths, skipping separation: {instrumental_path}")
        else:
            self.separate_audio(processed_track["youtube_audio"], self.model_name, instrumental_path, vocals_path)
            self.convert_to_lossy(instrumental_path, instrumental_path_lossy)
            self.convert_to_lossy(vocals_path, vocals_path_lossy)

        processed_track["instrumental_audio"] = instrumental_path
        processed_track["vocals_audio"] = vocals_path

        processed_track["instrumental_audio_lossy"] = instrumental_path_lossy
        processed_track["vocals_audio_lossy"] = vocals_path_lossy

        instrumental_path_2 = os.path.join(
            track_output_dir, f"{artist_title} (Instrumental {self.model_name_2}).{self.lossless_output_format}"
        )
        vocals_path_2 = os.path.join(track_output_dir, f"{artist_title} (Vocals {self.model_name_2}).{self.lossless_output_format}")

        instrumental_path_2_lossy = os.path.join(
            track_output_dir, f"{artist_title} (Instrumental {self.model_name_2}).{self.lossy_output_format}"
        )
        vocals_path_2_lossy = os.path.join(track_output_dir, f"{artist_title} (Vocals {self.model_name_2}).{self.lossy_output_format}")

        if os.path.isfile(instrumental_path_2) and os.path.isfile(vocals_path_2):
            self.logger.debug(f"Separated audio files already exist in output paths, skipping separation: {instrumental_path_2}")
        else:
            self.separate_audio(processed_track["youtube_audio"], self.model_name_2, instrumental_path_2, vocals_path_2)
            self.convert_to_lossy(instrumental_path_2, instrumental_path_2_lossy)
            self.convert_to_lossy(vocals_path_2, vocals_path_2_lossy)

        processed_track["instrumental_audio_2"] = instrumental_path_2
        processed_track["vocals_audio_2"] = vocals_path_2

        processed_track["instrumental_audio_2_lossy"] = instrumental_path_2_lossy
        processed_track["vocals_audio_2_lossy"] = vocals_path_2_lossy

        self.logger.info("Script finished, audio downloaded, lyrics fetched and audio separated!")

        return processed_track

    def convert_to_lossy(self, input_filename, output_filename):
        if input_filename is None or not os.path.isfile(input_filename):
            raise Exception(f"Error: Invalid input file provided for convert_to_lossy: {input_filename}")

        self.logger.info(f"Converting {self.lossless_output_format} audio to lossy {self.lossy_output_format} format")

        ffmpeg_extras = "-q:a 0" if self.lossy_output_format == "mp3" else ""

        ffmpeg_command = f'{self.ffmpeg_base_command} -i "{input_filename}" {ffmpeg_extras} "{output_filename}"'
        self.logger.debug(f"Running command: {ffmpeg_command}")
        os.system(ffmpeg_command)

    def is_playlist_url(self):
        """
        Checks if the provided URL is a YouTube playlist URL.
        """
        if self.url and "playlist?list=" in self.url:
            return True
        return False

    def process_playlist(self):
        """
        Processes all videos in a YouTube playlist.
        """
        self.logger.debug(f"Querying playlist metadata from YouTube, assuming consistent artist {self.artist}...")
        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            result = ydl.extract_info(self.url, download=False)
            if "entries" in result:
                track_results = []
                self.logger.info(f"Found {len(result['entries'])} videos in playlist, processing each invididually...")
                for video in result["entries"]:
                    video_url = f"https://www.youtube.com/watch?v={video['id']}"
                    self.logger.info(f"Processing video: {video_url}")
                    self.url = video_url
                    track_results.append(self.prep_single_track())
                    self.artist = self.persistent_artist
                    self.title = None
                return track_results

    def process(self):
        if self.is_playlist_url():
            self.persistent_artist = self.artist
            self.logger.info(
                f"Provided YouTube URL is a playlist, beginning batch operation with persistent artist: {self.persistent_artist}"
            )
            return self.process_playlist()
        else:
            self.logger.info(f"Provided YouTube URL is NOT a playlist, processing single track")
            # TODO: Add support for using karaoke-prep with an existing audio file in any format (e.g. FLAC), not just youtube
            return [self.prep_single_track()]

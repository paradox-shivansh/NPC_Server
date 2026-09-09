import os
import asyncio
import edge_tts
import pygame


class TTSManager:

    def __init__(self):

        self.voice_folder = "voice"

        # create voice folder if missing
        os.makedirs(
            self.voice_folder,
            exist_ok=True
        )

        pygame.mixer.init()


    async def _generate_audio(
        self,
        text,
        voice,
        output_file
    ):

        communicate = edge_tts.Communicate(
            text,
            voice
        )

        await communicate.save(
            output_file
        )


    def speak(
        self,
        character_name,
        text
    ):

        voices = {

            "Eva":
                "en-US-JennyNeural",

            "Freddy":
                "en-US-GuyNeural",

            "John":
                "en-GB-RyanNeural"

        }


        voice = voices.get(
            character_name,
            "en-US-JennyNeural"
        )


        # unique file name
        filename = (
            f"{character_name}_speech.mp3"
        )


        output_file = os.path.join(
            self.voice_folder,
            filename
        )


        try:

            asyncio.run(
                self._generate_audio(
                    text,
                    voice,
                    output_file
                )
            )


            pygame.mixer.music.load(
                output_file
            )

            pygame.mixer.music.play()


            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)



        except Exception as e:

            print(
                f"⚠️ TTS failed: {e}"
            )

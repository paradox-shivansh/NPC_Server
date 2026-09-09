import asyncio
import edge_tts
import pygame
import os
import uuid


class TTSManager:

    def __init__(self):
        pygame.mixer.init()

        self.voices = {

            "Eva": "en-US-AriaNeural",

            "Freddy": "en-US-GuyNeural",

            "John": "en-US-DavisNeural"

        }


    async def _generate_audio(
        self,
        text,
        voice,
        output_file
    ):

        communicate = edge_tts.Communicate(
            text=text,
            voice=voice
        )

        await communicate.save(output_file)



    def speak(
        self,
        character_name,
        text
    ):

        try:

            voice = self.voices.get(
                character_name,
                "en-US-AriaNeural"
            )


            filename = (
                f"tts_{uuid.uuid4()}.mp3"
            )


            asyncio.run(
                self._generate_audio(
                    text,
                    voice,
                    filename
                )
            )


            pygame.mixer.music.load(
                filename
            )

            pygame.mixer.music.play()


            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)


            pygame.mixer.music.unload()


            os.remove(filename)



        except Exception as e:

            print(
                "⚠️ TTS failed:",
                e
            )

            print(
                "Continuing simulation..."
            )
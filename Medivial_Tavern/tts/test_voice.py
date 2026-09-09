import edge_tts
import asyncio


async def main():

    communicate = edge_tts.Communicate(
        text="Hello, I am Eva from the medieval tavern.",
        voice="en-US-AriaNeural"
    )

    await communicate.save(
        "eva_test.mp3"
    )


asyncio.run(main())
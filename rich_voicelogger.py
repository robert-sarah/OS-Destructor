#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rich Voicelogger - Audio Recording Tool
Professional voice/audio recording with Rich console
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
import pyaudio
import wave
from datetime import datetime
import os

console = Console()

class RichVoicelogger:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.RECORD_SECONDS = 10
        self.start_time = None
        
    def record_audio(self, duration=10):
        """Record audio for specified duration"""
        self.RECORD_SECONDS = duration
        self.start_time = datetime.now()
        
        console.print(Panel.fit(
            "[bold cyan]Rich Voicelogger[/bold cyan]\n"
            f"Recording for {duration} seconds...",
            border_style="cyan"
        ))
        
        audio = pyaudio.PyAudio()
        
        stream = audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        frames = []
        
        with Progress(console=console) as progress:
            task = progress.add_task("[green]Recording...", total=duration)
            
            for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
                data = stream.read(self.CHUNK)
                frames.append(data)
                if i % 44 == 0:  # Update roughly every second
                    progress.update(task, advance=1)
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"voice_recording_{timestamp}.wav"
        
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(audio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        # Display stats
        table = Table(title="Recording Complete")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Duration", f"{duration} seconds")
        table.add_row("Filename", filename)
        table.add_row("Sample Rate", str(self.RATE))
        table.add_row("Channels", str(self.CHANNELS))
        
        console.print(table)
        console.print(f"\n[green]✓ Audio saved to: {filename}[/green]")
        
        return filename

if __name__ == "__main__":
    console.print(Panel.fit(
        "[bold cyan]Rich Voicelogger[/bold cyan]\n"
        "Professional audio recording tool"
    ))
    
    logger = RichVoicelogger()
    logger.record_audio(duration=10)


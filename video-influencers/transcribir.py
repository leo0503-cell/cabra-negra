"""Transcribe los videos fuente con marcas de tiempo por palabra."""
import json
from pathlib import Path
import subprocess
import imageio_ffmpeg
import numpy as np
from faster_whisper import WhisperModel


def pcm(v):
    b = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", str(v), "-ac", "1", "-ar", "16000",
                        "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.float32)


R = Path(__file__).parent
m = WhisperModel("small", device="cpu", compute_type="int8")
for v in sorted((R / "fuentes/videos").glob("v*.mp4")):
    segs, _ = m.transcribe(pcm(v), language="es", word_timestamps=True, vad_filter=False,
                           initial_prompt="Cabra Negra, cabranegramx, mandil, tabla, parrilla")
    out = []
    for s in segs:
        out.append(dict(ini=s.start, fin=s.end, texto=s.text,
                        palabras=[(w.start, w.end, w.word) for w in s.words]))
    (R / "transcripciones" / f"{v.stem}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"== {v.stem}")
    for s in out:
        print(f"  {s['ini']:5.1f}-{s['fin']:5.1f} {s['texto']}")

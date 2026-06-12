# -*- coding: utf-8 -*-
"""百炼 CosyVoice 声音克隆：曾志伟 → 沙尘猫"""
import sys
import json
import time
from dashscope.audio.tts_v2 import VoiceEnrollmentService, SpeechSynthesizer

REF_URL = "https://libtv-res.liblib.art/claw/8b3b169b03734516a0c5ebdae4bcd23e/7aaf0e6b-0068-4155-92ba-cf29efe45ffe.mp4"
MODEL = "cosyvoice-v3.5-plus"

def create_voice():
    svc = VoiceEnrollmentService()
    result = svc.create_voice(
        target_model=MODEL,
        prefix="shachen",
        url=REF_URL,
        language_hints=["zh"]
    )
    print(f"[create_voice] {json.dumps(result, ensure_ascii=False) if not isinstance(result, str) else result}")
    if isinstance(result, str):
        return result
    return result.get("voice_id") or result.get("output", {}).get("voice_id")

def query_voice(voice_id):
    svc = VoiceEnrollmentService()
    result = svc.query_voice(voice_id=voice_id)
    print(f"[query_voice] {json.dumps(result, ensure_ascii=False)}")
    return result

def synthesize(voice_id, text, output_path):
    synth = SpeechSynthesizer(model=MODEL, voice=voice_id)
    result = synth.call(text)
    if isinstance(result, bytes):
        with open(output_path, "wb") as f:
            f.write(result)
        print(f"[synthesize] saved {len(result)} bytes → {output_path}")
    else:
        print(f"[synthesize] {json.dumps(result, ensure_ascii=False)}")
        if result.get("audio"):
            import base64
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(result["audio"]))
            print(f"[synthesize] saved from base64 → {output_path}")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"

    if cmd == "create":
        vid = create_voice()
        if vid:
            print(f"VOICE_ID={vid}")
            # Save for later
            with open("c:/Users/Brian/xundao/characters/沙尘/voice_id.txt", "w") as f:
                f.write(vid)

    elif cmd == "query":
        vid = sys.argv[2] if len(sys.argv) > 2 else open("c:/Users/Brian/xundao/characters/沙尘/voice_id.txt").read().strip()
        info = query_voice(vid)
        status = info.get("status") or info.get("output", {}).get("status")
        print(f"Status: {status}")

    elif cmd == "synth":
        vid = sys.argv[2] if len(sys.argv) > 2 else open("c:/Users/Brian/xundao/characters/沙尘/voice_id.txt").read().strip()
        text = "我唔理——you guys自己搞掂——that woman背脊嗰啲嘢我唔敢搞㗎——咪望我"
        if len(sys.argv) > 3:
            text = sys.argv[3]
        out = sys.argv[4] if len(sys.argv) > 4 else "c:/Users/Brian/xundao/characters/沙尘/shachen_test.wav"
        synthesize(vid, text, out)

    else:  # all
        print("=== Step 1: Create Voice ===")
        vid = create_voice()
        if not vid:
            print("FAILED to create voice")
            sys.exit(1)
        print(f"Voice ID: {vid}")

        print("\n=== Step 2: Poll until ready ===")
        for i in range(20):
            time.sleep(3)
            info = query_voice(vid)
            status = (info.get("output", {}) or info).get("status", "")
            print(f"  poll {i+1}: status={status}")
            if status in ("OK", "ok", "ready", "completed"):
                break
            elif status in ("FAILED", "failed", "error"):
                print(f"FAILED: {json.dumps(info, ensure_ascii=False)}")
                sys.exit(1)

        print("\n=== Step 3: Synthesize ===")
        text = "我唔理——you guys自己搞掂——that woman背脊嗰啲嘢我唔敢搞㗎——咪望我"
        synthesize(vid, text, "c:/Users/Brian/xundao/characters/沙尘/shachen_test.wav")
        print("\nDone! Check: c:/Users/Brian/xundao/characters/沙尘/shachen_test.wav")

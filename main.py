import openai
import sounddevice as sd
from scipy.io.wavfile import write
import os
import random
import csv


openai.api_key = "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"


file_path = "sentences.csv" 
def load_tongue_twisters(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        return [row[0] for row in reader]


def record_audio(filename, duration=5):
    print(f"เริ่มบันทึกเสียง (พูดใน {duration} วินาที)...")
    sample_rate = 44100
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    write(filename, sample_rate, recording)
    print("การบันทึกเสร็จสิ้น!")


def transcribe_audio(filename):
    try:
        with open(filename, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]
    except Exception as e:
        print("เกิดข้อผิดพลาด:", e)
        return None


def tongue_twister_game():
    tongue_twisters = load_tongue_twisters("sentences.csv")
    random.shuffle(tongue_twisters)
    score = 0

    for i, sentence in enumerate(tongue_twisters[:10], 1):
        print(f"\nข้อที่ {i}: {sentence}")
        input("กด Enter เพื่อเริ่มการบันทึกเสียง...")
        record_audio("user_audio.wav", duration=10)
        result = transcribe_audio("user_audio.wav")
        print(f"\nคุณพูดว่า: {result}")
        if result:
            accuracy = calculate_accuracy(sentence, result)
            print(f"ความแม่นยำ: {accuracy:.2f}%")
            if accuracy > 70:  # เกณฑ์ผ่าน 70%
                print("ผ่าน! +1 คะแนน")
                score += 1
            else:
                print("ยังไม่ผ่าน ลองใหม่ในครั้งหน้า!")
        else:
            print("ไม่สามารถวิเคราะห์เสียงได้")

    print(f"\nคะแนนรวม: {score}/10")


def calculate_accuracy(original, spoken):
    original_words = set(original.lower().split())
    spoken_words = set(spoken.lower().split())
    common_words = original_words.intersection(spoken_words)
    return len(common_words) / len(original_words) * 100


if __name__ == "__main__":
    tongue_twister_game()



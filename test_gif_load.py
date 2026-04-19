from PIL import Image

try:
    img = Image.open("C:\Users\avars\OneDrive\Desktop\JarvisAI\gui\waveform.gif")  # adjust relative path
    print("✅ GIF loaded successfully!")
    img.show()
except Exception as e:
    print("❌ Error loading GIF:", e)

# Generate a simple PNG mascot image for the assistant "Zarya"
from PIL import Image, ImageDraw

size = 512
img = Image.new("RGBA", (size, size), (0,0,0,0))
draw = ImageDraw.Draw(img)

# body
draw.ellipse((96, 96, 416, 416), fill=(230,230,255,255))

# face
draw.ellipse((176, 200, 336, 340), fill=(255,255,255,255))

# eyes
draw.ellipse((210, 240, 240, 270), fill=(60,60,120,255))
draw.ellipse((272, 240, 302, 270), fill=(60,60,120,255))

# mouth
draw.arc((230, 280, 290, 320), start=0, end=180, fill=(60,60,120,255), width=4)

# small antenna
draw.line((256, 80, 256, 96), fill=(120,120,200,255), width=6)
draw.ellipse((242, 60, 270, 88), fill=(120,120,200,255))

path = "zarya_assistant.png"
img.save(path)

path
# Generate two PNG images for the assistant mascot "Zarya":
# 1) idle (eyes open)
# 2) blink (eyes closed)
from PIL import Image, ImageDraw

size = 512

def draw_base(face=True, eyes="open"):
    img = Image.new("RGBA", (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)

    # body
    draw.ellipse((96, 96, 416, 416), fill=(230,230,255,255))

    # face
    draw.ellipse((176, 200, 336, 340), fill=(255,255,255,255))

    if eyes == "open":
        draw.ellipse((210, 240, 240, 270), fill=(60,60,120,255))
        draw.ellipse((272, 240, 302, 270), fill=(60,60,120,255))
    elif eyes == "closed":
        draw.line((210,255,240,255), fill=(60,60,120,255), width=6)
        draw.line((272,255,302,255), fill=(60,60,120,255), width=6)

    # mouth
    draw.arc((230, 280, 290, 320), start=0, end=180, fill=(60,60,120,255), width=4)

    # antenna
    draw.line((256, 80, 256, 96), fill=(120,120,200,255), width=6)
    draw.ellipse((242, 60, 270, 88), fill=(120,120,200,255))

    return img

idle = draw_base(eyes="open")
blink = draw_base(eyes="closed")

idle_path = "zarya_idle.png"
blink_path = "zarya_blink.png"

idle.save(idle_path)
blink.save(blink_path)

idle_path, blink_path
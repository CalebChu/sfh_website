from PIL import Image

dominant = (245, 244, 242, 255)
accent = (24, 25, 27, 255)
accent_t = (24, 25, 27, int(0.451*255)) 
secondary = (178, 222, 240, 255)
secondaryg = (158, 203, 174, 255)
yellow = (255, 221, 60, 255)
red = (255, 105, 97, 255) 

# names = {"search": dominant, "announcement": dominant, "trophy": dominant, "calendar": dominant}
# names = {"user": accent_t, "trophy": accent_t}
# names = {"options": accent_t}
names = {"podium": red}

for name, color in names.items():
    img = Image.open(f"{name}.png")
    px = img.load()
    out = Image.new('RGBA', img.size, 0xffffff)


    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b, a = px[x, y]
            if not a == 0:
                out.putpixel((x, y), color)
            else:
                out.putpixel((x, y), (r, g, b, a))

    out.save(f'{name}-r.png')
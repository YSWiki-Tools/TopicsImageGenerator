from PIL import Image, ImageOps, ImageDraw, ImageFont
from json import load
import configparser

config = configparser.ConfigParser()
config.read('config.ini', "utf-8")

topics, students = [], []
is_eighties = config["MAIN"].getboolean("is_eighties")

with (open(config["MAIN"]["streaming_assets_path"]+f"/JSON/{'EightiesTopics' if is_eighties else 'Topics'}.json", encoding="UTF-8") as topics_file,
      open(config["MAIN"]["streaming_assets_path"]+f"/JSON/{'Eighties' if is_eighties else 'Students'}.json", encoding="UTF-8") as students_file):
    topics = load(topics_file)
    students = load(students_file)

SCALE_CONST = 0.85
photo_xy = (36, 117)
vstart, hstart = 77, 72
hdist, vdist = 89, 107
pattern = Image.open("Background.png")
neg = Image.open("1.png")
pos = Image.open("2.png")

for i in range(len(topics)-3):
    p = pattern.copy()
    for j in range(1, 26):
        if topics[i][str(j)] == "1":
            p.paste(neg, (512 + hstart + hdist*((j-1) % 5), vstart + vdist*((j-1) // 5) - (j-1) // 8), neg)
        if topics[i][str(j)] == "2":
            p.paste(pos, (512 + hstart + hdist*((j-1) % 5), vstart + vdist*((j-1) // 5) - (j-1) // 8), pos)
    photo = Image.open(config['MAIN']['streaming_assets_path'] + f"/Portraits{'1989' if is_eighties else ''}/Student_{i+1}.png")
    p.paste(ImageOps.scale(photo, SCALE_CONST), photo_xy)
    draw_text = ImageDraw.Draw(p)

    draw_text.text(
        (264,44 + ((not bool(students[i]["RealName"])) * 20)),
        students[i]["Name"],
        fill=('#dc99d1'),
        font=ImageFont.truetype("Futura Condensed Medium.otf", 50 + ((not bool(students[i]["RealName"])) * 20)),
        anchor="ms",
        )
    draw_text.text(
        (260,40 + ((not bool(students[i]["RealName"])) * 20)),
        students[i]["Name"],
        fill=('#ffffff'),
        font=ImageFont.truetype("Futura Condensed Medium.otf", 50 + ((not bool(students[i]["RealName"])) * 20)),
        anchor="ms",
        )
    if students[i]["RealName"]:
        draw_text.text(
            (263,73),
            "Real name: " + students[i]["RealName"],
            fill=('#dc99d1'),
            font=ImageFont.truetype("Futura Condensed Medium.otf", 30),
            anchor="ms",
            )
        draw_text.text(
            (260,70),
            "Real name: " + students[i]["RealName"],
            fill=('#ffffff'),
            font=ImageFont.truetype("Futura Condensed Medium.otf", 30),
            anchor="ms",
            )
    if len(students[i]["Class"]) == 2:
        draw_text.text(
            (262,107),
            "Class " + students[i]["Class"][0]+"-"+students[i]["Class"][1],
            fill=('#dc99d1'),
            font=ImageFont.truetype("Futura Condensed Medium.otf", 30),
            anchor="ms",
            )
        draw_text.text(
            (260,105),
            "Class " + students[i]["Class"][0]+"-"+students[i]["Class"][1],
            fill=('#ffffff'),
            font=ImageFont.truetype("Futura Condensed Medium.otf", 30),
            anchor="ms",
            )
    p.save(f"{config['MAIN']['resultfolder_path']}/Интересы {students[i]['Name'].split()[0]}.png")
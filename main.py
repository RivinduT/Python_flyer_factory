import os
from PIL import Image, ImageFont, ImageDraw

UniDictionary = {
    "SJP": "University of Sri Jayewardenepura - SJP",
    "COL": "University of Colombo - COL",
    "PER": "University of Peradeniya - PER",
    "KEL": "University of Kelaniya - KEL",
    "JAF": "University of Jaffna - JAF",
    "MOR": "University of Moratuwa - MOR",
    "RUH": "University of Ruhuna - RUH",
    "VAU": "University of Vavuniya - VAU",
    "VAV": "University of Vavuniya - VAU",
    "SAB": "Sabaragamuwa University of Sri Lanka - SAB",
    "WAY": "Wayamba University of Sri Lanka - WAY",
    "RAJ": "Rajarata University of Sri Lanka - RAJ",
    "UVA": "Uva Wellassa University - UVA",
    "UVU": "Uva Wellassa University - UVA",
    "EST": "Eastern University of Sri Lanka - EST",
    "SEU": "South Eastern University of Sri Lanka - SEU",
    "SEA": "South Eastern University of Sri Lanka - SEU",
    "VPA": "University of Visual & Performing Arts - VPA",
    "GWU": "Gampaha Wickramarachchi University - GWU",
    "GWA": "Gampaha Wickramarachchi University - GWU"
}

dir_path = os.path.dirname(os.path.realpath(__file__))

def getUniLogo(uniNameShort):
    if UniDictionary.get(uniNameShort) is None:
        print(f'Error in excel file. Please check the name of {uniNameShort}')
        exit()
    else:
        uniName = UniDictionary.get(uniNameShort)
    
    if len(uniName.split(" - ")) > 1:
        uniTag = uniName.split(" - ")[1]
    else:
        uniTag = uniName.split(" - ")[1]

    uniLogo = Image.open(f'{dir_path}/uni_logos/{uniTag}.png').convert("RGBA")
    uniLogo = uniLogo.resize((200, 200))
    return (uniTag, uniLogo)

sportName = input("Enter the sport name: ").lower()
numOfGames = int(input("Enter the number of games: "))
if numOfGames > 4:
    print("Error! Maximum number of games is 4")
    exit()

scoresFont = ImageFont.truetype(f'{dir_path}/fonts/DrukTextWide-MediumItalic-Trial.otf', 175)
uniNameFont = ImageFont.truetype(f'{dir_path}/fonts/DrukTextWide-MediumItalic-Trial.otf', 42)
winningFont = ImageFont.truetype(f'{dir_path}/fonts/DrukTextWide-HeavyItalic-Trial.otf', 60)
customTextFont = ImageFont.truetype(f'{dir_path}/fonts/DrukTextWide-MediumItalic-Trial.otf', 50)
customTextFont2 = ImageFont.truetype(f'{dir_path}/fonts/DrukTextWide-MediumItalic-Trial.otf', 35)

custom_texts = []

# creating each score card
for i in range(numOfGames):
    templateScore = Image.open(f'{dir_path}/imgs/scoresBG.png').convert("RGBA")
    editable_templateScore = ImageDraw.Draw(templateScore) 
    custom_text = input(f"Enter the custom text for match {i+1} (ex: Men's Preliminary Group A): ")
    custom_texts.append(custom_text)
    uniNames = input(f"Enter the names of the universities for match {i+1} (ex: SJP EST): ")
    un1, un2 = uniNames.split(" ")
    un1 = un1.upper()
    un2 = un2.upper()
    scores = input(f"Enter the scores of {un1} and {un2} for match {i+1} (ex: 01 02): ")
    s1, s2 = map(int, scores.split(" "))  # Convert scores to integers

    if s1 > s2:
        winningTeam = un1
    else:
        winningTeam = un2

    isWinningTeam = "y"
    if isWinningTeam == "y":
        winningTeam = winningTeam.upper()
    else:
        print("Some inputs may be wrong!!")
        exit()

    winningTeam += " WON"

    uni1, uniLogo1 = getUniLogo(un1)
    uni2, uniLogo2 = getUniLogo(un2)

    templateScore.paste(uniLogo1, (177, 116), uniLogo1)
    templateScore.paste(uniLogo2, (1315, 116), uniLogo2)

    # Measure the width of the text
    bbox = editable_templateScore.textbbox((0, 0), uni1, font=uniNameFont)
    text_width = bbox[2] - bbox[0]

    # Calculate the starting x-coordinat3
    start_x = 790 - text_width

    # Draw the text at the calculated position
    editable_templateScore.text((start_x, 89), uni1, (255, 255, 255), uniNameFont)
    editable_templateScore.text((900, 89), uni2, (255, 255, 255), uniNameFont)

    # Format scores with leading zeros
    s1_str = str(s1)
    s2_str = str(s2)

    # Measure the bounding box of the text
    bbox = editable_templateScore.textbbox((0, 0), s1_str, font=scoresFont)
    text_width = bbox[2] - bbox[0]

    # Calculate the starting x-coordinate
    start_x = 745 - text_width

    # Draw the text at the calculated position
    editable_templateScore.text((start_x, 136), s1_str, (12, 50, 109), font=scoresFont)
    editable_templateScore.text((931, 136), s2_str, (12, 50, 109), scoresFont)

    # Measure the bounding box of the text
    bbox = editable_templateScore.textbbox((0, 0), winningTeam, font=winningFont)
    text_width = bbox[2] - bbox[0]

    # Calculate the center x-coordinate of the image
    W, H = templateScore.size
    center_x = W // 2

    # Calculate the starting x-coordinate for center alignment
    start_x = center_x - (text_width // 2)

    # Draw the text at the calculated position
    editable_templateScore.text((630, 290), winningTeam, (250, 250, 250), font=winningFont)
    
    templateScore.save(f'{dir_path}/results/match{i}.png')

    print(f'{i+1} of {numOfGames} result created!')

background = Image.open(f'{dir_path}/imgs/{sportName}BG.jpg').convert("RGBA")
W, H = background.size

conut = 1
if numOfGames == 1:
    for i in range(numOfGames):
        match = Image.open(f'{dir_path}/results/match{i}.png').convert("RGBA")
        w, h = match.size
        y_offset = (H - h) // 2 + 100 # Center the scorecard vertically
        draw = ImageDraw.Draw(background)
        bbox = draw.textbbox((0, 0), custom_texts[i], font=customTextFont)
        text_width = bbox[2] - bbox[0]
        draw.text(((W - text_width) / 2, y_offset - 20), custom_texts[i], (255, 255, 255), font=customTextFont)
        background.paste(match, (int((W - w) / 2), y_offset), match)
        conut += 1
        print(f'{conut} of {numOfGames} result pasted!')

elif numOfGames == 2:
    for i in range(numOfGames):
        match = Image.open(f'{dir_path}/results/match{i}.png').convert("RGBA")
        w, h = match.size
        y_offset = 750 + i * (h + 50)
        draw = ImageDraw.Draw(background)
        bbox = draw.textbbox((0, 0), custom_texts[i], font=customTextFont)
        text_width = bbox[2] - bbox[0]
        draw.text(((W - text_width) / 2, y_offset - 20), custom_texts[i], (255, 255, 255), font=customTextFont)
        background.paste(match, (int((W - w) / 2), y_offset), match)
        conut += 1
        print(f'{conut} of {numOfGames} result pasted!')

elif numOfGames == 3:
    for i in range(numOfGames):
        match = Image.open(f'{dir_path}/results/match{i}.png').convert("RGBA")
        w, h = match.size
        y_start = 600
        y_end = 1950
        total_height = y_end - y_start
        gap = (total_height - (h * numOfGames)) // (numOfGames - 1)
        y_offset = y_start + i * (h + gap)
        draw = ImageDraw.Draw(background)
        bbox = draw.textbbox((0, 0), custom_texts[i], font=customTextFont)
        text_width = bbox[2] - bbox[0]
        draw.text(((W - text_width) / 2, y_offset - 4), custom_texts[i], (255, 255, 255), font=customTextFont)
        background.paste(match, (int((W - w) / 2), y_offset), match)
        conut += 1
        print(f'{conut} of {numOfGames} result pasted!')

elif numOfGames == 4:
    for i in range(numOfGames):
        match = Image.open(f'{dir_path}/results/match{i}.png').convert("RGBA")
        w, h = match.size
        w = int(w * 0.85)
        h = int(h * 0.85)
        y_start = 550
        y_end = 1950
        total_height = y_end - y_start
        gap = (total_height - (h * numOfGames)) // (numOfGames - 1)
        y_offset = y_start + i * (h + gap)
        draw = ImageDraw.Draw(background)
        bbox = draw.textbbox((0, 0), custom_texts[i], font=customTextFont2)
        text_width = bbox[2] - bbox[0]
        draw.text(((W - text_width) / 2, y_offset + 10), custom_texts[i], (255, 255, 255), font=customTextFont2)
        match = match.resize((w, h), Image.Resampling.LANCZOS)
        background.paste(match, (int((W - w) / 2), y_offset), match)
        conut += 1
        print(f'{conut} of {numOfGames} result pasted!')

background.save(f'{dir_path}/final.png')

print("Exit..")
exit()
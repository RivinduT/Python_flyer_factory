import os
import pandas as pd
from PIL import Image, ImageFont, ImageDraw

UniDictionary = {"SJP" : "University of Sri Jayewardenepura - SJP",
"COL" : "University of Colombo - COL",
"PER":"University of Peradeniya - PER",
"KEL":"University of Kelaniya - KEL",
"JAF":"University of Jaffna - JAF",
"MOR":"University of Moratuwa - MOR",
"RUH":"University of Ruhuna - RUH",
"VAU":"University of Vavuniya - VAU",
"VAV":"University of Vavuniya - VAU",
"SAB":"Sabaragamuwa University of Sri Lanka - SAB",
"WAY":"Wayamba University of Sri Lanka - WAY",
"RAJ":"Rajarata University of Sri Lanka - RAJ",
"UVA":"Uva Wellassa University - UVA",
"UVU":"Uva Wellassa University - UVA",
"EST":"Eastern University of Sri Lanka - EST",
"SEU":"South Eastern University of Sri Lanka - SEU",
"SEA":"South Eastern University of Sri Lanka - SEU",
"VPA":"University of Visual & Performing Arts - VPA",
"GWU":"Gampaha Wickramarachchi University - GWU",
"GWA":"Gampaha Wickramarachchi University - GWU"
}

dir_path = os.path.dirname(os.path.realpath(__file__))

numOfGames = input("Enter the number of games: ")

print("running...")

try:
    df = pd.read_excel(f'{dir_path}/pointsTable.xlsx')
except FileNotFoundError:
    print("Error: The file 'Book1.xlsx' was not found. Please check the file path and try again.")
    exit()
except pd.errors.EmptyDataError:
    print("Error: The file 'Book1.xlsx' is empty. Please provide a valid Excel file.")
    exit()
except Exception as e:
    print(f"Error: An unexpected error occurred: {e}")
    exit()

nameList = df["Name"]
menScores = df["Men"]
womenScores = df["Women"]
totalScores = df["Total"]
rank = df["Rank"].tolist()

length = len(df)

templateImage = Image.open(f'{dir_path}/leaderboard BG.png')
W,H = templateImage.size

editable_image = ImageDraw.Draw(templateImage)

font = ImageFont.truetype(f'{dir_path}/fonts/Montserrat-SemiBold.ttf',18)
boldFont = ImageFont.truetype(f'{dir_path}/fonts/Montserrat-SemiBold.ttf',20)
boldFont2 = ImageFont.truetype(f'{dir_path}/fonts/DrukTextWide-MediumItalic-Trial.otf',15)

count = 0

for i in range(length):
    uniNameShort = nameList[i].upper()
    men = menScores[i]
    women = womenScores[i]
    total = totalScores[i]

    if UniDictionary.get(uniNameShort) == None:
        print(f'Error in excel file. Please check the name of {uniNameShort}')
        exit()
    else:
        uniName = UniDictionary.get(uniNameShort)

    if len(uniName.split(" - ")) > 1:
        uniTag = uniName.split(" - ")[1]
    else:
        uniTag = uniName.split(" - ")[1]

    uniLogo = Image.open(f'{dir_path}/uni_logos/{uniTag}.png').convert("RGBA")

    uniLogo = uniLogo.resize((30,30))

    templateImage.paste(uniLogo,(175,(217+(count*50))),uniLogo)


    editable_image.text((220,(220+(count*50))),uniName,(0,0,0),font)
    editable_image.text((745,(220+(count*50))),str(men),(0,0,0),font)
    editable_image.text((820,(220+(count*50))),str(women),(0,0,0),font)
    editable_image.text((890,(220+(count*50))),str(total),(0,0,0),font)
    editable_image.text((125,(225+(count*50))),str(rank[i]),(255,255,255),boldFont2)
    

    print(f'{i+1} of {length} invitations created!')
    count += 1

#afterText = f"After completion of {numOfGames} games".upper()
#tw = editable_image.textlength(afterText,font=boldFont2)
#editable_image.text((int((W-tw)/2),150),afterText,(10,51,107),boldFont2)


templateImage.save(f'{dir_path}/after{numOfGames}games.png')




print("Exit..")
exit()
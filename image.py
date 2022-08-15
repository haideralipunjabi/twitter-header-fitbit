import io
from urllib import request
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime as dt
from datetime import timedelta as td
import requests

FA_FONT = ImageFont.truetype('fonts/Font Awesome 6 Free-Solid-900.otf', 40)

STATS_TITLE_SIZE = 40
STATS_SUBTITLE_SIZE = 18
STATS_FONT_JURA = ImageFont.truetype('fonts/Jura-Regular.ttf', STATS_TITLE_SIZE)
STATS_FONT_KALAM = ImageFont.truetype('fonts/Kalam-Regular.ttf', STATS_TITLE_SIZE)

ACTIVITY_SIZE = 30
ACTIVITY_FONT_JURA = ImageFont.truetype('fonts/Jura-Regular.ttf', ACTIVITY_SIZE)
ACTIVITY_FONT_KALAM = ImageFont.truetype('fonts/Kalam-Regular.ttf', ACTIVITY_SIZE)

def get_coordinates_stats(x,y,offsetX=0, offsetY=0):
    orgX = 100
    orgY = 100
    xGap = 210
    yGap = 70
    return (orgX + (x * xGap) + offsetX, orgY + (y*yGap) + offsetY)


def get_coordinates_activites(x,y,offsetX=0, offsetY=0):
    orgX = 420
    orgY = 350
    xGap = 210
    yGap = 40
    return (orgX + (x * xGap) + offsetX, orgY + (y*yGap) + offsetY)

class ImageGenerator():
    def __init__(self):
        self.image = Image.new("RGB",(1500,500))
        self.draw = ImageDraw.Draw(self.image)

    # Apply the background image
    def background(self, fp):
        bg = Image.open(fp)
        bg = bg.resize((3087,2315))
        self.image.paste(bg, (-152,-1121))
        self.write_text((750,480), "Header generated using code. Check pinned tweet for details.", ACTIVITY_FONT_JURA.font_variant(size=20), "#FFFFFF")
        self.write_text((1400,480), "#FitDevs",ACTIVITY_FONT_KALAM.font_variant(size=25), "#FFFFFF")

    # Wrapper function to use some default values
    def write_text(self,xy, text,font=None, fill="#222222", anchor='mm', align='center'):
        self.draw.text(xy=xy,text=str(text),fill=fill,font=font,anchor=anchor,align=align)

    def write_stats(self, todays, best, lifetime):
        self.write_text(get_coordinates_stats(1,-1), '', FA_FONT)
        self.write_text(get_coordinates_stats(2,-1), '', FA_FONT)
        self.write_text(get_coordinates_stats(0,0, offsetX=70), 'Today', STATS_FONT_KALAM, anchor='rm')
        self.write_text(get_coordinates_stats(1,0), todays['steps'], STATS_FONT_JURA)
        self.write_text(get_coordinates_stats(2,0), f"{round(todays['distance'],2)} km", STATS_FONT_JURA)
        self.write_text(get_coordinates_stats(0,1, offsetX=70), 'Best', STATS_FONT_KALAM, anchor='rm')
        self.write_text(get_coordinates_stats(1,1), f"{best['steps']['value']}", STATS_FONT_JURA)
        self.write_text(get_coordinates_stats(1,1, offsetY=25), f"{dt.strptime(best['steps']['date'], '%Y-%m-%d').strftime('%b %d, %Y')}", STATS_FONT_JURA.font_variant(size=STATS_SUBTITLE_SIZE))
        self.write_text(get_coordinates_stats(2,1), f"{round(best['distance']['value'], 2)} km", STATS_FONT_JURA)
        self.write_text(get_coordinates_stats(2,1, offsetY=25), f"{dt.strptime(best['distance']['date'], '%Y-%m-%d').strftime('%b %d, %Y')}", STATS_FONT_JURA.font_variant(size=STATS_SUBTITLE_SIZE))
        self.write_text(get_coordinates_stats(0,2, offsetX=70),'Lifetime', STATS_FONT_KALAM, anchor='rm')
        self.write_text(get_coordinates_stats(1,2), lifetime['steps'], STATS_FONT_JURA)
        self.write_text(get_coordinates_stats(2,2), f"{lifetime['distance']} km", STATS_FONT_JURA)

    def write_activities(self,activities):
        for i,activity in enumerate(activities):
            self.write_text(get_coordinates_activites(0,i), activity['name'], ACTIVITY_FONT_KALAM)
            date =  dt.fromisoformat(activity["startTime"]).strftime('%d %b, %I:%M %p')
            self.write_text(get_coordinates_activites(1,i), date, ACTIVITY_FONT_JURA)
            duration = td(milliseconds=activity["duration"])
            self.write_text(get_coordinates_activites(2,i), duration, ACTIVITY_FONT_JURA)
            self.write_text(get_coordinates_activites(3,i, offsetX=-70), f'{activity["calories"]} cals', ACTIVITY_FONT_JURA)

    def draw_followers(self,images):
        self.write_text((940,70), 'Latest Followers:', STATS_FONT_KALAM)
        for i,url in enumerate(images):
            image = Image.open(io.BytesIO(requests.get(url).content))
            image = image.resize((50,50))
            self.image.paste(image,(1100 + (i * 60),40))

    def save(self,fp):
        self.image.save(fp)


if __name__ == "__main__":
    i = ImageGenerator()
    i.write_stats({},{},{})
    i.save()
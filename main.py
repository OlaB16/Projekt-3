# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.garden.mapview import MapView, MapMarker
from math import sqrt, pi, sin, cos, atan, tan, atan2
import random

Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'Show me on the map'
            on_press: root.manager.current = 'showme'
        Button:
            text: 'Flags of countries'
            on_press: root.manager.current = 'flags'

<ShowMeScreen>:
    search_lat: coor_lat
	search_long: coor_long
	my_map: map
	my_image: image
	my_score: score
    GridLayout:
        rows: 4
        cols: 1
        BoxLayout:
            size_hint_y: 1
            
            MapView:
                lat: 0
                lon: 0
                zoom: 1
                id: map
				on_map_relocated: root.draw_marker()
            Image:
                source: 'paris.jpg'
                id: image
        BoxLayout:
    		size_hint_y: 0.1
    		Label:
    			size_hint_x: 25
    			text: "Lat"
    		Label:
    			size_hint_x: 25
    			id: coor_lat
    		Label:
    			size_hint_x: 25
    			text: "Long"
    		Label:
    			size_hint_x: 25
    			id: coor_long
    	BoxLayout:
    		size_hint_y: 0.1
    		Label:
    			size_hint_x: 25
    			text: "Score"
    		Label:
    			size_hint_x: 25
    			id: score
    		Button:
    			size_hint_x: 25
    			text: "Check"
    			on_press: root.check_points()
    		Button:
    			size_hint_x: 25
    			text: "Next"
                on_press: root.next_place()
        BoxLayout:
            size_hint_y: 0.1
            Button:
                height: "40dp"
                text: 'Back to menu'
                on_press: root.manager.current = 'menu'
            
<FlagsScreen>:
    flag_score: score_flags
    my_image: image
    country_name: country
    GridLayout:
        rows: 3
        cols: 1
        BoxLayout:
			size_hint_y: 1
            Image:
                source: 'france.png'
                id: image
        BoxLayout:
            size_hint_y: 0.1
            Label:
				size_hint_x: 15
				text: "Score"
			Label:
				size_hint_x: 15
				id: score_flags
			Label:
				size_hint_x: 15
				text: "Country"
			TextInput:
				size_hint_x: 25
				id: country
			Button:
				size_hint_x: 15
				text: "Check"
				on_press: root.check_flag()
			Button:
				size_hint_x: 15
				text: "Next"
				on_press: root.next_flag()
		BoxLayout:
			size_hint_y: 0.1
			Button:
				height: "40dp"
				text: 'Back to menu'
				on_press: root.manager.current = 'menu'
""")
score=0
score_flags=0
# Zadeklarowanie obu ekranów
class MenuScreen(Screen):
    pass
 
class ShowMeScreen(Screen): 
    list_of_points = [                  # utworzenie bazy 10 obiektów - zdjęć obiektów wraz z współrzędnymi
                ['paris.jpg', 48+(51/60)+(30.05/3600), 2+(17/60)+(40.38/3600)],
                ['oslo.jpg', 59+(54/60)+(25/3600), 10+(45/60)+(13/3600)],
                ['new_york.jpg', 40+(41/60)+(21.1/3600), -(74+(2/60)+(40.2/3600))],
                ['london.jpg', 51+(30/60)+(2.2/3600), 0+(7/60)+(28.6/3600)],
                ['sydney.jpg', -33.85706, 151.21490],
                ['barcelona.jpg', 41+(24/60)+(13/3600), 2+(10/60)+(27.05/3600)],
                ['rome.jpg', 41+(53/60)+(24/3600), 12+(29/60)+(32/3600)],
                ['paris2.jpg', 48+(51/60)+(11/3600), 2+(20/60)+(59/3600)],
                ['moscow.jpg', 55+(45/60)+(8.95/3600), 37+(37/60)+(22.93/3600)],
                ['london2.jpg', 51+(30/60)+(9/3600), 0+(7/60)+(10/3600)],                
                ]
    
    def draw_marker(self):          
        
        try:
            self.my_map.remove_marker(self.marker)
        except:
            pass
        
        self.latitude = self.my_map.lat             # przypisanie współrzędnych z mapy
        self.longitude = self.my_map.lon
        
        self.marker = MapMarker(lat=self.latitude, lon=self.longitude)      # dodanie markera do mapy  
        self.my_map.add_marker(self.marker)
        
        self.search_lat.text = "{:.5f}".format(self.latitude)       # wyswietlenie współrzędnych markera
        self.search_long.text = "{:.5f}".format(self.longitude)
    
    def next_place(self):           # przejscie do następnego obiektu, który jest wybierany losowo
        x=random.choice(self.list_of_points)
        self.my_image.source=x[0]           # wczytanie odpowiedniego zdjęcia
     
    def check_points(self):
        global score
        
        for i in range(0,9):
            if self.my_image.source == self.list_of_points[i][0]:
                self.latitude = self.my_map.lat     # przypisanie wspołrzędnych z mapy
                self.longitude = self.my_map.lon
                a=6378137                       # algorytm Vincentego - obliczenie odległosci od wskazanego punktu do punktu, w którym znajduje się obiekt
                e2=0.0066943800229
                fi1=self.latitude*pi/180
                lambda1=self.longitude*pi/180
                fi2=self.list_of_points[i][1]*pi/180
                lambda2=self.list_of_points[i][2]*pi/180
                b=a*sqrt(1-e2)
                f=1-(b/a)
                d_lambda=lambda2-lambda1
                U1=atan(((1-f)*tan(fi1)))
                U2=atan(((1-f)*tan(fi2)))
                L_new=d_lambda
                L_old=0
                j=0
                while abs(L_new-L_old) >= (0.000001/3600)*pi/180:
                    L_old=L_new
                    j=j+1
                    sin_sigma=sqrt((cos(U2)*sin(L_old))**2+(cos(U1)*sin(U2)-sin(U1)*cos(U2)*cos(L_old))**2)
                    cos_sigma=sin(U1)*sin(U2)+cos(U1)*cos(U2)*cos(L_old)
                    sigma=atan2(sin_sigma,cos_sigma)
                    sin_alfa=(cos(U1)*cos(U2)*sin(L_old))/sin_sigma
                    cos2_alfa=1-((sin_alfa)**2)        
                    cos_2sigma_m=cos_sigma-2*(sin(U1)*sin(U2)/cos2_alfa)
                    C=(f/16)*cos2_alfa*(4+f*(4-3*cos2_alfa))
                    L_new=d_lambda+(1-C)*f*sin_alfa*(sigma+C*sin_sigma*(cos_2sigma_m+C*cos_sigma*(-1+2*cos_2sigma_m**2)))
            
                u2=((a**2)-(b**2))*cos2_alfa/(b**2)
                A=1+(u2/16384)*(4096+u2*(-768+u2*(320-175*u2)))
                B=(u2/1024)*(256+u2*(-128+u2*(74-47*u2)))
                d_sigma=B*sin_sigma*(cos_2sigma_m+0.25*B*(cos_sigma*(-1+2*cos_2sigma_m**2)-(1/6)*B*cos_2sigma_m*(-3+4*sin_sigma**2)*(-3+4*cos_2sigma_m**2)))
                s12=b*A*(sigma-d_sigma)
                print (s12)
                
                if s12<100000:   # dodawanie punktów w przypadku gdy odległosć wynosi mniej niż 100 km
                    score=score+1
                else:
                    score=score
                
                self.my_score.text = "{}".format(score)     # wyswietlenie punktów

class FlagsScreen(Screen):
    list_of_flags= [                # stworzenie bazy 8 flag państw
                ['france.png', "Francja"],
                ['norway.png', "Norwegia"],
                ['USA.png', "USA"],
                ['UK.png', "Wielka Brytania"],
                ['australia.png', "Australia"],
                ['spain.png', "Hiszpania"],
                ['italy.png', "Włochy"],
                ['russia.png', "Rosja"],
                ]
    
    def check_flag(self):
        global score_flags
        
        for i in range(0,7):
            if self.my_image.source == self.list_of_flags[i][0]:
                if self.country_name.text == self.list_of_flags[i][1]:  # dodawanie punktów w przypadku dobrej odpowiedzi
                    score_flags=score_flags+1
                else:
                    score_flags=score_flags
                
        self.flag_score.text = "{}".format(score_flags)  # wyswietlenie punktów
        
    def next_flag(self):    # przejscie do następnej flagi, która jest wybierana losowo
        x=random.choice(self.list_of_flags)
        self.my_image.source=x[0]   # wczytanie odpowiedniego zdjęcia
    
# Stworzenie screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(ShowMeScreen(name='showme'))
sm.add_widget(FlagsScreen(name='flags'))

class Application(App):

    def build(self):
        return sm

if __name__ == '__main__':
    Application().run()
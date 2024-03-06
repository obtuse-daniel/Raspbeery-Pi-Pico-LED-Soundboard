import time
import urequests
import ujson
import network
import machine
import base64
import pico_i2c_lcd
import neopixel
import lcd_api

country_dict = {
                'Argentina' : '37i9dQZEVXbMMy2roB9myp',
                'Australia' : '37i9dQZEVXbJPcfkRz0wJ0',
                'Austria' : '37i9dQZEVXbKNHh6NIXu36',
                'Belarus' : '37i9dQZEVXbIYfjSLbWr4V',
                'Belgium' : '37i9dQZEVXbJNSeeHswcKB',
                'Bolivia' : '37i9dQZEVXbJqfMFK4d691',
                'Brazil' : '37i9dQZEVXbMXbN3EUUhlg',
                'Bulgaria' : '37i9dQZEVXbNfM2w2mq1B8',
                'Canada' : '37i9dQZEVXbKj23U1GF4IR',
                'Chile' : '37i9dQZEVXbL0GavIqMTeb',
                'Colombia' : '37i9dQZEVXbOa2lmxNORXQ',
                'Costa Rica' : '37i9dQZEVXbMZAjGMynsQX',
                'Czech Republic' : '37i9dQZEVXbIP3c3fqVrJY',
                'Denmark' : '37i9dQZEVXbL3J0k32lWnN',
                'Dominican Republic' : '37i9dQZEVXbKAbrMR8uuf7',
                'Ecuador' : '37i9dQZEVXbJlM6nvL1nD1',
                'Egypt' : '37i9dQZEVXbLn7RQmT5Xv2',
                'El Salvador' : '37i9dQZEVXbLxoIml4MYkT',
                'Estonia' : '37i9dQZEVXbLesry2Qw2xS',
                'Finland' : '37i9dQZEVXbMxcczTSoGwZ',
                'France' : '37i9dQZEVXbIPWwFssbupI',
                'Germany' : '37i9dQZEVXbJiZcmkrIHGU',
                'Greece' : '37i9dQZEVXbJqdarpmTJDL',
                'Guatemala' : '37i9dQZEVXbLy5tBFyQvd4',
                'Honduras' : '37i9dQZEVXbJp9wcIM9Eo5',
                'Hong Kong' : '37i9dQZEVXbLwpL8TjsxOG',
                'Hungary' : '37i9dQZEVXbNHwMxAkvmF8',
                'Iceland' : '37i9dQZEVXbKMzVsSGQ49S',
                'India' : '37i9dQZEVXbLZ52XmnySJg',
                'Indonesia' : '37i9dQZEVXbObFQZ3JLcXt',
                'Ireland' : '37i9dQZEVXbKM896FDX8L1',
                'Israel' : '37i9dQZEVXbJ6IpvItkve3',
                'Italy' : '37i9dQZEVXbIQnj7RRhdSX',
                'Japan' : '37i9dQZEVXbKXQ4mDTEBXq',
                'Kazakhstan' : '37i9dQZEVXbM472oKPNKzS',
                'Latvia' : '37i9dQZEVXbJWuzDrTxbKS',
                'Lithuania' : '37i9dQZEVXbMx56Rdq5lwc',
                'Luxembourg' : '37i9dQZEVXbKGcyg6TFGx6',
                'Malaysia' : '37i9dQZEVXbJlfUljuZExa',
                'Mexico' : '37i9dQZEVXbO3qyFxbkOE1',
                'Morocco' : '37i9dQZEVXbJU9eQpX8gPT',
                'Netherlands' : '37i9dQZEVXbKCF6dqVpDkS',
                'New Zealand' : '37i9dQZEVXbM8SIrkERIYl',
                'Nicaragua' : '37i9dQZEVXbISk8kxnzfCq',
                'Nigeria' : '37i9dQZEVXbKY7jLzlJ11V',
                'Norway' : '37i9dQZEVXbJvfa0Yxg7E7',
                'Pakistan' : '37i9dQZEVXbJkgIdfsJyTw',
                'Panama' : '37i9dQZEVXbKypXHVwk1f0',
                'Paraguay' : '37i9dQZEVXbNOUPGj7tW6T',
                'Peru' : '37i9dQZEVXbJfdy5b0KP7W',
                'Philippines' : '37i9dQZEVXbNBz9cRCSFkY',
                'Poland' : '37i9dQZEVXbN6itCcaL3Tt',
                'Portugal' : '37i9dQZEVXbKyJS56d1pgi',
                'Romania' : '37i9dQZEVXbNZbJ6TZelCq',
                'Saudi Arabia' : '37i9dQZEVXbLrQBcXqUtaC',
                'Singapore' : '37i9dQZEVXbK4gjvS1FjPY',
                'Slovakia' : '37i9dQZEVXbKIVTPX9a2Sb',
                'South Africa' : '37i9dQZEVXbMH2jvi6jvjk',
                'South Korea' : '37i9dQZEVXbNxXF4SkHj9F',
                'Spain' : '37i9dQZEVXbNFJfN1Vw8d9',
                'Taiwan' : '37i9dQZEVXbMnZEatlMSiu',
                'Thailand' : '37i9dQZEVXbMnz8KIWsvf9',
                'Turkey' : '37i9dQZEVXbIVYVBNw9D5K',
                'United Emirates' : '37i9dQZEVXbM4UZuIrvHvA',
                'USA' : '37i9dQZEVXbLRQDuF5jeBp',
                'UK' : '37i9dQZEVXbLnolsZ8PSNw',
                'Ukraine' : '37i9dQZEVXbKkidEfWYRuD',
                'Uruguay' : '37i9dQZEVXbMJJi3wgRbAy',
                'Venezuela' : '37i9dQZEVXbNLrliB10ZnX', 
                'Vietnam' : '37i9dQZEVXbLdGSmz6xilI', 
                }

def connect():
# Connect to WLAN
# Connect function from https://projects.raspberrypi.org/en/projects/get-started-pico-w/2
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid) # Remove password if using airuc-guest
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)

def get_access_code():
    '''a function that asks the spotify web api for an authorization code and then returns that code'''
    client_string = base64.b64encode(bytes(client_id, 'utf-8') + bytes(':', 'utf-8') + bytes(client_secret, 'utf-8'))[:-1]
    body = {'grant_type' : 'client_credentials'} # data_encoded and headers are parameters for the post statement
    data_encoded = '&'.join(n+"="+v for n,v in body.items())
    headers = {'Authorization' : ('Basic ' + bytes.decode(client_string)),
               'Content-Type' : 'application/x-www-form-urlencoded'}
    
    access_code = urequests.post('https://accounts.spotify.com/api/token', headers = headers, data = data_encoded) # requests the access code
    returned_access_token = ujson.loads(access_code.text)
    access_token_list = [i for i in returned_access_token.values()] # taking the dictionary and making into the list
    access_token = access_token_list[1] # just taking the access code from the list

    return access_token

def get_top3_songs(token, country_link):
    '''sends a request to the spotufy web api to get the top 3 songs from a country's top 50 daily songs playlist'''
    lcd.clear() # clearing the led's and screen for a clean slate
    strip.clear() 
    strip.show()
    headers = {'Authorization': f'Bearer {token}'} # the access code is used here as a parameter
    top3_songs = urequests.get(f'https://api.spotify.com/v1/playlists/{country_link}/tracks?limit=3', headers = headers) # requests the songs
    top3_songs_json = ujson.loads(top3_songs.text)['items'] # taking the nested list and slices it at the items 
    lcd.putstr(f'{countries}') # prints the country name
    time.sleep(1)
    for song in top3_songs_json: # for each song in the top 3
        lcd.clear() # clear the screen
        track = song.get('track') # get the track data
        name = track.get('name') # get the name and popularity statistic of the song
        popularity = int(track.get('popularity'))
        lcd.putstr(f'{name[:32]}') # print the song name, cutting it if it is longer than the display screen
        if song == top3_songs_json[0]:
            rgbw1 = (5, 25, 0)
            rgbw2= (10, 10, 50)
                    
            if popularity >= 95:
                strip.set_pixel_line_gradient(0, 8, rgbw1, rgbw2)
                print('951')
            elif popularity >= 90:
                strip.set_pixel_line_gradient(0, 5, rgbw1, rgbw2)
                print('901')
            elif popularity >= 85:
                strip.set_pixel_line_gradient(0, 3, rgbw1, rgbw2)
                print('851')
            elif popularity >= 75:
                strip.set_pixel_line_gradient(0, 2, rgbw1, rgbw2)
                print('751')
            elif popularity >= 60:
                strip.set_pixel_line_gradient(0, 1, rgbw1, rgbw2)
                print('601')
            else:
                print('Not popular')
                lcd.clear()
                lcd.putstr('Not popular')
                        
        if song == top3_songs_json[1]:
            rgbw1 = (30, 0, 45)
            rgbw2= (50, 45, 50)
                    
            if popularity >= 95:
                strip.set_pixel_line_gradient(15, 8, rgbw1, rgbw2)
                print('952')
            elif popularity >= 90:
                strip.set_pixel_line_gradient(15, 9, rgbw1, rgbw2)
                print('902')
            elif popularity >= 85:
                strip.set_pixel_line_gradient(15, 11, rgbw1, rgbw2)
                print('852')
            elif popularity >= 75:
                strip.set_pixel_line_gradient(15, 13, rgbw1, rgbw2)
                print('752')
            elif popularity >= 60:
                strip.set_pixel_line_gradient(15, 14, rgbw1, rgbw2)
                print('602')
            else:
                print('Not popular')
                lcd.clear()
                lcd.putstr('Not popular')
                        
        if song == top3_songs_json[2]:
            rgbw1 = (10, 10, 10)
            rgbw2= (0, 0, 5)
                    
            if popularity >= 95:
                strip.set_pixel_line_gradient(14, 22, rgbw1, rgbw2)
                print('953')
            elif popularity >= 90:
                strip.set_pixel_line_gradient(14, 20, rgbw1, rgbw2)
                print('903')
            elif popularity >= 85:
                strip.set_pixel_line_gradient(14, 18, rgbw1, rgbw2)
                print('853')
            elif popularity >= 75:
                strip.set_pixel_line_gradient(14, 17, rgbw1, rgbw2)
                print('753')
            elif popularity >= 60:
                strip.set_pixel_line_gradient(14, 15, rgbw1, rgbw2)
                print('603')
            else:
                print('Not popular')
                lcd.clear()
                lcd.putstr('Not popular')
                      
        strip.show()
        time.sleep(4)

ssid = 'airuc-guest' # This should be ‘airuc-guest’ on campus Wi-Fi

try:
    connect()
    
except KeyboardInterrupt:
    machine.reset()
    
print('Connected. End of code.')

client_id = '580ae12575b64c4f8b7ae5d576bb76ce' # data needed for the push request to get the access code
client_secret = 'fac510a615c04f6dbca036127957e920'

i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000) # setting up the raspberry pi for the lcd screen
lcd = pico_i2c_lcd.I2cLcd(i2c, 39, 2, 16)
lcd.backlight_on()
strip = neopixel.Neopixel(30, 1, 28, "RGBW") # setting up the led's
strip.brightness(100)
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

strip.clear() # clean slate of the display and led's
strip.show()
lcd.putstr('Top 3 Songs by  Country')
lcd.clear()

token = get_access_code() # call the get_access_code fuction to get the access code and assign it to token
for countries in country_dict: # for each country with daily songs playlist, send the playlist id and the access code to the get_top3_songs fucntion
    get_top3_songs(token, country_dict[countries])

time.sleep(2)
lcd.clear()
strip.clear()
lcd.putstr('Finished')
time.sleep(4)

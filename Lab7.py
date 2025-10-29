import RPi.GPIO as GPIO
import socket

# --- GPIO setup ---
GPIO.setmode(GPIO.BCM)
led_pins = [23, 24, 25]  # LED1, LED2, LED3 (change to your pins)
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)

# Create PWM objects (1kHz frequency)
pwm_leds = [GPIO.PWM(pin, 100) for pin in led_pins]
for pwm in pwm_leds:
    pwm.start(0)

# Brightness values
led_brightness = [0, 0, 0]  # starting brightness in percent
selected_led = 0             # default LED 1

# --- Webpage function ---
def web_page():
    html = """
    <html>
    <head>
      <title>LED Brightness Control</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="icon" href="data:,">
      <style>
        html {
          font-family: Helvetica;
          display: inline-block;
          margin: 0px auto;
          text-align: center;
        }
        .box {
          border: 1px solid #888;
          border-radius: 6px;
          padding: 10px;
          display: inline-block;
          background-color: #f9f9f9;
          text-align: left;
        }
        label {
          font-weight: bold;
        }
        input[type=range] {
          width: 100%;
        }
        button {
          margin-top: 8px;
          width: 100%;
          padding: 6px;
          border: 1px solid #ccc;
          border-radius: 4px;
          background-color: #eee;
          cursor: pointer;
        }
        button:hover {
          background-color: #ddd;
        }
      </style>
    </head>
    <body>
      <div class="box">
        <label for="brightness">Brightness level:</label><br>
        <input type="range" id="brightness" name="brightness" min="0" max="100" value="%s"><br><br>

        <label>Select LED:</label><br>
        <form action="/" method="GET">
          <input type="radio" id="led1" name="led" value="1" %s>
          <label for="led1">LED 1 (%s%%)</label><br>

          <input type="radio" id="led2" name="led" value="2" %s>
          <label for="led2">LED 2 (%s%%)</label><br>

          <input type="radio" id="led3" name="led" value="3" %s>
          <label for="led3">LED 3 (%s%%)</label><br><br>

          <button type="submit" name="change">Change Brightness</button>
        </form>
      </div>
    </body>
    </html>
    """ % (
        led_brightness[selected_led],
        "checked" if selected_led == 0 else "",
        led_brightness[0],
        "checked" if selected_led == 1 else "",
        led_brightness[1],
        "checked" if selected_led == 2 else "",
        led_brightness[2],
    )

    return html.encode('utf-8')


# --- Web server setup ---
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(3)

def serve_web_page():
    global selected_led

    while True:
        print('Waiting for connection...')
        conn, addr = s.accept()
        print('Connection from', addr)
        request = conn.recv(1024).decode('utf-8')
        print('\nGET request:\n--------------------')
        print(request)

        data = request[request.find('GET')+6 : request.find('HTTP')]
        if len(data) > 0:
            # --- Parse LED selection ---
            if "led=1" in data:
                selected_led = 0
            elif "led=2" in data:
                selected_led = 1
            elif "led=3" in data:
                selected_led = 2

            # --- Parse brightness value ---
            if "brightness=" in data:
                try:
                    value = int(data.split("brightness=")[1].split("&")[0])
                    led_brightness[selected_led] = value
                    pwm_leds[selected_led].ChangeDutyCycle(value)
                    print("LED %d brightness set to %d%%" % (selected_led + 1, value))
                except:
                    pass

        conn.send(b'HTTP/1.1 200 OK\n')
        conn.send(b'Content-Type: text/html\n')
        conn.send(b'Connection: close\r\n\r\n')
        try:
            conn.sendall(web_page())
        finally:
            conn.close()


try:
    serve_web_page()
except KeyboardInterrupt:
    GPIO.cleanup()

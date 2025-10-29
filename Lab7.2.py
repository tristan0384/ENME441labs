import RPi.GPIO as GPIO
import socket

# --- GPIO setup ---
GPIO.setmode(GPIO.BCM)
led_pins = [23, 24, 25]  # LED1, LED2, LED3 (change to your pins)
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)

# Create PWM objects (1kHz frequency)
pwm_leds = [GPIO.PWM(pin, 1000) for pin in led_pins]
for pwm in pwm_leds:
    pwm.start(0)

# Brightness values
led_brightness = [0, 0, 0]  # starting brightness in percent
selected_led = 0             # default LED 1


def web_page():
    html = f"""
    <html>
    <head>
      <title>LED Brightness Control</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>
        html {{
          font-family: Helvetica;
          text-align: center;
        }}
        .box {{
          border: 1px solid #888;
          border-radius: 6px;
          padding: 15px;
          display: inline-block;
          background-color: #f9f9f9;
          margin-top: 20px;
          text-align: left;
        }}
        label {{
          font-weight: bold;
          display: inline-block;
          width: 60px;
        }}
        input[type=range] {{
          width: 200px;
          vertical-align: middle;
        }}
        span {{
          display: inline-block;
          width: 40px;
          text-align: right;
        }}
      </style>
      <script>
        function updateBrightness(led, value) {{
          document.getElementById('val' + led).innerText = value + '%';
          var xhr = new XMLHttpRequest();
          xhr.open('GET', '/?led=' + led + '&brightness=' + value, true);
          xhr.send();
        }}
      </script>
    </head>
    <body>
      <div class="box">
        <h2>LED Brightness Control</h2>
        <div>
          <label>LED 1:</label>
          <input type="range" min="0" max="100" value="{led_brightness[0]}" oninput="updateBrightness(1, this.value)">
          <span id="val1">{led_brightness[0]}%</span>
        </div><br>
        <div>
          <label>LED 2:</label>
          <input type="range" min="0" max="100" value="{led_brightness[1]}" oninput="updateBrightness(2, this.value)">
          <span id="val2">{led_brightness[1]}%</span>
        </div><br>
        <div>
          <label>LED 3:</label>
          <input type="range" min="0" max="100" value="{led_brightness[2]}" oninput="updateBrightness(3, this.value)">
          <span id="val3">{led_brightness[2]}%</span>
        </div>
      </div>
    </body>
    </html>
    """
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
        request = conn.recv(1024).decode('utf-8')

        data = request[request.find('GET')+6 : request.find('HTTP')]
        if len(data) > 0:
            if "led=1" in data:
                selected_led = 0
            elif "led=2" in data:
                selected_led = 1
            elif "led=3" in data:
                selected_led = 2

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
    for pwm in pwm_leds:
        pwm.stop()
    GPIO.cleanup()


class Image():
    def __init__(self, **kwargs)->None:
        self.width = kwargs.get("width", 500)
        self.height = kwargs.get("height", 150)

        self.font = kwargs.get("font", ["./static/fonts/Josefin_Sans/JosefinSans-VariableFont_wght.ttf"])
        self.font_lengthMin = kwargs.get("font_lengthMin", 60)
        self.font_lengthMax = kwargs.get("font_lengthMax", 73)
        
        self.wrap_amplitude = kwargs.get("wrap_amplitude", 5)
        self.wrap_waveLength = kwargs.get("wrap_waveLength", 60)

        self.line_widthMin = kwargs.get("line_widthMin", 1)
        self.line_widthMax = kwargs.get("line_widthMax", 2)
        self.line_count = kwargs.get("line_count", 3)

        self.curve_count = kwargs.get("curve_count", 2)

        self.margin = 10

    ##
    def generate_text(self, txt:str)->object:
        from PIL import Image, ImageDraw, ImageFont
        import random

        ##
        # img = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))

        usable_width = self.width - self.margin * 2
        spacing = usable_width // len(txt)
        x = self.margin

        for i in txt:
            font_path = random.choice(self.font)
            font_size = random.randint(self.font_lengthMin, self.font_lengthMax)
            # print(font_path)
            font = ImageFont.truetype(font=font_path, size=font_size)

            #
            # char_x = 20 # random.randint(0, 40)
            # char_y = 25 # random.randint(0, 40)

            char_x = random.randint(0, 10)
            char_y = random.randint(0 ,25)

            char_img = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
            # char_img = Image.new('RGBA', (80, 80), (0, 0, 0, 0))
            char_draw = ImageDraw.Draw(char_img)
            char_draw.text((char_x, char_y), text=i, font=font, fill=(0, 0, 0))

            #
            # rotated = char_img
            rotated = char_img.rotate(random.randint(-20, 20), expand=True)

            img.paste(rotated, (x, random.randint(5, 25)), rotated)
            # img.paste(rotated, (x, 10), rotated)
            x += spacing

        # img.show()
        return img

    def generate_background(self)->object:
        from PIL import Image
        import numpy
        import random

        ##
        base = numpy.random.randint(200, 245, (self.height, self.width, 3), dtype=numpy.uint8)

        for _ in range(200):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            base[y, x] = numpy.random.randint(150, 200)

        return Image.fromarray(base)

    def add_line(self, img:object)->object:
        from PIL import ImageDraw
        import random

        ##
        draw = ImageDraw.Draw(img)

        for _ in range(self.line_count):
            x1, y1 = random.randint(0, self.width), random.randint(0, self.height)
            x2, y2 = random.randint(0, self.width), random.randint(0, self.height)
            draw.line((x1, y1, x2, y2), fill=(0, 0, 0), width=random.randint(self.line_widthMin, self.line_widthMax))

        for _ in range(self.curve_count):
            points = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(4)]
            for i in range(100):
                t = i / 99
                x = int((1-t)**3 * points[0][0] +
                        3*(1-t)**2 * t * points[1][0] +
                        3*(1-t) * t**2 * points[2][0] +
                        t**3 * points[3][0])
                y = int((1-t)**3 * points[0][1] +
                        3*(1-t)**2 * t * points[1][1] +
                        3*(1-t) * t**2 * points[2][1] +
                        t**3 * points[3][1])
                if 0 <= x < self.width and 0 <= y < self.height:
                    img.putpixel((x, y), (60, 60, 60))

        # img.show()

        return img

    def wrap(self, img:object)->object:
        from PIL import Image
        import random
        import math

        ##
        amplitude = self.wrap_amplitude
        wave_length = self.wrap_waveLength

        img_wrapped = Image.new("RGB", (self.width, self.height))
        for x in range(self.width):
            for y in range(self.height):
                offset = int(amplitude * math.sin(2 * math.pi * y / wave_length))
                next_x = (x + offset) % self.width
                img_wrapped.putpixel((next_x, y), img.getpixel((x, y)))

        return img_wrapped

    ##
    def generate(self, text:str)->object:
        import random

        ##
        img_text = self.generate_text(text)
        background = self.generate_background()

        background.paste(img_text, (0, 0), img_text)

        img_rotated = background.rotate(random.randint(-10, 10), expand=False, fillcolor="white")
        img_wrapped = self.wrap(img_rotated)
        img_lined = self.add_line(img_wrapped)

        return img_lined.convert("RGB")

## Flask application
def generate_img()->object:
    from begin.xtensions import flask
    from begin.globals import Cookie, Token

    from io import BytesIO

    ##
    captcha_instance = Image()
    captcha_token = Token.code_captcha()
    captcha_img = captcha_instance.generate(captcha_token)
    # captcha_img = captcha_instance.generate('gggggg999')

    print('token: ', captcha_token)

    img_io = BytesIO()
    captcha_img.save(img_io, 'PNG')
    img_io.seek(0)

    #
    captcha_token_hashed = Token.crypt_phash(captcha_token)

    response = flask.make_response(flask.send_file(img_io, mimetype="image/png", download_name="captcha.png"))
    Cookie.define(response=response, name="captcha_token", value=captcha_token_hashed, max_age=5*60)

    return response

def generate(type:str)->object:
    type = type.upper()

    if type == "IMG":
        return generate_img()

    return flask.jsonify({
        'message': Messages.Message(
            content=Messages.Captcha.Error.invalid_type,
            type=Messages.Captcha.Error.js_class
        ).json
    })


def valid(token_input:str)->object:
    from begin.xtensions import flask
    from begin.globals import Cookie, Messages, Token

    ##
    if Cookie.get("captcha_token") is None:
        return flask.jsonify({
            "valid_captcha": False,
            "message": Messages.Message(
                content=Messages.Captcha.Error.not_requested,
                type=Messages.Captcha.Error.js_class
            ).json
        })

    captcha_token = Cookie.get("captcha_token")
    valid = Token.crypt_phash_auth(captcha_token, token_input)
    msg = Messages.Message(
        content=Messages.Captcha.Error.invalid if not valid else Messages.Captcha.Success.ok,
        type=Messages.Captcha.Error.js_class if not valid else Messages.Captcha.Success.js_class
    ).json

    response = flask.make_response(flask.jsonify({
        "valid_captcha": valid,
        "message": msg
    }))
    
    if valid:
        Cookie.delete(response=response, name="captcha_token")

    return response


"""

import secrets
import string

code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(13))
print(code)

instance = Captcha()
# captcha = instance.generate(code)
captcha = instance.generate(code)

captcha.show()

"""

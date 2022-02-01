import pygame
import requests


class Button:
    def __init__(self, x: int, y: int, w: int, h: int, color: tuple, color_hover: tuple):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.color = color
        self.color_hover = color_hover

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))

    def hover(self, win):
        m_pos = pygame.mouse.get_pos()
        if self.x < m_pos[0] < self.x + self.w and self.y < m_pos[1] < self.y + self.h:
            pygame.draw.rect(win, self.color_hover, (self.x, self.y, self.w, self.h))

    def click(self):
        m_pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()

        if self.x < m_pos[0] < self.x + self.w and self.y < m_pos[1] < self.y + self.h:
            if pressed[0]:
                return True

    def render_text(self, size, text, x, y, color, win, font=None):
        txt = pygame.font.Font(font, size)
        win.blit(txt.render(u'' + text, True, color), (self.x + x, self.y + y))


pygame.init()
lon, lat = 37.620070, 55.753630  # input('ll: ')
delta = "0.08"  # input('zoom: ')
win = pygame.display.set_mode((500, 500))
zoom = 1
btn_map = Button(455, 5, 40, 40, (255, 255, 255), (255, 255, 255))
btn_sat = Button(455, 50, 40, 40, (255, 255, 255), (255, 255, 255))
btn_gibr = Button(455, 95, 40, 40, (255, 255, 255), (255, 255, 255))


def ll():
    return f'{round(lon, 7)},{round(lat, 7)}'


def get_img(props=None):
    if props is None:
        props = {}
    global img

    resp = requests.get(
        'https://static-maps.yandex.ru/1.x/',
        {
            'll': ll(),
            "l": "map",
            "spn": ",".join([delta, delta]),
            "size": '450,450',
            **props
        })
    with open('map.jpg', 'wb') as writer:
        writer.write(resp.content)

    img = pygame.image.load('map.jpg')


get_img()
img = pygame.image.load('map.jpg')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == 1073741899 and zoom < 4:
                zoom += 0.1
                get_img({
                    "size": '450,450',
                    'scale': zoom
                })
            elif event.key == 1073741902 and zoom > 1:
                zoom -= 0.1
                get_img({
                    "size": '450,450',
                    'scale': zoom
                })

            elif event.key == 1073741903:
                lon += 0.005
                get_img()
            elif event.key == 1073741904:
                lon -= 0.005
                get_img()
            elif event.key == 1073741906:
                lat += 0.005
                get_img()
            elif event.key == 1073741905:
                lat -= 0.005
                get_img()

    win.blit(img, (0, 0))

    btn_map.draw(win)
    btn_map.hover(win)
    btn_map.render_text(20, 'MAP', 5, 15, (0, 0, 0), win)
    if btn_map.click():
        get_img({
            'l': 'map'
        })

    btn_sat.draw(win)
    btn_sat.hover(win)
    btn_sat.render_text(20, 'SAT', 5, 15, (0, 0, 0), win)
    if btn_sat.click():
        get_img({
            'l': 'sat'
        })

    btn_gibr.draw(win)
    btn_gibr.hover(win)
    btn_gibr.render_text(20, 'SAT,SKL', 0, 15, (0, 0, 0), win)
    if btn_gibr.click():
        get_img({
            'l': 'sat,skl'
        })

    pygame.display.update()

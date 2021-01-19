from tkinter import Tk, Canvas, Frame, BOTH
from numpy import sin, cos, tan, array, pi


factor_x = 100
factor_y = 200
offset = 50


class Scramjet2D(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self,):
        self.master.title("Scramjet")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)
        # upper_body_x = [0, 15, 20, 30]
        # upper_body_y = [0, 1.8, 1.8, 0]
        # lower_body_x = [12, 22]
        # lower_body_y = [2.4, 2.4]

        # thetas
        thetas = array([7.5, 8.6, 10.3, 4.27]) * pi / 180
        beta = 15.6 * pi / 180
        mu = 27.04 * pi / 180

        # Upper body    
        U1 = 2
        U2 = 1.5
        U3 = 1.1
        U4 = 4
        U5 = 5

        x0 = 0
        y0 = 0
        x1 = x0 + U1
        y1 = y0 + tan(thetas[0]) * U1
        x2 = x1 + U2
        y2 = y1 + tan(thetas[1]) * U2
        x3 = x2 + U3
        y3 = y2 + tan(thetas[2]) * U3
        x4 = x3 + U4
        y4 = y3
        x5 = x4 + U5
        y5 = y0

        upper_body_x = [x0, x1, x2, x3, x4, x5]
        upper_body_y = [y0, y1, y2, y3, y4, y5]

        upper_body = []
        for x, y in zip(upper_body_x, upper_body_y):
            upper_body += [x * factor_x + offset, y * factor_y + offset] 
        upper_body += upper_body[0:2]

        # Lower body
        heigth_comb = 0.4
        x_lip = (y3 + heigth_comb) / tan(beta)
        y_lip = y3 + heigth_comb
        L1 = 0.5
        L2 = 5
        L3 = tan(thetas[3]) * L1 / tan(mu)
        print(L3)

        x0 = x_lip
        y0 = y_lip
        x1 = x0 + L1
        y1 = y0 + tan(thetas[3]) * L1
        x2 = x1 + L2 + L3
        y2 = y1
        x3 = x2 - L3
        y3 = y0

        lower_body_x = [x0, x1, x2, x3]
        lower_body_y = [y0, y1, y2, y3]

        lower_body = []
        for x, y in zip(lower_body_x, lower_body_y):
        	lower_body += [x * factor_x + offset, y * factor_y + offset] 
        lower_body += lower_body[0:2]

        oblique_shock1 = upper_body[0:2] + lower_body[0:2]
        oblique_shock2 = upper_body[2:4] + lower_body[0:2]
        oblique_shock3 = upper_body[4:6] + lower_body[0:2]
        oblique_shock4 = lower_body[0:2] + upper_body[6:8]
        oblique_shock = oblique_shock1 + oblique_shock2 + oblique_shock3 + oblique_shock4

        expansion_wave1 = upper_body[8:10] + lower_body[6:8]
        expansion_wave2 = upper_body[8:10] + [lower_body[6] + 40, lower_body[3]]
        expansion_wave = expansion_wave1 + expansion_wave2

        # canvas.create_line(upper_body, width=2)
        canvas.create_line(lower_body, width=2)
        # canvas.create_line(oblique_shock, width=2, dash=(4, 2), fill='#f11')
        # canvas.create_line(expansion_wave, width=2, dash=(4, 2), fill='#1f1')

        canvas.pack(fill=BOTH, expand=1)


def main():
    root = Tk()
    X43A = Scramjet2D()
    root.geometry("1200x300+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()

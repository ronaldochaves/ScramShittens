from tkinter import Tk, Canvas, Frame, BOTH


class Scramjet2D(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Scramjets")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)
        upper_body_x = [0, 15, 20, 30]
        upper_body_y = [0, 1.8, 1.8, 0]
        lower_body_x = [12, 22]
        lower_body_y = [2.4, 2.4]

        factor_x = 20
        factor_y = 60
        offset = 50

        upper_body = []
        for x, y in zip(upper_body_x, upper_body_y):
        	upper_body += [x * factor_x + offset, y * factor_y + offset] 
        upper_body += upper_body[0:2]

        lower_body = []
        for x, y in zip(lower_body_x, lower_body_y):
        	lower_body += [x * factor_x + offset, y * factor_y + offset] 
        lower_body += lower_body[0:2]

        oblique_shock1 = upper_body[0:2] + lower_body[0:2]
        oblique_shock2 = lower_body[0:2] + upper_body[2:4]
        oblique_shock = oblique_shock1 + oblique_shock2

        expansion_wave1 = upper_body[4:6] + lower_body[2:4]
        expansion_wave2 = upper_body[4:6] + [lower_body[2] + 40, lower_body[3]]
        expansion_wave = expansion_wave1 + expansion_wave2
        canvas.create_line(upper_body, width=2)
        canvas.create_line(lower_body, width=2)
        canvas.create_line(oblique_shock, width=2, dash=(4, 2), fill='#f11')
        canvas.create_line(expansion_wave, width=2, dash=(4, 2), fill='#1f1')

        canvas.pack(fill=BOTH, expand=1)


def main():
    root = Tk()
    X43A = Scramjet2D()
    root.geometry("800x400+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()

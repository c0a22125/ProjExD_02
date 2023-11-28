import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900


def main():
    pg.display.set_caption("逃げろ！こうかとん")#ウィンドウタイトルを「逃げろ！こうかとん」とする
    screen = pg.display.set_mode((WIDTH, HEIGHT))#幅1600✖高さ900のスクリーンSurfaceを生成する
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")#背景画像pg_bg.jpgのSurfaceを生成する
    kk_img = pg.image.load("ex02/fig/3.png")#こうかとん画像3.pngをロード
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)# 2倍に拡大したSurfaceを生成する
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        screen.blit(bg_img, [0, 0])#背景画像をスクリーンSurfaceに貼り付ける
        screen.blit(kk_img, [900, 400])#こうかとん画像をスクリーンSurfaceの横900，縦400に貼り付ける
        pg.display.update()#画面を更新する
        tmr += 1
        clock.tick(10)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
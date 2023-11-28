import sys
import random
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta = {  # 練習３：押下キーと移動量の辞書
    pg.K_UP: (0, -5),  # キー：移動量／値：（横方向移動量，縦方向移動量）
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し、真理値タプルを返す関数
    引数 rct：こうかとんor爆弾SurfaceのRect
    戻り値：横方向、縦方向判定結果（画面内：True/画面外：False）
    """
    yoko , tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向の判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向の判定
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")  # ウィンドウタイトルを「逃げろ！こうかとん」
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # 幅1600✖高さ900のスクリーンSurfaceを生成
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")  # 背景画像pg_bg.jpgのSurfaceを生成
    kk_img = pg.image.load("ex02/fig/3.png")  # こうかとん画像3.pngをロード
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)  # 2倍に拡大したSurfaceを生成
    kk_rct = kk_img.get_rect()  # 練習３：こうかとんSurfaceのRectを抽出する
    kk_rct.center = 900, 400  # 練習３：こうかとんの初期座標
    bb_img = pg.Surface((20, 20))  # 練習:1 透明のsurfaceを生成
    bb_img.set_colorkey((0, 0, 0))  # 背景を透明にする
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 半径10の赤い円を生成
    bb_rct = bb_img.get_rect()  # 練習2:爆弾surfaceのRectを抽出
    bb_rct.centerx = random.randint(0, WIDTH)  # 座標の設定
    bb_rct.centery = random.randint(0, HEIGHT)
    clock = pg.time.Clock()
    tmr = 0
    vx = 5
    vy = 5
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:  # キーが押されたら
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        screen.blit(bg_img, [0, 0])  # 背景画像をスクリーンSurfaceに貼り付ける
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)  # 練習３：こうかとんを移動させる
        screen.blit(kk_img, kk_rct)  # こうかとん画像をスクリーンSurfaceの横900，縦400に貼り付ける
        bb_rct.move_ip(vx, vy)  # 赤い円が移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横がはみ出たら
            vx *= -1
        if not tate:  # 縦がはみ出たら
            vy *= -1
        
        screen.blit(bb_img, bb_rct)  # 赤い円を表示
        pg.display.update()  # 画面を更新する
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
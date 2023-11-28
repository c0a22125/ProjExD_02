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
    gg_img = pg.image.load("ex02/fig/6.png")  # ゲームオーバー時のこうかとんのSurfaceを生成
    gg_img = pg.transform.rotozoom(gg_img, 0, 2.0)  # 2倍に拡大したSurfaceを生成
    gg_rct = gg_img.get_rect()  # ゲームオーバー時のこうかとんSurfaceのRectを抽出する
    gg_rct.center = 900, 400  # ゲームオーバー時のこうかとんの座標
    fonto = pg.font.Font(None, 200)  # ゲームオーバーの文字を生成
    txt = fonto.render("Game Over", True, (255, 0, 0))
    clock = pg.time.Clock()
    tmr = 0
    vx , vy = 5, 5

    # 各方向に対するこうかとんの画像を作成
    kk_imgs = {
        (0, -5): pg.transform.flip(pg.transform.rotozoom(kk_img, 90, 1.0), True,True ),  # 下向き
        (0, 5): pg.transform.rotozoom(kk_img, 45, 1.0),   # 上向き
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 1.0),  # 右向き
        (5, 0): pg.transform.flip(pg.transform.rotozoom(kk_img, 0, 1.0), True, False),  # 左向き
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 1.0),  # 右下斜め
        (5, -5): pg.transform.flip(pg.transform.rotozoom(kk_img, -45, 1.0), True, False), # 左下斜め
        (-5, 5): pg.transform.rotozoom(kk_img, 45, 1.0), # 右上斜め
        (5, 5): pg.transform.flip(pg.transform.rotozoom(kk_img, 45, 1.0), True, False), # 左上斜め
    }

    accs = [a for a in range(1, 11)]  # 加速度のリスト

    bb_imgs = []
    bb_rcts = []
    for r in range(1, 11):  # 爆弾の大きさを大きくする
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
        bb_rcts.append(bb_img.get_rect())

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):  # ゲームオーバーの処理
            gg_rct.center = kk_rct.center  # ゲームオーバー時のこうかとんの座標を更新
            txt_rect = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(bg_img, [0, 0])  # 背景を表示
            screen.blit(bb_img, bb_rct)  # 爆弾を表示
            screen.blit(txt, txt_rect)  # Game Overを画面中央に表示
            screen.blit(gg_img, gg_rct)  # ゲームオーバー時のこうかとんを表示
            pg.display.update()
            pg.time.delay(2000)
            return
            
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:  # キーが押されたら
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        screen.blit(bg_img, [0, 0])  # 背景画像をスクリーンSurfaceに貼り付ける
        kk_rct.move_ip(sum_mv[0], sum_mv[1])  # こうかとんを移動
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_imgs.get((sum_mv[0], sum_mv[1]), kk_img), kk_rct.topleft)  # 押したキーに応じて向きを変えて移動
        avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]  # 爆弾の速度を更新
        bb_rct.move_ip(avx, avy)  # 爆弾の速度の変更を適応
        yoko, tate = check_bound(bb_rct)
        if yoko == False:  # 横がはみ出たら
            vx *= -1
        if not tate:  # 縦がはみ出たら
            vy *= -1
        
        bb_img = bb_imgs[min(tmr//500, 9)]  # 爆弾のサイズを更新
        screen.blit(bb_img, bb_rct)  # 爆弾を表示
        pg.display.update()  # 画面を更新する
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
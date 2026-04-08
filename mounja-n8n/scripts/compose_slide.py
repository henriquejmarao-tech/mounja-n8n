"""Compõe 1 slide final: canvas cream + tipografia + asset transparente."""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from config import (
    SLIDE_SIZE, SAFE_MARGIN, ASSET_PADDING, TEXT_REGION_RATIO, COLORS,
    FONT_CANDIDATES_TITLE, FONT_CANDIDATES_BODY, FONT_CANDIDATES_HANDLE,
    FONT_SIZE_TITLE, FONT_SIZE_BODY, FONT_SIZE_HANDLE,
    BRAND_HANDLE, LOGO_PATH,
)


def _load_font(candidates, size):
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _text_region_box(region: str) -> tuple:
    """Retorna (x0, y0, x1, y1) da área de texto dentro das margens."""
    W, H = SLIDE_SIZE
    m = SAFE_MARGIN
    if region == "left":
        return (m, m + 120, int(W * TEXT_REGION_RATIO), H - m - 140)
    if region == "right":
        return (int(W * (1 - TEXT_REGION_RATIO)), m + 120, W - m, H - m - 140)
    if region == "top":
        return (m, m + 120, W - m, int(H * TEXT_REGION_RATIO))
    if region == "bottom":
        return (m, int(H * (1 - TEXT_REGION_RATIO)), W - m, H - m - 140)
    # center
    return (m, m + 120, W - m, H - m - 140)


def _asset_region_box(position: str) -> tuple:
    """Retorna (x0, y0, x1, y1) da área do asset."""
    W, H = SLIDE_SIZE
    m = SAFE_MARGIN + ASSET_PADDING
    half_w, half_h = W // 2, H // 2
    regions = {
        "right":        (half_w, m, W - m, H - m - 140),
        "left":         (m, m, half_w, H - m - 140),
        "top":          (m, m, W - m, half_h),
        "bottom":       (m, half_h, W - m, H - m - 140),
        "top-right":    (half_w, m, W - m, half_h),
        "top-left":     (m, m, half_w, half_h),
        "bottom-right": (half_w, half_h, W - m, H - m - 140),
        "bottom-left":  (m, half_h, half_w, H - m - 140),
    }
    return regions.get(position, regions["bottom-right"])


def _wrap_text(text: str, font: ImageFont.ImageFont, max_width: int, draw: ImageDraw.ImageDraw) -> list:
    """Quebra texto em linhas que cabem em max_width."""
    words = text.replace("\\n", "\n").split()
    lines = []
    current = ""
    for word in words:
        if "\n" in word:
            parts = word.split("\n")
            for i, part in enumerate(parts):
                test = f"{current} {part}".strip() if i == 0 else part
                if draw.textlength(test, font=font) <= max_width:
                    current = test
                else:
                    if current:
                        lines.append(current)
                    current = part
                if i < len(parts) - 1:
                    lines.append(current)
                    current = ""
        else:
            test = f"{current} {word}".strip()
            if draw.textlength(test, font=font) <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
    if current:
        lines.append(current)
    return lines


def _gradient_mask_text(text: str, font: ImageFont.ImageFont, size: tuple) -> Image.Image:
    """Cria uma imagem RGBA com o texto preenchido com gradiente rosa→roxo."""
    w, h = size
    # Gradiente horizontal rosa → roxo
    grad = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for x in range(w):
        t = x / max(w - 1, 1)
        r = int(COLORS["brand_pink"][0] * (1 - t) + COLORS["brand_purple"][0] * t)
        g = int(COLORS["brand_pink"][1] * (1 - t) + COLORS["brand_purple"][1] * t)
        b = int(COLORS["brand_pink"][2] * (1 - t) + COLORS["brand_purple"][2] * t)
        for y in range(h):
            grad.putpixel((x, y), (r, g, b, 255))
    # Máscara do texto
    mask = Image.new("L", (w, h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.text((0, 0), text, font=font, fill=255)
    # Aplica máscara ao gradiente
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(grad, (0, 0), mask)
    return out


def _draw_text_block(canvas: Image.Image, slide: dict, region: tuple):
    """Desenha título + corpo dentro de region, com destaque em gradiente."""
    draw = ImageDraw.Draw(canvas)
    x0, y0, x1, y1 = region
    max_w = x1 - x0

    title_font = _load_font(FONT_CANDIDATES_TITLE, FONT_SIZE_TITLE)
    body_font = _load_font(FONT_CANDIDATES_BODY, FONT_SIZE_BODY)

    y = y0
    # ---- TÍTULO ----
    title = slide.get("titulo", "")
    destaque = slide.get("destaque", "") or ""
    title_lines = _wrap_text(title, title_font, max_w, draw)
    for line in title_lines:
        if destaque and destaque.lower() in line.lower():
            # Divide a linha em 3: antes, destaque, depois
            idx = line.lower().find(destaque.lower())
            before = line[:idx]
            match = line[idx:idx + len(destaque)]
            after = line[idx + len(destaque):]
            cx = x0
            if before:
                draw.text((cx, y), before, font=title_font, fill=COLORS["text_dark"])
                cx += int(draw.textlength(before, font=title_font))
            # gradiente no trecho do destaque
            mw = int(draw.textlength(match, font=title_font)) + 4
            mh = FONT_SIZE_TITLE + 20
            grad_img = _gradient_mask_text(match, title_font, (mw, mh))
            canvas.paste(grad_img, (cx, y), grad_img)
            cx += mw
            if after:
                draw.text((cx, y), after, font=title_font, fill=COLORS["text_dark"])
        else:
            draw.text((x0, y), line, font=title_font, fill=COLORS["text_dark"])
        y += int(FONT_SIZE_TITLE * 1.15)

    y += 20
    # linha divisória dourada/roxa
    draw.line([(x0, y), (x0 + 80, y)], fill=COLORS["brand_purple"], width=3)
    y += 30

    # ---- CORPO ----
    body = slide.get("corpo", "")
    for paragraph in body.split("\n"):
        if not paragraph.strip():
            y += int(FONT_SIZE_BODY * 0.5)
            continue
        body_lines = _wrap_text(paragraph, body_font, max_w, draw)
        for line in body_lines:
            if y > y1:
                return
            if destaque and destaque.lower() in line.lower() and destaque.lower() not in title.lower():
                # destaque também pode aparecer no corpo
                idx = line.lower().find(destaque.lower())
                before = line[:idx]
                match = line[idx:idx + len(destaque)]
                after = line[idx + len(destaque):]
                cx = x0
                if before:
                    draw.text((cx, y), before, font=body_font, fill=COLORS["text_dark"])
                    cx += int(draw.textlength(before, font=body_font))
                mw = int(draw.textlength(match, font=body_font)) + 4
                mh = FONT_SIZE_BODY + 14
                grad_img = _gradient_mask_text(match, body_font, (mw, mh))
                canvas.paste(grad_img, (cx, y), grad_img)
                cx += mw
                if after:
                    draw.text((cx, y), after, font=body_font, fill=COLORS["text_dark"])
            else:
                draw.text((x0, y), line, font=body_font, fill=COLORS["text_dark"])
            y += int(FONT_SIZE_BODY * 1.35)


def _paste_asset(canvas: Image.Image, asset_path: Path, region: tuple):
    """Encaixa o asset transparente dentro de region com drop shadow."""
    if not asset_path.exists():
        return
    asset = Image.open(asset_path).convert("RGBA")
    x0, y0, x1, y1 = region
    rw, rh = x1 - x0, y1 - y0
    aw, ah = asset.size
    # Escala preservando aspecto
    scale = min(rw / aw, rh / ah)
    new_size = (max(1, int(aw * scale)), max(1, int(ah * scale)))
    asset = asset.resize(new_size, Image.LANCZOS)
    # Centraliza na região
    px = x0 + (rw - new_size[0]) // 2
    py = y0 + (rh - new_size[1]) // 2
    # Drop shadow
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shadow_mask = asset.getchannel("A")
    shadow_layer = Image.new("RGBA", new_size, (123, 44, 191, 100))
    shadow_layer.putalpha(shadow_mask)
    shadow.paste(shadow_layer, (px + 8, py + 16), shadow_layer)
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    canvas.alpha_composite(shadow)
    # Asset real
    canvas.alpha_composite(asset, dest=(px, py))


def _draw_footer(canvas: Image.Image, slide_n: int, total: int):
    draw = ImageDraw.Draw(canvas)
    W, H = SLIDE_SIZE
    handle_font = _load_font(FONT_CANDIDATES_HANDLE, FONT_SIZE_HANDLE)
    # Handle à esquerda
    draw.text((SAFE_MARGIN, H - SAFE_MARGIN - 30), BRAND_HANDLE,
              font=handle_font, fill=COLORS["text_muted"])
    # Paginação à direita
    pag = f"{slide_n:02d} / {total:02d}"
    tw = draw.textlength(pag, font=handle_font)
    draw.text((W - SAFE_MARGIN - tw, H - SAFE_MARGIN - 30), pag,
              font=handle_font, fill=COLORS["text_muted"])
    # Logo no rodapé central (se existir)
    if LOGO_PATH.exists():
        logo = Image.open(LOGO_PATH).convert("RGBA")
        lh = 50
        lw = int(logo.width * (lh / logo.height))
        logo = logo.resize((lw, lh), Image.LANCZOS)
        canvas.alpha_composite(logo, dest=((W - lw) // 2, H - SAFE_MARGIN - 55))
    # Linha sutil divisória no topo
    draw.line([(SAFE_MARGIN, SAFE_MARGIN + 40), (W - SAFE_MARGIN, SAFE_MARGIN + 40)],
              fill=COLORS["divider"][:3], width=2)


def compose_slide(slide: dict, asset_path: Path, out_path: Path, total_slides: int):
    W, H = SLIDE_SIZE
    canvas = Image.new("RGBA", (W, H), COLORS["bg_cream"] + (255,))

    text_region = _text_region_box(slide.get("text_region", "left"))

    # Asset primeiro (fica atrás do texto se houver sobreposição parcial — mas em princípio não tem)
    if slide.get("asset_position") and asset_path and asset_path.exists():
        asset_region = _asset_region_box(slide["asset_position"])
        _paste_asset(canvas, asset_path, asset_region)

    _draw_text_block(canvas, slide, text_region)
    _draw_footer(canvas, slide["n"], total_slides)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(out_path, "PNG", quality=95)


def main():
    import json
    ap = argparse.ArgumentParser()
    ap.add_argument("--slide-json", required=True, help="JSON de um único slide")
    ap.add_argument("--asset", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--total", type=int, required=True)
    args = ap.parse_args()
    slide = json.loads(Path(args.slide_json).read_text(encoding="utf-8"))
    compose_slide(slide, Path(args.asset), Path(args.out), args.total)
    print(f"[compose] {args.out}")


if __name__ == "__main__":
    main()

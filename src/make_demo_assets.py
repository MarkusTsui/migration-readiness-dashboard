"""Create repository-ready dashboard images and a short visual demo."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "outputs" / "powerbi_data"
SCREENSHOTS = ROOT / "dashboard" / "screenshots"
DEMO = ROOT / "demo"


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in ("C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _save_summary_card(path: Path, title: str, subtitle: str, lines: list[str], colour: str) -> None:
    image = Image.new("RGB", (1600, 900), "#f7f9fc")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1600, 130), fill=colour)
    draw.text((70, 38), title, fill="white", font=_font(48))
    draw.text((70, 170), subtitle, fill="#27364b", font=_font(32))
    y = 290
    for line in lines:
        draw.text((100, y), line, fill="#27364b", font=_font(42))
        y += 90
    image.save(path)


def _desktop_frame(page: Image.Image, cursor: tuple[int, int], click: bool = False) -> Image.Image:
    """Place a dashboard page in a browser-like desktop and draw a moving cursor."""
    canvas = Image.new("RGB", (1280, 720), "#1f2937")
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 1280, 34), fill="#111827")
    draw.ellipse((16, 11, 28, 23), fill="#ef4444")
    draw.ellipse((36, 11, 48, 23), fill="#f59e0b")
    draw.ellipse((56, 11, 68, 23), fill="#22c55e")
    draw.rectangle((0, 34, 1280, 78), fill="#e5e7eb")
    draw.text((92, 47), "Migration readiness dashboard  |  localhost:8501", fill="#374151", font=_font(20))
    fitted = page.copy()
    fitted.thumbnail((1160, 600), Image.Resampling.LANCZOS)
    left = (1280 - fitted.width) // 2
    top = 92 + (600 - fitted.height) // 2
    canvas.paste(fitted, (left, top))
    x, y = cursor
    draw.line((x, y, x + 18, y + 30), fill="white", width=5)
    draw.line((x, y, x + 18, y + 30), fill="#111827", width=2)
    draw.polygon([(x, y), (x + 2, y + 25), (x + 12, y + 19), (x + 20, y + 29)], fill="white", outline="#111827")
    if click:
        draw.ellipse((x - 16, y - 16, x + 16, y + 16), outline="#38bdf8", width=5)
    return canvas


def _make_desktop_demo(pages: list[Image.Image]) -> list[Image.Image]:
    """Create a short simulated desktop recording with cursor movement and clicks."""
    frames: list[Image.Image] = []
    starts = [(190, 150), (1020, 170), (240, 580)]
    ends = [(1020, 170), (250, 580), (1040, 560)]
    for page, start, end in zip(pages, starts, ends):
        for step in range(45):
            fraction = step / 44
            cursor = (
                round(start[0] + (end[0] - start[0]) * fraction),
                round(start[1] + (end[1] - start[1]) * fraction),
            )
            frames.append(_desktop_frame(page, cursor, click=step in (38, 44)))
        frames.extend([_desktop_frame(page, end)] * 15)
    return frames


def main() -> None:
    score = pd.read_csv(DATA / "scorecard_before_after.csv")
    control = pd.read_csv(DATA / "before_08_control_totals.csv")
    variance = pd.read_csv(DATA / "before_05_balance_variance.csv")
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    DEMO.mkdir(parents=True, exist_ok=True)

    before = score[score.stage.eq("before")]
    after = score[score.stage.eq("after")]
    _save_summary_card(
        SCREENSHOTS / "01_readiness_summary.png",
        "Migration readiness: remediation changes the decision",
        "Synthetic loan migration | 50,000 legacy records",
        [
            f"Before: {before['verdict'].iloc[0]}  |  {int((before.status == 'PASS').sum())}/{len(before)} checks pass",
            f"After:  {after['verdict'].iloc[0]}  |  {int((after.status == 'PASS').sum())}/{len(after)} checks pass",
            f"Balance variance before remediation: ${before.dollar_impact.sum():,.2f}",
        ],
        "#315a8a",
    )

    fig, ax = plt.subplots(figsize=(16, 9))
    control.plot(x="product", y=["legacy_total", "new_total"], kind="bar", ax=ax, color=["#315a8a", "#70ad47"])
    ax.set_title("Financial tie-out: product control totals", fontsize=22, pad=18)
    ax.set_xlabel("")
    ax.set_ylabel("Outstanding balance")
    ax.legend(["Legacy", "New system"])
    fig.tight_layout()
    fig.savefig(SCREENSHOTS / "02_financial_tieout.png", dpi=120)
    plt.close(fig)

    top = variance.assign(abs_variance=variance["variance"].abs()).sort_values("abs_variance", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.barh(top["loan_id"].astype(str)[::-1], top["abs_variance"][::-1], color="#d95f02")
    ax.set_title("Defect drill-down: largest balance variances", fontsize=22, pad=18)
    ax.set_xlabel("Absolute balance variance")
    ax.set_ylabel("Loan ID")
    fig.tight_layout()
    fig.savefig(SCREENSHOTS / "03_defect_drilldown.png", dpi=120)
    plt.close(fig)

    pages = [Image.open(path).convert("RGB") for path in (
        SCREENSHOTS / "01_readiness_summary.png",
        SCREENSHOTS / "02_financial_tieout.png",
        SCREENSHOTS / "03_defect_drilldown.png",
    )]
    frames = _make_desktop_demo(pages)
    frames[0].save(DEMO / "demo.gif", save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=True)

    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        with tempfile.TemporaryDirectory(prefix="migration-demo-") as temp_dir:
            frame_dir = Path(temp_dir)
            for index, frame in enumerate(frames):
                frame.save(frame_dir / f"frame_{index:04d}.png")
            subprocess.run(
                [ffmpeg, "-y", "-framerate", "12.5", "-i", str(frame_dir / "frame_%04d.png"),
                 "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                 str(DEMO / "demo.mp4")],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )


if __name__ == "__main__":
    main()

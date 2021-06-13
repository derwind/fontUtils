import os, sys, re
import glob
import argparse
from fontTools.ttLib import TTFont

def get_psname(ttFont):
    return ttFont["name"].getName(nameID=6, platformID=3, platEncID=1)

class IsKanji:
    def __init__(self):
        self.kanji_ranges = set(range(0x2E80, 0x2FDF+1)) | {0x3005, 0x3007, 0x303B} | set(range(0x4E00, 0x9FFF+1)) | set(range(0xF900, 0xFAFF+1)) | set(range(0x20000, 0x2FFFF+1))

    def __call__(self, uni):
        return uni in self.kanji_ranges

iskanji = IsKanji()

def enumerate_many_kanji_fonts(ref_font, font_dir, collect_dir=None):
    ref_psname = get_psname(ref_font)
    ref_cmap = ref_font.getBestCmap()
    ref_kanjis = {uni for uni in ref_cmap if iskanji(uni)}

    print(f"ref kanjis: {len(ref_kanjis)}")
    print("-"*20)

    if collect_dir is not None:
        import shutil
        os.makedirs(collect_dir, exist_ok=True)

    for file in glob.glob(os.path.join(font_dir, "*.*tf")):
        ttFont =TTFont(file)
        psname = get_psname(ttFont)
        if psname == ref_psname:
            continue
        cmap = ttFont.getBestCmap()
        shared_kanjis = ref_kanjis & set(cmap)
        ratio = len(shared_kanjis) / len(ref_kanjis)

        if ratio < 0.9:
            continue

        print(psname, len(shared_kanjis), f"({round(ratio * 100, 2)}%)")
        if collect_dir is not None:
            basename = os.path.basename(file)
            shutil.copy2(file, os.path.join(collect_dir, basename))

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", metavar="REF_FONT", dest="ref_font", type=str, required=True,
                        help="reference font")
    parser.add_argument("--collect", metavar="collect_dir", dest="collect_dir", type=str, default=None,
                        help="directory path in which target fonts will be collected")
    parser.add_argument("font_dir", metavar="FONT_DIR", type=str,
                        help="fonts directory")

    args = parser.parse_args()

    return args

def main():
    args = get_args()

    ref_font = TTFont(args.ref_font)

    enumerate_many_kanji_fonts(ref_font, args.font_dir, args.collect_dir)

if __name__ == "__main__":
    main()

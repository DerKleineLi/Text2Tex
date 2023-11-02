from argparse import ArgumentParser
from pathlib import Path

import cv2

# scene_name = "LivingRoom-36282"
# short_prompt = "classic"  # used for output_dir


def parse_args():
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "--scene_name", type=str, default="0b16abb1-4a59-4ce3-85b5-8ec10440d9dd"
    )
    arg_parser.add_argument("--short_prompt", type=str, default="classic")
    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    scene_name = args.scene_name
    short_prompt = args.short_prompt

    input_dir = Path("data") / scene_name
    output_dir = Path("outputs") / "text2tex" / scene_name / short_prompt

    # input_stuff_dir = input_dir / "stuff"

    # # all png files in input_stuff_dir
    # png_files = list(input_stuff_dir.glob("*.png"))
    # # read all png files
    # pngs = [cv2.imread(str(png_file)) for png_file in png_files]
    # combined_mask = np.zeros_like(pngs[0], dtype=bool)
    # for png in pngs:
    #     combined_mask |= png[0] > 128

    output_stuff_file = (
        output_dir / "stuff" / "42-p36-h0-1.0-0.3-0.1" / "generate" / "mesh" / "15.png"
    )
    result = cv2.imread(str(output_stuff_file))

    input_things_dir = input_dir / "things"
    output_things_dir = output_dir / "things"
    things_dirs = list(output_things_dir.glob("*"))
    for thing_dir in things_dirs:
        mask_file = thing_dir / "42-p36-h0-1.0-0.3-0.1/generate/mesh/9_texture_mask.png"
        texture_file = thing_dir / "42-p36-h0-1.0-0.3-0.1/generate/mesh/9.png"
        mask_png = cv2.imread(str(mask_file))
        mask = mask_png[:, :, 0] > 128
        texture_png = cv2.imread(str(texture_file))
        result[mask] = texture_png[mask]
    texture_file = (
        Path("outputs") / "text2tex" / f"text2tex_{scene_name}_{short_prompt}.png"
    )
    cv2.imwrite(str(texture_file), result)
    print("texture written to ", texture_file)

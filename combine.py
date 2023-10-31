from pathlib import Path

import cv2

scene_name = "LivingRoom-36282"
short_prompt = "classic"  # used for output_dir

if __name__ == "__main__":
    input_dir = Path("data") / scene_name
    output_dir = Path("outputs") / scene_name / short_prompt

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
    png_files = list(input_things_dir.glob("*.png"))
    for png_file in png_files:
        mask_png = cv2.imread(str(png_file))
        mask = mask_png[:, :, 0] > 128
        thing_name = png_file.stem
        output_png_file = (
            output_dir
            / "things"
            / thing_name
            / "42-p36-h0-1.0-0.3-0.1"
            / "generate"
            / "mesh"
            / "9.png"
        )
        output_png = cv2.imread(str(output_png_file))
        result[mask] = output_png[mask]

    cv2.imwrite(str(output_dir / "texture.png"), result)

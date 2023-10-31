from pathlib import Path

scene_name = "LivingRoom-36282"
short_prompt = "classic"  # used for output_dir
prompt_stuff = "a classic style living room"
prompt_thing = "a {thing_type} in a classic style living room"
camera_xyz = [0.85963, 1.1377, -4.6706]
radius = 2.5

stuff_pattern_file = "jobs/pattern/stuff.job"
thing_pattern_file = "jobs/pattern/thing.job"

with open(stuff_pattern_file, "r") as f:
    stuff_pattern = f.read()
with open(thing_pattern_file, "r") as f:
    thing_pattern = f.read()

if __name__ == "__main__":
    job_dir = Path("jobs") / scene_name / short_prompt
    input_dir = Path("data") / scene_name
    output_dir = Path("outputs") / scene_name / short_prompt

    job_dir.mkdir(parents=True, exist_ok=True)

    stuff_job = stuff_pattern.format(
        scene_name=scene_name,
        output_dir=output_dir / "stuff",
        prompt=prompt_stuff,
        radius=radius,
        camera_center_x=camera_xyz[0],
        camera_center_y=camera_xyz[1],
        camera_center_z=camera_xyz[2],
    )

    with open(job_dir / "stuff.job", "w") as f:
        f.write(stuff_job)

    input_things_dir = input_dir / "things"
    png_files = list(input_things_dir.glob("*.png"))
    for png_file in png_files:
        thing_name = png_file.stem
        thing_type = thing_name.split("_")[1]
        thing_job = thing_pattern.format(
            scene_name=scene_name,
            thing_name=thing_name,
            output_dir=output_dir / "things" / thing_name,
            prompt=prompt_thing.format(thing_type=thing_type),
        )
        with open(job_dir / f"{thing_name}.job", "w") as f:
            f.write(thing_job)

    with open(job_dir / "submit.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f"for i in *.job; do\n    sbatch -p submit $i;\ndone")

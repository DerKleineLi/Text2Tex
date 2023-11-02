from pathlib import Path

scene_name = "0b16abb1-4a59-4ce3-85b5-8ec10440d9dd"
short_prompt = "classic"  # used for output_dir
prompt_stuff = "a classic style living room"
prompt_thing = "a {thing_type} in a classic style living room"
camera_xyz = [0.85963, 1.1377, -4.6706]
radius = 2.5

if __name__ == "__main__":
    stuff_pattern_file = "jobs/pattern/stuff.job"
    thing_pattern_file = "jobs/pattern/thing.job"
    combine_pattern_file = "jobs/pattern/combine.job"
    with open(stuff_pattern_file, "r") as f:
        stuff_pattern = f.read()
    with open(thing_pattern_file, "r") as f:
        thing_pattern = f.read()
    with open(combine_pattern_file, "r") as f:
        combine_pattern = f.read()

    job_dir = Path("jobs")
    scene_dir = Path("data/3D-FRONT_preprocessed/scenes") / scene_name
    room_dir = next(scene_dir.iterdir())
    input_dir = room_dir / "meshes"
    output_dir = Path("outputs") / "text2tex" / scene_name / short_prompt

    job = stuff_pattern.format(
        input_dir=input_dir / "stuff",
        output_dir=output_dir / "stuff",
        prompt=prompt_stuff,
        radius=radius,
        camera_center_x=camera_xyz[0],
        camera_center_y=camera_xyz[1],
        camera_center_z=camera_xyz[2],
    )

    input_things_dir = input_dir / "things"
    obj_files = list(input_things_dir.glob("*.obj"))
    for obj_file in obj_files:
        thing_name = obj_file.stem
        thing_type = thing_name.split("_")[1]
        thing_job = thing_pattern.format(
            input_dir=input_things_dir,
            scene_name=scene_name,
            thing_name=thing_name,
            output_dir=output_dir / "things" / thing_name,
            prompt=prompt_thing.format(thing_type=thing_type),
        )
        job += thing_job

    job += combine_pattern.format(scene_name=scene_name, short_prompt=short_prompt)

    with open(job_dir / f"{scene_name}_{short_prompt}.job", "w") as f:
        f.write(job)

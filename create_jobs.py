from pathlib import Path

import yaml

scene_prompt_short_list = [  # scene_name, short_prompt, prompt_stuff
    # # realistic
    # [
    #     "0b7e278e-d5df-416d-8c71-684ca8cbd364",
    #     "baroque",
    #     "a baroque style cozy bedroom",
    # ],
    # [
    #     "0b16abb1-4a59-4ce3-85b5-8ec10440d9dd",
    #     "classic",
    #     "a classic style living room",
    # ],
    # [
    #     "0da4d8b3-d0fc-44c6-83bc-016a8e7a1503",
    #     "modern",
    #     "a modern living room",
    # ],
    # [
    #     "0f737b17-9449-4961-b978-e115bcba56de",
    #     "minimalist",
    #     "a minimalist style living room",
    # ],
    # [
    #     "01ba1742-4fa5-4d1e-8ba4-2f807fe6b283",
    #     "midcentury",
    #     "a midcentury style living room",
    # ],
    # [
    #     "93f59740-4b65-4e8b-8a0f-6420b339469d",
    #     "scandinavian",
    #     "a scandinavian style living room",
    # ],
    # [
    #     "305d3251-8f1e-4cca-9227-011187146d89",
    #     "cozy",
    #     "a cozy big traditional style bedroom",
    # ],
    # [
    #     "01805656-e66f-44b1-8bc1-5e722fff3fff",
    #     "contemporary",
    #     "a contemporary style bedroom",
    # ],
    # [
    #     "a37f9f03-7361-4fe4-8aa7-718f41855ea5",
    #     "transitional",
    #     "a transitional style bedroom",
    # ],
    # realistic2
    [
        "0b7e278e-d5df-416d-8c71-684ca8cbd364",
        "modern",
        "a modern style bedroom",
    ],
    [
        "0b16abb1-4a59-4ce3-85b5-8ec10440d9dd",
        "transitional",
        "a transitional style living room",
    ],
    [
        "0da4d8b3-d0fc-44c6-83bc-016a8e7a1503",
        "contemporary",
        "a contemporary living room",
    ],
    [
        "0f737b17-9449-4961-b978-e115bcba56de",
        "tranditional",
        "a tranditional style living room",
    ],
    [
        "01ba1742-4fa5-4d1e-8ba4-2f807fe6b283",
        "luxury",
        "a luxury style living room",
    ],
    [
        "93f59740-4b65-4e8b-8a0f-6420b339469d",
        "country",
        "a country style living room",
    ],
    [
        "305d3251-8f1e-4cca-9227-011187146d89",
        "french",
        "a french country style bedroom",
    ],
    [
        "01805656-e66f-44b1-8bc1-5e722fff3fff",
        "scandinavian",
        "a scandinavian style bedroom",
    ],
    [
        "a37f9f03-7361-4fe4-8aa7-718f41855ea5",
        "midcentury",
        "a midcentury style bedroom",
    ],
    # # creative
    # [
    #     "0b7e278e-d5df-416d-8c71-684ca8cbd364",
    #     "oil_painting",
    #     "an oil painting style bedroom",
    # ],
    # [
    #     "0b16abb1-4a59-4ce3-85b5-8ec10440d9dd",
    #     "star_wars",
    #     "a star wars style living room",
    # ],
    # [
    #     "0da4d8b3-d0fc-44c6-83bc-016a8e7a1503",
    #     "cartoon",
    #     "a cartoon style colorful living room",
    # ],
    # [
    #     "0f737b17-9449-4961-b978-e115bcba56de",
    #     "lego",
    #     "a lego style living room",
    # ],
    # [
    #     "01ba1742-4fa5-4d1e-8ba4-2f807fe6b283",
    #     "metallic",
    #     "a metallic style living room",
    # ],
    # [
    #     "93f59740-4b65-4e8b-8a0f-6420b339469d",
    #     "tropical",
    #     "a tropical style modern living room",
    # ],
    # [
    #     "305d3251-8f1e-4cca-9227-011187146d89",
    #     "fairy_tale",
    #     "a fairy tale style bedroom",
    # ],
    # [
    #     "01805656-e66f-44b1-8bc1-5e722fff3fff",
    #     "doodle",
    #     "a doodle style monochrome bedroom",
    # ],
    # [
    #     "a37f9f03-7361-4fe4-8aa7-718f41855ea5",
    #     "game_of_throne",
    #     "a game of throne style bedroom",
    # ],
]


def format_string(s, **kwargs):
    for k, v in kwargs.items():
        s = s.replace(f"{{{k}}}", str(v))
    return s


def generate_job(scene_name, short_prompt, prompt_stuff):
    prompt_thing = "the {thing_type} in " + prompt_stuff

    stuff_pattern_file = "jobs/pattern/stuff.job"
    thing_pattern_file = "jobs/pattern/thing.job"
    combine_pattern_file = "jobs/pattern/combine.job"
    with open(stuff_pattern_file, "r") as f:
        stuff_pattern = f.read()
    with open(thing_pattern_file, "r") as f:
        thing_pattern = f.read()
    with open(combine_pattern_file, "r") as f:
        combine_pattern = f.read()

    job_dir = Path("jobs") / "scenes"
    job_dir.mkdir(exist_ok=True, parents=True)
    scene_dir = Path("data/3D-FRONT_preprocessed/scenes") / scene_name
    room_dir = next(scene_dir.iterdir())
    sphere_camera_file = room_dir / "cameras" / "sphere.yaml"
    input_dir = room_dir / "meshes"
    output_dir = Path("outputs") / "text2tex" / scene_name / short_prompt
    stuff_dir = input_dir / "stuff"
    stuff_obj_file = next(stuff_dir.glob("*.obj"))
    stuff_name = stuff_obj_file.stem

    sphere_camera = yaml.load(sphere_camera_file.read_text(), Loader=yaml.SafeLoader)
    camera_xyz = sphere_camera["at"][0]
    radius = sphere_camera["dist"]["max"]

    job = format_string(
        stuff_pattern,
        input_dir=stuff_dir,
        output_dir=output_dir / "stuff",
        stuff_name=stuff_name,
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
        thing_job = format_string(
            thing_pattern,
            input_dir=input_things_dir,
            scene_name=scene_name,
            thing_name=thing_name,
            output_dir=output_dir / "things" / thing_name,
            prompt=format_string(prompt_thing, thing_type=thing_type),
        )
        job += thing_job

    job += combine_pattern.format(scene_name=scene_name, short_prompt=short_prompt)

    with open(job_dir / f"{scene_name}_{short_prompt}.job", "w") as f:
        f.write(job)


if __name__ == "__main__":
    for i, (scene_name, short_prompt, prompt_stuff) in enumerate(
        scene_prompt_short_list
    ):
        generate_job(scene_name, short_prompt, prompt_stuff)
    submit_script = Path("jobs") / "scenes" / "submit.sh"
    with open(submit_script, "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f"for i in *.job; do\n    sbatch $i;\ndone")

import argparse
import inquirer
import os
import requests
import zipfile


def download_and_extract_template(template_url, project_name):
    template_name = template_url.split("/")[-5]
    zip_name = template_name + ".zip"
    r = requests.get(template_url)

    with open(zip_name, "wb") as f:
        f.write(r.content)

    with zipfile.ZipFile(zip_name, "r") as zip_ref:
        zip_ref.extractall(".")

    os.remove(zip_name)
    os.rename(template_name + "-main", project_name)


def create_project_from_template(template, project_name):
    if template == "First-person template":
        first_person_template_url = "https://codeload.github.com/Xarithma/GodotFirstPersonTemplate/zip/refs/heads/main"
        download_and_extract_template(first_person_template_url, project_name)

    elif template == "Third-person template":
        third_person_template_url = "https://codeload.github.com/Xarithma/GodotThirdPersonTemplate/zip/refs/heads/main"
        download_and_extract_template(third_person_template_url, project_name)


def main():
    print("Starting main function...")

    parser = argparse.ArgumentParser(description="A simple CLI tool.")
    parser.add_argument("--name", help="Specify project name")
    parser.add_argument("--features", nargs="*", help="Specify project features")
    parser.add_argument("--template", help="Specify project template")

    args = parser.parse_args()

    name = args.name
    template = args.template
    # features = args.features

    questions = []

    if not name:
        questions.append(inquirer.Text("name", message="Enter project name:"))

    if not template:
        questions.append(
            inquirer.List(
                "template",
                message="Select template:",
                choices=["First-person template", "Third-person template"],
            )
        )

    # if not features:
    #     questions.append(
    #         inquirer.Checkbox(
    #             "features",
    #             message="Select features:",
    #             choices=["Touch screen controls"],
    #         )
    #     )

    if questions:
        answers = inquirer.prompt(questions)
        name = answers.get("name", name)
        template = answers.get("template", template)
        # features = answers.get("features", features)

    print(f"Creating project with name {name}...")
    print(f"Downloading template {template}...")
    create_project_from_template(template, name)
    # print(f"Using features: {features}")
    print("\n")
    print("Done!")
    print("\n")
    print("If you have Godot installed to path, run it with:")
    print("\n")
    print(f"  cd {name}")
    print("  godot project.godot")
    print("\n")


if __name__ == "__main__":
    main()

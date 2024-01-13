import argparse
import os
import yaml

from deep_merge import merge

OVERRIDE_KEY = "override"
arg_relative_path = ''
arg_ws_prefix = ''


class CustomDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(CustomDumper, self).increase_indent(flow, False)


def generate_projects_config(project_names: list[str], project_settings: dict) -> list:
    parent_settings = project_settings["projects"]
    per_project_settings = get_project_specific_settings(project_settings)

    return list(map(lambda project_name: generate_project_config(
        project_name,
        parent_settings,
        per_project_settings
    ), project_names))


def generate_project_config(
        project_name: str,
        parent_settings,
        per_project_settings: dict
) -> dict:
    mandatory_settings = get_project_mandatory_settings(project_name)
    specific_settings = per_project_settings.get(f"project-{project_name}", {})

    return generate_project_specific_config(
        mandatory_settings,
        parent_settings,
        specific_settings
    )


def get_project_mandatory_settings(project_name: str) -> dict:
    return {
        "name": project_name,
        "dir": f"{arg_relative_path}{project_name}",
        "workspace": f"{arg_ws_prefix}{project_name}"
    }


def generate_project_specific_config(
        mandatory_settings: dict,
        parent_settings: dict,
        project_specific_settings: dict
) -> dict:
    if project_specific_settings:
        if project_specific_settings.get(OVERRIDE_KEY, None):
            del project_specific_settings[OVERRIDE_KEY]
            return merge(mandatory_settings, project_specific_settings)

        return merge(mandatory_settings, parent_settings, project_specific_settings)

    return merge(mandatory_settings, parent_settings)


def get_config(config_file_path: str) -> tuple:
    config_template_file = get_config_template_file(config_file_path)
    config = yaml.load(config_template_file, Loader=yaml.Loader)
    return get_global_settings(config), get_projects_settings(config)


def get_config_template_file(file_path):
    return read_file(file_path)


def get_global_settings(config: dict) -> dict:
    def filter_project_keys(pair: tuple):
        return not check_tuple_key_prefix(pair, "project")

    return dict(filter(filter_project_keys, config.items()))


def get_projects_settings(config: dict) -> dict:
    def filter_project_keys(pair: tuple):
        return check_tuple_key_prefix(pair, "project")

    return dict(filter(filter_project_keys, config.items()))


def get_project_specific_settings(global_projects_settings: dict) -> dict:
    def filter_project_keys(pair: tuple):
        return check_tuple_key_prefix(pair, "project-")

    return dict(filter(filter_project_keys, global_projects_settings.items()))


def list_folders(directory) -> list:
    try:
        # List non-hidden folders in the specified directory
        names = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder)) and not folder.startswith('.')]
        names.sort()
        return names

    except Exception as e:
        print(f"An error occurred: {e}")


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def check_tuple_key_prefix(pair: tuple, prefix: str):
    key, _ = pair
    if key.startswith(prefix):
        return True
    return False


def write_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File successfully written to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def init_argparse():
    global arg_relative_path
    global arg_ws_prefix

    parser = argparse.ArgumentParser(description="Generate atlantis yaml config file")

    parser.add_argument(
        "-c", "--config_file", default=f"{os.getcwd()}/atlantis.yaml.tmpl",
        help="Additional atlantis configuration to be added."
    )
    parser.add_argument(
        "-d", "--directory", default="./",
        help="RELATIVE path where the project folders are hosted. Defaults to current directory './' ."
    )
    parser.add_argument(
        "-o", "--output", default=f"{os.getcwd()}/atlantis.yaml",
        help="Output file to be generated. Defaults to 'atlantis.yaml' on the current working directory."
    )
    parser.add_argument(
        "-p", "--prefix", default="",
        help="Workspace name prefix. Will be included in all workspace names."
    )

    # Return -v flag to print the cli tool version
    parser.add_argument(
        "-v", "--version", default="3",
        help="Atlantis yaml version. Defaults to version 3."
    )

    args = parser.parse_args()

    arg_relative_path = args.directory
    arg_ws_prefix = args.prefix

    return args


def main() -> None:
    args = init_argparse()

    global_config, project_settings = get_config(args.config_file)
    project_names = list_folders(args.directory)
    parent_settings = project_settings["projects"]
    per_project_settings = get_project_specific_settings(project_settings)

    projects_config = list(
        map(lambda project_name: generate_project_config(
            project_name,
            parent_settings,
            per_project_settings
        ), project_names)
    )

    global_config["projects"] = projects_config

    atlantis_yaml = yaml.dump(
        global_config,
        Dumper=CustomDumper,
        allow_unicode=True,
        sort_keys=False
    )

    write_file(args.output, atlantis_yaml)


if __name__ == '__main__':
    raise SystemExit(main())

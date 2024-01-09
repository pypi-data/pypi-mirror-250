#!/usr/bin/env python
"""Combine documentation files and write them out."""

import argparse
from collections import OrderedDict
import json
import os
import sys
from typing import Dict, Sequence, Tuple


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Combine documentation files and write them out.",
        usage=(
            "write_docs -p docs -s intro usage "
            "-oj nextflow_config.json -ot README.md"
        )
    )

    parser.add_argument(
        '-p',
        '--paths',
        required=True,
        nargs="+",
        help='Locations (files or dirs) in which to find doc files.'
    )

    parser.add_argument(
        '-s',
        '--sections',
        required=True,
        nargs="+",
        help='Names of required documentation sections.'
    )

    parser.add_argument(
        '-e',
        '--extensions',
        nargs="+",
        required=True,
        default=['.rst', '.txt', '.md'],
        help='List of allowed extensions.'
    )

    parser.add_argument(
        '-oj',
        '--output_json',
        help='Path at which to output JSON.'
    )

    parser.add_argument(
        '-ot',
        '--output_text',
        help='Path at which to output JSON.'
    )

    parser.add_argument(
        '-ns',
        '--nextflow_schema',
        required=True,
        help='Nextflow schema JSON.'
    )

    parser.add_argument(
        '-od',
        '--output_definition',
        required=False,
        help='Output definition JSON.'
    )

    args = parser.parse_args(sys.argv[1:])
    return args


def load_file(
    name: str,
    path: str
) -> Dict[str, str]:
    """Load documentation from file."""
    with open(path) as read_in:
        contents = "".join(read_in.readlines())
        return {name: contents}


def check_path(
    path: str,
    required: Sequence[str],
    extensions: Sequence[str]
) -> Tuple[bool, str]:
    """Check if a path exists and has the right extension."""
    basename = os.path.basename(path)
    nameroot, nameext = os.path.splitext(basename)
    if (
        os.path.isfile(path)
        and nameroot in required
        and nameext in extensions
    ):
        return True, nameroot
    return False, nameroot


def load(
    paths: Sequence[str],
    required: Sequence[str],
    extensions: Sequence[str]
) -> Dict[str, str]:
    """Load documentation from paths."""
    sections = {}
    for item in paths:
        check, name = check_path(
            item, required, extensions)
        if check:
            sections.update(load_file(name, item))
            continue
        if os.path.isdir(item):
            for subitem in os.listdir(item):
                subitem_path = f"{item}/{subitem}"
                subcheck, subname = check_path(
                    subitem_path, required, extensions)
                if not subcheck:
                    continue
                sections.update(
                    load_file(subname, subitem_path))
    return sections


def check(
    found: Dict[str, str], required: Sequence[str]
) -> None:
    """Check documentation is in order."""
    notfound_reqs = []
    for req in required:
        if not found.get(req):
            notfound_reqs.append(req)

    if notfound_reqs:
        notfound = ", ".join(notfound_reqs)
        print(
            "Error: Not all expected sections "
            f"were found: {notfound}")
        sys.exit(1)

    return OrderedDict(
        [(req, found[req]) for req in required])


def write_json(
    sections: Dict[str, str], path: str, key: str = 'docs'
) -> None:
    """Write documentation to json."""
    data = {}
    if os.path.exists(path):
        with open(path, "r") as existing_file:
            try:
                data.update(json.load(existing_file))
            except json.decoder.JSONDecodeError:
                raise RuntimeError(
                    "Error: Output JSON file exists but cannot "
                    f"be loaded, it may be corrupt: {path}")
    data.update({key: sections})
    with open(path, "w") as out_file:
        json.dump(data, out_file, indent=4)


def write_text(
    sections: Dict[str, str], path: str, workflow_title: str,
) -> None:
    """Write documentation to file."""
    joined_sections = ''
    title_dic = {
        "01_brief_description": str(workflow_title),
        "02_introduction": "Introduction",
        "03_compute_requirements": "Compute requirements",
        "04_install_and_run": "Install and run",
        "05_related_protocols": "Related protocols",
        "06_input_example": "Input example",
        "06_input_parameters": "Input parameters",
        "07_outputs": "Outputs",
        "08_pipeline_overview": "Pipeline overview",
        "09_troubleshooting": "Troubleshooting",
        "10_FAQ": "FAQ's",
        "11_other": "Related blog posts"}
    for k, v in sections.items():
        title = '## {}\n\n'.format(str(title_dic[k]))
        if k == "01_brief_description":
            title = '# {}\n\n'.format(str(title_dic[k]))
        joined_sections += title
        doc_text = '{}\n\n\n\n'.format(v)
        joined_sections += doc_text
    with open(path, "w") as new_file:
        new_file.write(joined_sections)


def dict_raise_on_duplicates(ordered_pairs):
    """Reject duplicate keys."""
    d = {}
    for k, v in ordered_pairs:
        if k in d:
            raise ValueError(
                "output_definition.json contains duplicate key: {}"
                .format(k))
        else:
            d[k] = v
    return d


def create_outputs(
        path: str,
        docs_folder: str,
) -> None:
    """Create outputs.md from output_definitions.json of workflow."""
    with open(path, 'r') as f:
        d = json.load(f, object_pairs_hook=dict_raise_on_duplicates)
        files = d['files']
    output_md = os.path.join(docs_folder[0], "07_outputs.md")
    with open(output_md, 'w+') as f:
        f.write(
            "Output files may be aggregated including information for all "
            "samples or provided per sample. Per-sample files "
            "will be prefixed with respective aliases and represented "
            "below as {{ alias }}.\n\n"
        )
        f.write(
            "| Title | File path | Description | Per sample or aggregated |\n")
        f.write(
            "|-------|-----------|-------------|--------------------------|\n")
        check_duplicates = list()
        for v in files.values():
            title = v['title']
            if title not in check_duplicates:
                check_duplicates.append(title)
            else:
                raise ValueError(
                    "output_definition.json contains duplicate title: {}"
                    .format(title))
            f.write(
                "| {} | {} | {} | {} |\n".format(
                    title, v["filepath"], v["description"], v["type"]))


def create_compute_requirements(
        path: str,
        docs_folder: str,
) -> None:
    """Create compute_requirements.md from nextflow_schema.json."""
    with open(path) as f:
        d = json.load(f)
        resources = d['resources']
    compute_md = os.path.join(docs_folder[0], "03_compute_requirements.md")
    with open(compute_md, 'w+') as f:
        f.write('Recommended requirements:\n\n')
        f.write('+ CPUs = {}\n'.format(resources["recommended"]["cpus"]))
        f.write('+ Memory = {}\n\n'.format(resources["recommended"]["memory"]))
        f.write('Minimum requirements:\n\n')
        f.write('+ CPUs = {}\n'.format(resources["minimum"]["cpus"]))
        f.write('+ Memory = {}\n\n'.format(resources["minimum"]["memory"]))
        f.write('Approximate run time: {}\n\n'.format(resources["run_time"]))
        f.write(
            'ARM processor support: {}\n'
            .format(str(resources["arm_support"])))


def create_brief_description(
        path: str,
        docs_folder: str,
) -> None:
    """Create brief_description.md from nextflow_schema.json of workflow."""
    with open(path) as f:
        d = json.load(f)
        description = d['description']
    desc_md = os.path.join(docs_folder[0], "01_brief_description.md")
    with open(desc_md, 'w+') as f:
        f.write(description)


def create_inputs(
        path: str,
        docs_folder: str,
) -> None:
    """Create input_parameters.md from nextflow_schema.json of workflow."""
    with open(path) as f:
        d = json.load(f)
        files = d['definitions']
    input_md = os.path.join(docs_folder[0], "06_input_parameters.md")
    with open(input_md, 'w+') as f:
        for _, v in files.items():
            # Count hidden params and don't add the section if all are hidden
            # Usually "hidden" value doesn't exist in the properties
            hidden_values = []
            for p in v["properties"].keys():
                if 'hidden' in v["properties"][p].keys():
                    if v["properties"][p]["hidden"]:
                        hidden_values.append(p)
            # Don't add form sections that have no parameters
            if len(v["properties"]) <= 1:
                continue
            # Don't add form sections if all parameters are hidden
            elif len(v["properties"]) == len(hidden_values):
                continue
            else:
                f.write("### {}\n\n".format(v["title"]))
                f.write(
                    "| Nextflow parameter name  | Type | Description | Help | Default |\n")  # noqa
                f.write("|--------------------------|------|-------------|------|---------|\n")  # noqa
                for prop, values in v["properties"].items():
                    # Don't add hidden parameters to the tables
                    # but check hidden=true
                    if prop in hidden_values:
                        pass
                    else:
                        f.write("| {} | {} | {} | {} | {} |\n".format(
                                prop,
                                values["type"],
                                values["description"],
                                values.get("help_text", ""),
                                values.get("default", "")))
                f.write('\n\n')


def main() -> None:
    """Parse arguments and launch a workflow."""
    args = parse_args()
    if args.output_definition:
        create_outputs(args.output_definition, args.paths)
    create_inputs(args.nextflow_schema, args.paths)
    create_compute_requirements(args.nextflow_schema, args.paths)
    create_brief_description(args.nextflow_schema, args.paths)
    with open(args.nextflow_schema) as f:
        d = json.load(f)
        workflow_title = d['workflow_title']
    sections = load(args.paths, args.sections, args.extensions)
    ordered = check(sections, args.sections)
    if args.output_json:
        write_json(ordered, args.output_json)
    if args.output_text:
        write_text(ordered, args.output_text, workflow_title)
    if not (args.output_json or args.output_text):
        print(ordered)


if __name__ == '__main__':
    main()

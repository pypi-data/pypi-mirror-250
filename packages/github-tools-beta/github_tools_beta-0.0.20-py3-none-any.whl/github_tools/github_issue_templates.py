#!/usr/bin/env python

import os
import logging
import argparse

try:
    from .gh_issue_templates import IssueTemplates
except:
    from gh_issue_templates import IssueTemplates


########################################################################################################################


def main():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s', level=logging.INFO)

    # The list of key vaults to check passed as command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-T", "--title", type=str,
                        help="The title of issue created.")

    parser.add_argument("-t", "--template_filenames", nargs='+',
                        default="c_epic.md d_collection.md e_task.md",
                        help="List of template filenames.\n"
                             "Valid filenames: a_team.md b_goal.md c_epic.md d_collection.md e_task.md"
                             "Default: c_epic.md d_collection.md e_task.md"
                        )

    parser.add_argument("-b", "--base_dir", type=str, help="")

    parser.add_argument("-d", "--templates_dir", type=str,
                        default='.github/ISSUE_TEMPLATE',
                        help="The directory of the issue templates. Default: '.github/ISSUE_TEMPLATE'")

    parser.add_argument("-r", "--templates_repo", type=str,
                        default='equinor/act-templates-st',
                        help="The GitHub repo which contains the issue templates.")

    parser.add_argument("-v", "--templates_version", type=str,
                        default='v0.0.2',
                        help="The GitHub Template Repo Release version")

    parser.add_argument("-n", "--team_name", type=str,
                        default='Azure Champions Team',
                        help="Value which replaces the '--team_name_placeholder' values.\n"
                             "This is is used in team and goal templates.\n"
                             "Default: Azure Champions Team")

    parser.add_argument("-N", "--team_name_placeholder", type=str,
                        default='<team_name>',
                        help="Occurrences of this value will be replaced with the value of '--team_name'.\n"
                             "Default: <team_name>")

    parser.add_argument("-a", "--team_alias", type=str,
                        help="Value which replaces the '--team_alias_placeholder' values")

    parser.add_argument("-A", "--team_alias_placeholder", type=str,
                        default='<team_alias>',
                        help="Occurrences of this value will be replaced with the value of '--team_alias'")

    parser.add_argument("-p", "--create_pr", action='store_true',
                        help="Create pr if new templates are created.")

    parser.add_argument("-u", "--update", action='store_true',
                        help="Update with template from repo")

    args = parser.parse_args()

    title = args.title
    template_filenames = args.template_filenames
    base_dir = args.base_dir
    templates_dir = args.templates_dir
    templates_version = args.templates_version
    templates_repo = args.templates_repo
    team_name = args.team_name
    team_name_placeholder = args.team_name_placeholder
    team_alias = args.team_alias
    team_alias_placeholder = args.team_alias_placeholder
    create_pr = args.create_pr
    update = args.update

    if not base_dir:
        base_dir = os.getcwd()

    for k, v in sorted(vars(args).items()):
        logging.info(f"Argument '{k}': '{v}'")

    if len(template_filenames) == 1:
        template_filenames = template_filenames[0].split()

    if not title:
        logging.error("no issue template provided")
        exit(2)

    if not isinstance(team_alias, str) or not len(team_alias) == 3:
        logging.error("team_alias length must be exactly 3 characters.")
        exit(2)

    issue_template = IssueTemplates(template_filenames, templates_repo, templates_version,
                                    team_name, team_name_placeholder, team_alias, team_alias_placeholder,
                                    templates_dir, base_dir=base_dir
                                    )

    if update:
        logging.info(f"Adding templates from template repo '{templates_repo}'..")
        issue_template.handle_templates(new=update)

        if create_pr:
            # TODO: add pr request
            pass

        return

    template = issue_template.get_template(title)
    if template:
        logging.info(f"OK. Outputting template for '{title}' type issue..")
        return template

    logging.warning(f"Template not found in local repo '{templates_dir}'.")
    logging.info(f"Will try to use template from dir '{templates_dir}' in repo '{templates_repo}' instead..")
    template = issue_template.get_template(title, new=True)

    if create_pr:
        # TODO: add pr request
        pass

    if template:
        logging.info(f"OK. Outputting template for '{title}' type issue..")
        return template

    logging.error(f"Template for '{title}' type issue not found in '{templates_dir}'")

########################################################################################################################


if __name__ == '__main__':
    output = main()
    if output:
        print(output)

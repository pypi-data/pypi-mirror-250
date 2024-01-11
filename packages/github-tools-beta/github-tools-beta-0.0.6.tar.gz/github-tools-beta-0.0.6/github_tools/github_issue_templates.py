#!/usr/bin/env python

import os
import logging
import argparse
from gh_issue_templates import IssueTemplates


########################################################################################################################


def main():
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    # The list of key vaults to check passed as command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-T", "--title", type=str,
                        help="The title of issue created.")

    parser.add_argument("-t", "--template_files", nargs='+',
                        default="c_epic.md d_collection.md e_task.md",
                        help="List of template filenames.\n"
                             "Valid filenames: a_team.md b_goal.md c_epic.md d_collection.md e_task.md"
                             "Default: c_epic.md d_collection.md e_task.md"
                        )

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
    template_files = args.template_files
    templates_dir = args.templates_dir
    templates_version = args.templates_version
    templates_repo = args.templates_repo
    team_name = args.team_name
    team_name_placeholder = args.team_name_placeholder
    team_alias = args.team_alias
    team_alias_placeholder = args.team_alias_placeholder
    create_pr = args.create_pr
    update = args.update

    #############################################################################
    team_alias = "ste"
    title = "🏆 arne - col"
    template_files = "a_team.md b_goal.md c_epic.md d_collection.md e_task.md"
    #############################################################################

    logging.info(f"title: {title}")
    logging.info(f"template_files: {template_files}")
    logging.info(f"templates_dir: {templates_dir}")
    logging.info(f"templates_repo: {templates_repo}")
    logging.info(f"templates_version: {templates_version}")
    logging.info(f"team_name: {team_name}")
    logging.info(f"team_name_placeholder: {team_name_placeholder}")
    logging.info(f"team_alias: {team_alias}")
    logging.info(f"team_alias_placeholder: {team_alias_placeholder}")
    logging.info(f"create_pr: {create_pr}")
    logging.info(f"update: {update}")

    if not title:
        logging.error("no issue template provided")
        exit(2)

    if not isinstance(team_alias, str) or not len(team_alias) == 3:
        logging.error("team_alias length must be exactly 3 characters.")
        exit(2)

    issue_template = IssueTemplates(template_files, templates_repo, templates_version, templates_dir,
                                    team_name, team_name_placeholder, team_alias, team_alias_placeholder)

    issue_template.handle_templates()
    template = issue_template.get_template(title)
    if template:
        logging.info(f"OK. Outputting template for {title} type issue..")
        return template

    if not template and os.path.isdir(templates_dir):
        logging.warning(f"Template not found in '{templates_dir}'.")
        logging.info(f"Adding templates from {templates_repo}..")
        issue_template.handle_templates(new=update)
        template = issue_template.get_template(title)

        if create_pr:
            # TODO: add pr request
            pass

        if template:
            logging.info(f"OK. Outputting template for {title} type issue..")
            return template

    if update:
        logging.info(f"Adding templates from template repo '{templates_repo}'..")
        issue_template.handle_templates(new=update)

        if create_pr:
            # TODO: add pr request
            pass

        return

    # TODO: feature to use without adding local template dir?

    #logging.warning(f"No templates found in {templates_dir}..")
    #logging.info(f"Returning shell commands to run..")
    #out = f"{80 * '#'}\n"
    #out += f"mkdir -p {templates_dir}\n"
    #out += f"{issue_template.get_gh_cmd()}\n"
    #out += f"{issue_template.get_tar_cmd()}\n"
    #out += f"{80 * '#'}\n"
    #return out

########################################################################################################################


if __name__ == '__main__':
    output = main()
    if output:
        print(output)

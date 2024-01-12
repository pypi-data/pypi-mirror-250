#!/usr/bin/env python

import os
import logging
import pathlib

########################################################################################################################


class IssueTemplates(object):
    """
    POC / WIP : Returns the correct issue templates based on provided issue title
    """

    def __init__(self, template_filenames, templates_repo, templates_version,
                 team_name, team_name_placeholder, team_alias, team_alias_placeholder,
                 issue_templates_dir,
                 archive_format="tar.gz",
                 base_dir=""):

        self.template_filenames = template_filenames
        if isinstance(template_filenames, str):
            self.template_filenames = template_filenames.split()

        self.templates_repo_name = templates_repo.split("/")[-1]
        self.templates_version = templates_version.replace("v", "")

        self.team_name = team_name
        self.team_name_placeholder = team_name_placeholder
        self.team_alias = team_alias
        self.team_alias_placeholder = team_alias_placeholder

        self.archive_format = archive_format

        if not base_dir:
            base_dir = os.getcwd()

        self.templates_dir = os.path.join(base_dir, issue_templates_dir)
        self.repo_templates_dir = os.path.join(base_dir,
                                               f"{self.templates_repo_name}-{self.templates_version}",
                                               issue_templates_dir)
        self.templates = []

    def handle_templates(self, new=False):
        templates_dir = self.templates_dir

        if new:
            templates_dir = self.repo_templates_dir

        script_dir = pathlib.Path(__file__).parent.resolve()
        logging.info(f"script_dir : '{script_dir}'")
        logging.info(os.listdir(script_dir))

        base_dir = pathlib.Path(script_dir).parent.resolve()
        logging.info(f"base_dir : '{base_dir}'")
        logging.info(os.listdir(base_dir))

        logging.info(f"looking in dir '{templates_dir}'..")
        if not os.path.isdir(templates_dir):
            logging.error(f"'{templates_dir}' dir does not exists.")
            return False

        for item in os.listdir(templates_dir):
            template_file = os.path.join(templates_dir, item)
            if os.path.isfile(template_file):
                template = self.read_template(template_file)
                if template:
                    self.templates.append(template)
                    if new:
                        self.write_template(template_file, template)

        if self.templates:
            return True

    def write_template(self, item, template):
        version = template.get("version")
        header = template.get("header")
        body = template.get("body")
        content = "---\n"
        content += f"version: '{version}'\n"
        for line in header.splitlines():
            content += f"{line}\n"
        content += "---\n"
        for line in body.splitlines():
            content += f"{line}\n"

        with open(os.path.join(self.templates_dir, item), "w") as f:
            f.write(content)

    def replace_placeholder(self, s):
        row = s.replace(self.team_name_placeholder, self.team_name)
        row = row.replace(self.team_alias_placeholder, self.team_alias)
        return row

    def read_template(self, template_file):
        with open(template_file) as f:
            template = {}
            for line in f.readlines():
                if not template and line.startswith("---"):
                    template["header"] = ""
                elif template and not line.startswith("---") and "body" not in template:
                    template["header"] += self.replace_placeholder(line)
                    if line.startswith("title: "):
                        prefix = line.split("title: ")
                        prefix = prefix[-1].split()
                        prefix = prefix[0]
                        prefix = prefix.replace("'", "")
                        prefix = prefix.replace('"', '')
                        template["prefix"] = prefix
                elif template and line.startswith("---"):
                    template["body"] = ""
                elif not line.startswith("---") and "body" in template:
                    template["body"] += self.replace_placeholder(line)
            template["name"] = template_file.split("/")[-1]
            template["version"] = self.templates_version
            return template

    def get_template(self, title):
        if not title:
            logging.error("No issue template title")
            return

        if not self.templates_dir:
            logging.error("No templates dir.")
            return

        logging.info(f"Looking for template matching title: '{title}'..")
        for template in self.templates:
            prefix = template.get("prefix")
            name = template.get("name")
            if title.encode('unicode-escape').decode('ASCII').startswith(prefix):
                logging.info(f"Using '{name}' template for prefix: '{prefix}'")
                return template.get("body")
            if title.startswith(prefix):
                logging.info(f"Using '{name}' template for prefix: '{prefix}'")
                return template.get("body")

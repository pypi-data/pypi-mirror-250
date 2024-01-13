#!/usr/bin/env python

import os
import logging

########################################################################################################################


class IssueTemplates(object):
    """
    POC / WIP : Returns the correct issue templates based on provided issue title
    """

    def __init__(self, templates_dir, template_filenames,
                 team_name, team_name_placeholder, team_alias, team_alias_placeholder):

        self.templates_dir = templates_dir

        self.template_filenames = template_filenames
        if isinstance(template_filenames, str):
            self.template_filenames = template_filenames.split()

        self.team_name = team_name
        self.team_name_placeholder = team_name_placeholder
        self.team_alias = team_alias
        self.team_alias_placeholder = team_alias_placeholder
        self.templates = []

    def handle_templates(self, write_template=False):
        if not os.path.isdir(self.templates_dir):
            logging.info(f"'{self.templates_dir}' dir does not exists.")
            return False

        logging.info(f"looking in dir '{self.templates_dir}'..")
        for item in self.template_filenames:
            template_file = os.path.join(self.templates_dir, item)
            if os.path.isfile(template_file):
                template = self.read_template(template_file)
                if template:
                    self.templates.append(template)
                    if write_template:
                        self.write_template(item, template)

        if self.templates:
            return True

    def write_template(self, item, template):
        if not os.path.isdir(self.templates_dir):
            os.makedirs(self.templates_dir)

        header = template.get("header")
        body = template.get("body")
        content = "---\n"
        for line in header.splitlines():
            content += f"{line}\n"
        content += "---\n"
        for line in body.splitlines():
            content += f"{line}\n"

        with open(os.path.join(self.templates_dir, item), "w") as f:
            f.write(content)

    def replace_placeholder(self, string):
        row = string.replace(self.team_name_placeholder, self.team_name)
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
            return template

    def get_template(self, title, update_templates=False):
        if not self.handle_templates(write_template=update_templates):
            return

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

            if not prefix:
                logging.info(f"Prefix: '{prefix}'. Using '{name}' template.")
                return template.get("body")

            if title.encode('unicode-escape').decode('ASCII').startswith(prefix):
                logging.info(f"Prefix: '{prefix}'. Using '{name}' template.")
                return template.get("body")

            if title.startswith(prefix):
                logging.info(f"Prefix: '{prefix}'. Using '{name}' template.")
                return template.get("body")

#!/usr/bin/env python

import os
import logging

########################################################################################################################


class IssueTemplates(object):
    """
    POC / WIP : Returns the correct issue templates based on provided issue title
    """

    def __init__(self, template_files, templates_repo, templates_version, templates_dir,
                 team_name, team_name_placeholder, team_alias, team_alias_placeholder,
                 archive_format="tar.gz"):
        self.template_files = template_files
        self.templates_repo = templates_repo
        self.templates_version = templates_version.replace("v", "")
        self.team_name = team_name
        self.team_name_placeholder = team_name_placeholder
        self.team_alias = team_alias
        self.team_alias_placeholder = team_alias_placeholder
        self.templates_dir = templates_dir
        self.archive_format = archive_format

        if isinstance(template_files, str):
            self.template_files = template_files.split()

        if not isinstance(templates_dir, str):
            self.templates_dir = ""

        self.repo_templates_name = self.templates_repo.split("/")[-1]
        self.repo_templates_dir = os.path.join(f"{self.repo_templates_name}-{self.templates_version}", self.templates_dir)
        self.templates = []

    def get_tar_cmd(self):
        return f"tar xvfz {self.repo_templates_name}-{self.templates_version}.{self.archive_format}"

    def get_gh_cmd(self):
        return f"gh release download v{self.templates_version} -R {self.templates_repo} --archive={self.archive_format}"

    def handle_templates(self, new=False):
        templates_dir = self.templates_dir

        if new:
            templates_dir = self.repo_templates_dir

        if not os.path.isdir(templates_dir):
            logging.error(f"{templates_dir} does not exists.")
            return False

        for template_file in self.template_files:
            if os.path.isfile(os.path.join(templates_dir, template_file)):
                template = self.read_template(templates_dir, template_file)
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

    def read_template(self, templates_dir, item):
        with open(os.path.join(templates_dir, item)) as f:
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
            template["name"] = item
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

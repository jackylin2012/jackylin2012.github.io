#!/usr/bin/env python3
"""
Website Generator Script

This script reads markdown files from the sections directory and a configuration file
to generate a personal website using the HTML template.
"""

import json
import markdown
import os
from datetime import datetime


def read_markdown_file(file_path):
    """Read and convert markdown file to HTML"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
            return markdown.markdown(md_content)
    return ""


def read_config(config_path):
    """Read configuration file"""
    with open(config_path, 'r') as f:
        return json.load(f)


def generate_webpage(template_path, output_path, config, content_sections):
    """Generate the final webpage by replacing placeholders in the template"""
    # Read the template
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Handle CV link section separately
    if 'cv_link' in config and config['cv_link']:
        cv_link_section = f'            <p><a href="{config["cv_link"]}">[CV]</a></p>'
    else:
        cv_link_section = ''

    # Replace placeholders with actual content
    for key, value in config.items():
        # Skip the sections array as it's not a direct placeholder
        if key == "sections":
            continue
        placeholder = "{{ " + key + " }}"
        template = template.replace(placeholder, str(value))

    for section, content in content_sections.items():
        placeholder = "{{ " + section + "_content }}"
        template = template.replace(placeholder, content)

    # Replace the CV link section placeholder
    template = template.replace("{{ cv_link_section }}", cv_link_section)

    # Write the final HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template)


def main():
    """Main function to generate the website"""
    # Configuration
    config = read_config('config.json')

    # Always update last_updated with current date
    config['last_updated'] = datetime.now().strftime("%B %d, %Y")

    # Read content sections specified in config
    content_sections = {}

    # Use sections from config if available, otherwise use default sections
    sections = config.get('sections', [
        'about', 'publications', 'working_papers', 'courses',
        'grants', 'education', 'contact', 'recruitment'
    ])

    for section in sections:
        content_sections[section] = read_markdown_file(f'sections/{section}.md')

    # Generate the webpage
    generate_webpage(
        template_path='personal_template.html',
        output_path='index.html',
        config=config,
        content_sections=content_sections
    )

    print("Website generated successfully!")


if __name__ == "__main__":
    main()
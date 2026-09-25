from pathlib import Path

import material
import yaml

def get_icon_svg(name):
    path = Path(material.__file__).parent / "templates/.icons" / f"{name}.svg"
    return path.read_text(encoding="utf-8") if path.exists() else ""

def generate_member_html(author):
    socials = "".join(
        f'<a href="{social["link"]}" class="member-social" '
        f'aria-label="{social["icon"]}" target="_blank" rel="noopener">'
        f'{get_icon_svg(social["icon"])}</a>'
        for social in author.get("social", [])
        if social.get("icon") and social.get("link")
    )

    return f"""
<div class="member">
  <img src="{author.get("avatar", "")}" alt="{author.get("name", "")}" class="member-avatar">
  <div class="member-info">
    <h2 class="member-name">{author.get("name", "")}</h2>
    <div class="member-affiliation">{author.get("affiliation", "")}</div>
    <p class="member-description">{author.get("description", "")}</p>
    <div class="member-socials">{socials}</div>
  </div>
</div>
"""

def on_page_markdown(markdown, page, config, files):
    if page.file.src_uri != "members.md":
        return markdown

    path = Path(config["docs_dir"]) / "blog/.authors.yml"

    with path.open(encoding="utf-8") as file:
        authors = yaml.safe_load(file)["authors"]

    members = "".join(generate_member_html(author) for author in authors.values())

    return markdown.replace(
        '<div class="members-list">\n</div>',
        f'<div class="members-list">\n{members}</div>'
    )
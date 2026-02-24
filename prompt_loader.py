from pathlib import Path

PROMPT_TEMPLATE_FILE = "system_prompt.txt"


def load_system_prompt(flat_data: str, prompt_template_file: str = PROMPT_TEMPLATE_FILE) -> str:
    template_path = Path(__file__).resolve().parent / prompt_template_file

    try:
        template = template_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Error loading prompt template '{template_path}': {exc}")
        template = "You are the strict Sales AI called 'Rashed' for Roof Comfort.\n\n{FLAT_DATA}"

    if "{FLAT_DATA}" in template:
        return template.replace("{FLAT_DATA}", flat_data)

    print(
        f"Warning: '{template_path}' does not include {{FLAT_DATA}}. "
        "Appending flat data at the end."
    )
    return f"{template.rstrip()}\n\n{flat_data}"

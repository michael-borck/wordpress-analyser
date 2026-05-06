import re
from pathlib import Path

from .models import HookCall, WordPressAnalysisResult

# ---------------------------------------------------------------------------
# Compiled regex patterns
# ---------------------------------------------------------------------------

# Hooks — registration
ADD_ACTION = re.compile(r"add_action\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]?([^'\",$\s)]+)")
ADD_FILTER = re.compile(r"add_filter\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]?([^'\",$\s)]+)")
DO_ACTION = re.compile(r"do_action\s*\(\s*['\"]([^'\"]+)['\"]")
APPLY_FILTERS = re.compile(r"apply_filters\s*\(\s*['\"]([^'\"]+)['\"]")

# WP API
SHORTCODE = re.compile(r"add_shortcode\s*\(\s*['\"]([^'\"]+)['\"]")
POST_TYPE = re.compile(r"register_post_type\s*\(\s*['\"]([^'\"]+)['\"]")
TAXONOMY = re.compile(r"register_taxonomy\s*\(\s*['\"]([^'\"]+)['\"]")

# WP function calls (broad prefix scan)
WP_FUNC = re.compile(r"\b(wp_|get_the_|get_post|the_|esc_|sanitize_|register_)\w+\s*\(")

# PHP quality signals
FUNCTION_DEF = re.compile(r"\bfunction\s+\w+\s*\(")
CLASS_DEF = re.compile(r"\bclass\s+\w+")
DB_QUERY = re.compile(r"\$wpdb\s*->\s*(query|get_results|get_row|get_var)\s*\(")
NONCE = re.compile(r"\b(check_ajax_referer|wp_verify_nonce|wp_nonce_field)\s*\(")
ESCAPE = re.compile(r"\b(esc_html|esc_attr|esc_url|esc_js|wp_kses)\s*\(")
DIRECT_OUT = re.compile(r"\b(echo|print)\s+|<\?=")
PHP8_FEATURES = re.compile(r"\bmatch\s*\(|^\s*enum\s+|\breadonly\s+|#\[")

# File-type markers
PLUGIN_HEADER = re.compile(r"Plugin Name\s*:", re.IGNORECASE)
THEME_FUNCTIONS = re.compile(r"\b(add_theme_support|wp_enqueue_scripts)\s*[('\"]")
TEMPLATE_MARKERS = re.compile(r"\b(get_header|get_footer)\s*\(")


def _strip_func_paren(name: str) -> str:
    """Remove trailing '(' from a matched WP function name."""
    return name.rstrip("(").rstrip()


def analyse_file(path: str | Path) -> WordPressAnalysisResult:
    """Analyse a WordPress PHP file and return signals."""
    path = Path(path)

    # --- validation ---
    if not path.exists():
        return WordPressAnalysisResult(
            filename=str(path),
            file_size=0,
            line_count=0,
            detected_type="utility",
            has_plugin_header=False,
            has_theme_functions=False,
            hook_calls=[],
            unique_hooks=[],
            action_count=0,
            filter_count=0,
            wp_functions=[],
            shortcodes=[],
            post_types=[],
            taxonomies=[],
            function_count=0,
            class_count=0,
            direct_db_queries=0,
            nonce_checks=0,
            output_escaping=0,
            direct_output=0,
            php_version_calls=[],
            error=f"File not found: {path}",
        )

    if path.suffix.lower() != ".php":
        return WordPressAnalysisResult(
            filename=path.name,
            file_size=0,
            line_count=0,
            detected_type="utility",
            has_plugin_header=False,
            has_theme_functions=False,
            hook_calls=[],
            unique_hooks=[],
            action_count=0,
            filter_count=0,
            wp_functions=[],
            shortcodes=[],
            post_types=[],
            taxonomies=[],
            function_count=0,
            class_count=0,
            direct_db_queries=0,
            nonce_checks=0,
            output_escaping=0,
            direct_output=0,
            php_version_calls=[],
            error=f"Not a .php file: {path.name}",
        )

    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return WordPressAnalysisResult(
            filename=path.name,
            file_size=0,
            line_count=0,
            detected_type="utility",
            has_plugin_header=False,
            has_theme_functions=False,
            hook_calls=[],
            unique_hooks=[],
            action_count=0,
            filter_count=0,
            wp_functions=[],
            shortcodes=[],
            post_types=[],
            taxonomies=[],
            function_count=0,
            class_count=0,
            direct_db_queries=0,
            nonce_checks=0,
            output_escaping=0,
            direct_output=0,
            php_version_calls=[],
            error=f"Read error: {exc}",
        )

    lines = content.splitlines()
    file_size = path.stat().st_size

    # --- per-line analysis ---
    hook_calls: list[HookCall] = []
    action_count = 0
    filter_count = 0

    for lineno, line in enumerate(lines, start=1):
        # add_action
        for m in ADD_ACTION.finditer(line):
            hook_calls.append(HookCall(type="action", hook=m.group(1), function=m.group(2), line=lineno))
            action_count += 1

        # add_filter
        for m in ADD_FILTER.finditer(line):
            hook_calls.append(HookCall(type="filter", hook=m.group(1), function=m.group(2), line=lineno))
            filter_count += 1

        # do_action (invocation — no callback)
        for m in DO_ACTION.finditer(line):
            hook_calls.append(HookCall(type="action", hook=m.group(1), function=None, line=lineno))
            action_count += 1

        # apply_filters (invocation — no callback)
        for m in APPLY_FILTERS.finditer(line):
            hook_calls.append(HookCall(type="filter", hook=m.group(1), function=None, line=lineno))
            filter_count += 1

    # --- full-text analysis ---
    unique_hooks = list(dict.fromkeys(hc.hook for hc in hook_calls))

    shortcodes = list(dict.fromkeys(m.group(1) for m in SHORTCODE.finditer(content)))
    post_types = list(dict.fromkeys(m.group(1) for m in POST_TYPE.finditer(content)))
    taxonomies = list(dict.fromkeys(m.group(1) for m in TAXONOMY.finditer(content)))

    # WP functions — strip trailing '(' and collect unique names
    wp_functions = list(
        dict.fromkeys(
            _strip_func_paren(m.group(0)) for m in WP_FUNC.finditer(content)
        )
    )

    function_count = len(FUNCTION_DEF.findall(content))
    class_count = len(CLASS_DEF.findall(content))
    direct_db_queries = len(DB_QUERY.findall(content))
    nonce_checks = len(NONCE.findall(content))
    output_escaping = len(ESCAPE.findall(content))
    direct_output = len(DIRECT_OUT.findall(content))

    php_version_calls = list(
        dict.fromkeys(m.group(0).strip() for m in PHP8_FEATURES.finditer(content))
    )

    has_plugin_header = bool(PLUGIN_HEADER.search(content))
    has_theme_functions = bool(THEME_FUNCTIONS.search(content))
    has_template_markers = bool(TEMPLATE_MARKERS.search(content))

    # --- detected_type heuristic ---
    if has_plugin_header:
        detected_type = "plugin"
    elif has_theme_functions:
        detected_type = "theme-functions"
    elif class_count >= 1 and function_count <= 3:
        detected_type = "class-file"
    elif has_template_markers:
        detected_type = "template"
    else:
        detected_type = "utility"

    return WordPressAnalysisResult(
        filename=path.name,
        file_size=file_size,
        line_count=len(lines),
        detected_type=detected_type,
        has_plugin_header=has_plugin_header,
        has_theme_functions=has_theme_functions,
        hook_calls=hook_calls,
        unique_hooks=unique_hooks,
        action_count=action_count,
        filter_count=filter_count,
        wp_functions=wp_functions,
        shortcodes=shortcodes,
        post_types=post_types,
        taxonomies=taxonomies,
        function_count=function_count,
        class_count=class_count,
        direct_db_queries=direct_db_queries,
        nonce_checks=nonce_checks,
        output_escaping=output_escaping,
        direct_output=direct_output,
        php_version_calls=php_version_calls,
    )

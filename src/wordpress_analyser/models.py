from pydantic import BaseModel


class HookCall(BaseModel):
    type: str       # "action" or "filter"
    hook: str
    function: str | None  # callback name, None for do_action/apply_filters
    line: int


class WordPressAnalysisResult(BaseModel):
    filename: str
    file_size: int
    line_count: int
    detected_type: str
    has_plugin_header: bool
    has_theme_functions: bool
    # Hooks
    hook_calls: list[HookCall]
    unique_hooks: list[str]
    action_count: int
    filter_count: int
    # WP API
    wp_functions: list[str]
    shortcodes: list[str]
    post_types: list[str]
    taxonomies: list[str]
    # PHP quality
    function_count: int
    class_count: int
    direct_db_queries: int
    nonce_checks: int
    output_escaping: int
    direct_output: int
    php_version_calls: list[str]
    error: str | None = None

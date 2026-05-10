"""POS+NEG coverage for regex rules previously untested."""

import pytest

from wordpress_analyser.core import analyse_file


# --- nonce_checks --------------------------------------------------------


def test_no_nonce_check_when_absent(empty_file):
    result = analyse_file(empty_file)
    assert result.nonce_checks == 0


# --- output_escaping -----------------------------------------------------


def test_no_output_escaping_when_absent(empty_file):
    result = analyse_file(empty_file)
    assert result.output_escaping == 0


# --- direct_db_queries ---------------------------------------------------


def test_direct_db_queries_detected(wpdb_file):
    # $wpdb->query(...) + $wpdb->get_results(...) = 2
    result = analyse_file(wpdb_file)
    assert result.direct_db_queries == 2


def test_no_direct_db_queries_when_absent(empty_file):
    result = analyse_file(empty_file)
    assert result.direct_db_queries == 0


# --- taxonomies ----------------------------------------------------------


def test_taxonomies_detected(taxonomy_file):
    result = analyse_file(taxonomy_file)
    assert "genre" in result.taxonomies


def test_no_taxonomies_when_absent(empty_file):
    result = analyse_file(empty_file)
    assert result.taxonomies == []


# --- detected_type heuristics --------------------------------------------


def test_theme_functions_detected_type(theme_functions_file):
    result = analyse_file(theme_functions_file)
    assert result.detected_type == "theme-functions"
    assert result.has_theme_functions is True
    assert result.has_plugin_header is False


def test_class_file_detected_type(class_file):
    result = analyse_file(class_file)
    assert result.detected_type == "class-file"


def test_plugin_header_takes_precedence_over_theme_functions(plugin_and_theme_file):
    """Plugin header wins over theme functions in detection."""
    result = analyse_file(plugin_and_theme_file)
    assert result.detected_type == "plugin"
    assert result.has_plugin_header is True
    assert result.has_theme_functions is True


# --- php_version_calls ---------------------------------------------------


def test_php_version_calls_detected(php8_file):
    result = analyse_file(php8_file)
    assert len(result.php_version_calls) > 0
    # PHP8 fixture uses #[Attribute] and match (...)
    assert any("#[" in call or "match" in call for call in result.php_version_calls)


def test_no_php_version_calls_when_absent(empty_file):
    result = analyse_file(empty_file)
    assert result.php_version_calls == []


# --- wp_functions list ---------------------------------------------------


def test_wp_functions_collected(plugin_file):
    """wp_functions should include known WP function names from the fixture."""
    result = analyse_file(plugin_file)
    assert isinstance(result.wp_functions, list)
    assert len(result.wp_functions) >= 3
    assert "wp_enqueue_script" in result.wp_functions
    assert "esc_html" in result.wp_functions


# --- HookCall callback extraction ----------------------------------------


def test_hook_callback_extracted(plugin_file):
    """add_action callback name must be captured on the matching HookCall."""
    result = analyse_file(plugin_file)
    init_calls = [hc for hc in result.hook_calls if hc.hook == "init"]
    assert len(init_calls) == 1
    assert init_calls[0].function == "my_init_function"

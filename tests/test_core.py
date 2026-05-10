import pytest
from wordpress_analyser.core import analyse_file


def test_plugin_detected(plugin_file):
    result = analyse_file(plugin_file)
    assert result.detected_type == "plugin"
    assert result.has_plugin_header is True


def test_hook_counts(plugin_file):
    result = analyse_file(plugin_file)
    # add_action('init', ...) + do_action('my_plugin_loaded') = 2
    assert result.action_count == 2
    # add_filter('the_content', ...) + apply_filters('my_plugin_value', ...) = 2
    assert result.filter_count == 2


def test_shortcode_detected(plugin_file):
    result = analyse_file(plugin_file)
    assert "myshortcode" in result.shortcodes


def test_post_type_detected(plugin_file):
    result = analyse_file(plugin_file)
    assert "product" in result.post_types


def test_nonce_check_detected(plugin_file):
    result = analyse_file(plugin_file)
    assert result.nonce_checks == 1


def test_output_escaping_detected(plugin_file):
    result = analyse_file(plugin_file)
    # esc_html(...) + esc_attr(...) = 2
    assert result.output_escaping == 2


def test_class_count(plugin_file):
    result = analyse_file(plugin_file)
    assert result.class_count == 1


def test_function_count(plugin_file):
    result = analyse_file(plugin_file)
    # function my_init_function() + public function run() = 2
    assert result.function_count == 2


def test_template_detected(template_file):
    result = analyse_file(template_file)
    assert result.detected_type == "template"


def test_nonexistent_file():
    result = analyse_file("/tmp/this_file_does_not_exist_wordpress.php")
    assert result.error is not None


def test_non_php_file(tmp_path):
    f = tmp_path / "notes.txt"
    f.write_text("some content")
    result = analyse_file(f)
    assert result.error is not None
    assert "php" in result.error.lower()


def test_unique_hooks(plugin_file):
    result = analyse_file(plugin_file)
    assert isinstance(result.unique_hooks, list)
    # init, the_content, my_plugin_loaded, my_plugin_value = 4 unique hooks
    assert len(result.unique_hooks) == 4

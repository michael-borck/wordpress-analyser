import pytest
from pathlib import Path

PLUGIN_PHP = '''<?php
/**
 * Plugin Name: My Test Plugin
 * Description: A test plugin
 */

add_action('init', 'my_init_function');
add_filter('the_content', 'my_content_filter');
add_shortcode('myshortcode', 'my_shortcode_handler');
register_post_type('product', array());

function my_init_function() {
    wp_enqueue_script('my-script', get_template_directory_uri() . '/script.js');
    check_ajax_referer('my_action', 'nonce');
    $title = esc_html(get_the_title());
    echo esc_attr($title);
}

class MyPlugin {
    public function run() {
        do_action('my_plugin_loaded');
        apply_filters('my_plugin_value', $value);
    }
}
'''

TEMPLATE_PHP = '''<?php
get_header();
the_title();
get_footer();
'''


@pytest.fixture
def plugin_file(tmp_path):
    f = tmp_path / "my-plugin.php"
    f.write_text(PLUGIN_PHP)
    return f


@pytest.fixture
def template_file(tmp_path):
    f = tmp_path / "template.php"
    f.write_text(TEMPLATE_PHP)
    return f

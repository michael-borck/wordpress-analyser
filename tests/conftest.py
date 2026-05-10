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

EMPTY_PHP = '''<?php
// nothing here
'''

THEME_FUNCTIONS_PHP = '''<?php
add_theme_support('post-thumbnails');
function setup_scripts() {
    wp_enqueue_scripts('main', '/main.js');
}
'''

WPDB_PHP = '''<?php
$results = $wpdb->query("SELECT * FROM wp_users");
$rows = $wpdb->get_results("SELECT id FROM wp_posts");
'''

TAXONOMY_PHP = '''<?php
register_taxonomy('genre', 'book');
'''

PHP8_PHP = '''<?php
#[Attribute]
class Foo {
    public function test($x) {
        return match ($x) {
            1 => "one",
            2 => "two",
            default => "other",
        };
    }
}
'''

CLASS_FILE_PHP = '''<?php
class FooBar {
    public function thing() {
        return 1;
    }
}
'''

PLUGIN_AND_THEME_PHP = '''<?php
/**
 * Plugin Name: Plugin Wins
 */
add_theme_support('post-thumbnails');
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


@pytest.fixture
def empty_file(tmp_path):
    f = tmp_path / "empty.php"
    f.write_text(EMPTY_PHP)
    return f


@pytest.fixture
def theme_functions_file(tmp_path):
    f = tmp_path / "functions.php"
    f.write_text(THEME_FUNCTIONS_PHP)
    return f


@pytest.fixture
def wpdb_file(tmp_path):
    f = tmp_path / "db.php"
    f.write_text(WPDB_PHP)
    return f


@pytest.fixture
def taxonomy_file(tmp_path):
    f = tmp_path / "taxonomy.php"
    f.write_text(TAXONOMY_PHP)
    return f


@pytest.fixture
def php8_file(tmp_path):
    f = tmp_path / "modern.php"
    f.write_text(PHP8_PHP)
    return f


@pytest.fixture
def class_file(tmp_path):
    f = tmp_path / "class.php"
    f.write_text(CLASS_FILE_PHP)
    return f


@pytest.fixture
def plugin_and_theme_file(tmp_path):
    f = tmp_path / "plugin-and-theme.php"
    f.write_text(PLUGIN_AND_THEME_PHP)
    return f

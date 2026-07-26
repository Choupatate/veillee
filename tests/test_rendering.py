from app.rendering import render_markdown


def test_highlight_renders_as_mark():
    html = render_markdown("This is ==important==.", "/story/2026-01-01-story/media")
    assert "<mark>important</mark>" in html


def test_lone_image_wrapped_in_figure_with_caption():
    html = render_markdown("![The big moment](photo-001.jpg)", "/story/2026-01-01-story/media")
    assert "<figure>" in html
    assert 'src="/story/2026-01-01-story/media/photo-001.jpg"' in html
    assert "<figcaption>The big moment</figcaption>" in html


def test_image_without_alt_has_no_figcaption():
    html = render_markdown("![](photo-002.jpg)", "/story/2026-01-01-story/media")
    assert "<figure>" in html
    assert "<figcaption>" not in html


def test_two_images_in_one_paragraph_each_become_a_figure():
    """Editors insert at the cursor, so two photos added in a row share a
    paragraph. As bare inline <img> they'd miss the figure styling and
    render at full pixel width, blowing out of the column (F35)."""
    html = render_markdown(
        "![](photo-001.jpg)![Asleep](photo-002.jpg)", "/story/2026-01-01-story/media"
    )
    assert html.count("<figure>") == 2
    assert "<p>" not in html
    assert 'src="/story/2026-01-01-story/media/photo-001.jpg"' in html
    assert "<figcaption>Asleep</figcaption>" in html


def test_images_separated_by_a_single_newline_also_become_figures():
    html = render_markdown(
        "![](photo-001.jpg)\n![](photo-002.jpg)", "/story/2026-01-01-story/media"
    )
    assert html.count("<figure>") == 2


def test_image_mixed_with_text_stays_inline():
    """That's what the author wrote; CSS keeps it inside the column."""
    html = render_markdown(
        "We walked and then ![](photo-001.jpg)she slept.", "/story/2026-01-01-story/media"
    )
    assert "<figure>" not in html
    assert "<p>We walked and then <img" in html


def test_a_linked_image_is_left_as_a_link():
    html = render_markdown(
        "[![](photo-001.jpg)](https://example.com)", "/story/2026-01-01-story/media"
    )
    assert "<figure>" not in html
    assert '<a href="https://example.com">' in html
    assert 'src="/story/2026-01-01-story/media/photo-001.jpg"' in html


def test_images_only_paragraph_between_prose_keeps_its_neighbours():
    html = render_markdown(
        "Before\n\n![](a.jpg)![](b.jpg)\n\nAfter", "/story/2026-01-01-story/media"
    )
    assert "<p>Before</p>" in html
    assert "<p>After</p>" in html
    assert html.count("<figure>") == 2
    assert html.index("Before") < html.index("<figure>") < html.index("After")


def test_image_inside_a_list_item_is_not_pulled_out():
    html = render_markdown("- ![](photo-001.jpg)\n- two", "/story/2026-01-01-story/media")
    assert "<figure>" not in html
    assert "<li><img" in html
    assert 'src="/story/2026-01-01-story/media/photo-001.jpg"' in html


def test_lone_image_in_a_blockquote_still_becomes_a_figure():
    html = render_markdown("> ![](photo-001.jpg)", "/story/2026-01-01-story/media")
    assert "<blockquote>" in html
    assert "<figure>" in html


def test_absolute_image_src_not_rewritten():
    html = render_markdown("![alt](https://example.com/photo.jpg)", "/story/2026-01-01-story/media")
    assert 'src="https://example.com/photo.jpg"' in html


def test_tables_and_lists_extensions_work():
    html = render_markdown("- one\n- two\n", "/story/2026-01-01-story/media")
    assert "<li>one</li>" in html
    assert "<li>two</li>" in html


def test_basic_paragraph_and_emphasis():
    html = render_markdown("Hello *world*.", "/story/2026-01-01-story/media")
    assert "<em>world</em>" in html


def test_repeated_calls_do_not_leak_media_base_or_parse_state():
    """render_markdown reuses one Markdown parser per thread (perf); each
    call must still be fully independent of the last."""
    first = render_markdown("![a](photo-001.jpg)", "/story/one/media")
    second = render_markdown("![b](photo-002.jpg)", "/people/two/media")
    third = render_markdown("Hello *world*.", "/story/one/media")

    assert 'src="/story/one/media/photo-001.jpg"' in first
    assert 'src="/people/two/media/photo-002.jpg"' in second
    assert "/story/one/media" not in second
    assert "<em>world</em>" in third
    assert "<figure>" not in third

from flask import g, has_request_context, render_template_string

from wtforms.widgets import Input

_WIDGET_TEMPLATE = '''
<!-- box-->
<div id="{{ field.id }}" >
    <div class="d-flex" >
        <input
            id="inner_{{ field.id }}"
            class="form-control mr-2"
            name="{{ field.id }}"
            type="text"
            value="{% if field.data %}{{field.data}}{% endif %}"
        ></input>
        <button
            class="btn btn-secondary"
            type="button"
            onclick="BrowseServer(
                '{{ url_for("flaskfilemanager.index") }}',
                'inner_{{ field.id }}'
            );"
        >Browse</button>
    </div>
    
    <div class="d-flex" style="align-items: flex-end;">
        <img
            id="img_inner_{{ field.id }}"
            class="mt-1"
            height="60"
            style="cursor: pointer; max-width: 120px; object-fit: contain;"
            data-toggle="modal"
            data-target="#florist_imageinput_modal"
            onclick="
                window.FloristImageInputWidget &&
                window.FloristImageInputWidget.openFromPreview(this);
            "
            {% if field.data %}
                src="{{field.data}}"
            {% else %}
                hidden="true"
            {% endif %}
        />
        <a
            id="a_inner_{{ field.id }}"
            class="pl-2 text-primary"
            style="cursor:pointer"
            onclick="ClearField('inner_{{ field.id }}')"
            {% if not field.data %}hidden="true"{%endif%}
        >Clear</a>
    </div>

</div>
'''


_SCRIPT_TEMPLATE = '''
<script>
    (function () {
        if (window.FloristImageInputWidget) return;

        function ensureModal() {
            var existing = document.getElementById(
                'florist_imageinput_modal'
            );
            if (existing) return existing;

            var wrapper = document.createElement('div');
            wrapper.innerHTML =
                '<div class="modal fade" id="florist_imageinput_modal" ' +
                'tabindex="-1" role="dialog" aria-hidden="true">' +
                '  <div class="modal-dialog modal-dialog-centered" ' +
                'role="document" style="max-width: 95vw;">' +
                '    <div class="modal-content">' +
                '      <div class="modal-header">' +
                '        <h5 class="modal-title">Preview</h5>' +
                '        <button type="button" class="close" ' +
                'data-dismiss="modal" aria-label="Close">' +
                '          <span aria-hidden="true">&times;</span>' +
                '        </button>' +
                '      </div>' +
                '      <div class="modal-body p-3 d-flex flex-column" ' +
                'style="height: 85vh; overflow: hidden;">' +
                '        <div id="florist_imageinput_modal_url" ' +
                'class="small text-muted mb-2 text-center" ' +
                'style="word-break: break-all;">' +
                '        </div>' +
                '        <div class="flex-fill d-flex" ' +
                'style="min-height: 0; overflow: auto;">' +
                '          <img id="florist_imageinput_modal_img" ' +
                'alt="preview" style="max-width: 100%; ' +
                'max-height: 100%; width: auto; height: auto; ' +
                'display: block; margin: auto;" />' +
                '        </div>' +
                '        <div class="d-flex justify-content-center mt-3">' +
                '          <div class="btn-group" role="group">' +
                '            <button type="button" ' +
                'class="btn btn-secondary btn-sm" ' +
                'id="florist_imageinput_modal_prev">Prev</button>' +
                '            <button type="button" ' +
                'class="btn btn-secondary btn-sm" ' +
                'id="florist_imageinput_modal_next">Next</button>' +
                '          </div>' +
                '        </div>' +
                '      </div>' +
                '    </div>' +
                '  </div>' +
                '</div>';

            document.body.appendChild(wrapper.firstElementChild);

            // Bind handlers once after modal is inserted.
            var prevBtn = document.getElementById(
                'florist_imageinput_modal_prev'
            );
            var nextBtn = document.getElementById(
                'florist_imageinput_modal_next'
            );
            if (prevBtn) {
                prevBtn.addEventListener('click', function () {
                    if (window.FloristImageInputWidget) {
                        window.FloristImageInputWidget.prev();
                    }
                });
            }
            if (nextBtn) {
                nextBtn.addEventListener('click', function () {
                    if (window.FloristImageInputWidget) {
                        window.FloristImageInputWidget.next();
                    }
                });
            }

            return document.getElementById('florist_imageinput_modal');
        }

        function getSrc(fieldId) {
            var preview = document.getElementById('img_inner_' + fieldId);
            var input = document.getElementById('inner_' + fieldId);

            return (
                (preview && (preview.currentSrc || preview.src)) ||
                (input && input.value) ||
                (preview &&
                    preview.getAttribute &&
                    preview.getAttribute('src')) ||
                ''
            );
        }

        function getFieldIdFromPreview(previewEl) {
            if (!previewEl || !previewEl.id) return '';
            if (previewEl.id.indexOf('img_inner_') !== 0) return '';
            return previewEl.id.slice('img_inner_'.length);
        }

        function getSrcFromPreview(previewEl, fieldId) {
            if (previewEl) {
                return (
                    (previewEl.currentSrc || previewEl.src) ||
                    (previewEl.getAttribute &&
                        previewEl.getAttribute('src')) ||
                    getSrc(fieldId)
                );
            }
            return getSrc(fieldId);
        }

        function setModalSrc(src) {
            var modal = ensureModal();
            var img = document.getElementById(
                'florist_imageinput_modal_img'
            );
            var url = document.getElementById(
                'florist_imageinput_modal_url'
            );

            if (img) img.setAttribute('src', src || '');
            if (url) url.textContent = src || '';
        }

        function setNavButtonState(currentIndex, total) {
            var prevBtn = document.getElementById(
                'florist_imageinput_modal_prev'
            );
            var nextBtn = document.getElementById(
                'florist_imageinput_modal_next'
            );

            var hasMany = total > 1;
            if (prevBtn) {
                prevBtn.disabled = !hasMany || currentIndex <= 0;
            }
            if (nextBtn) {
                nextBtn.disabled = !hasMany || currentIndex >= total - 1;
            }
        }

        function collectAllPreviews() {
            var nodes = document.querySelectorAll('img[id^="img_inner_"]');
            var result = [];

            for (var i = 0; i < nodes.length; i++) {
                var el = nodes[i];
                if (!el) continue;
                if (el.hasAttribute('hidden')) continue;
                if (el.offsetParent === null) continue;

                var fieldId = getFieldIdFromPreview(el);
                if (!fieldId) continue;

                var src = getSrcFromPreview(el, fieldId);
                if (!src) continue;

                result.push({ previewEl: el, fieldId: fieldId, src: src });
            }

            return result;
        }

        var _items = [];
        var _index = -1;

        function openAtIndex(index) {
            if (!_items || !_items.length) return;
            if (index < 0) index = 0;
            if (index >= _items.length) index = _items.length - 1;

            _index = index;
            // Refresh src in case input changed after initial collection.
            var item = _items[_index];
            var src = getSrcFromPreview(item.previewEl, item.fieldId);
            setModalSrc(src);
            setNavButtonState(_index, _items.length);
        }

        window.FloristImageInputWidget = {
            open: function (fieldId) {
                var previewEl = document.getElementById(
                    'img_inner_' + fieldId
                );
                if (previewEl) {
                    this.openFromPreview(previewEl);
                } else {
                    // Fallback: just show current value
                    setModalSrc(getSrc(fieldId));
                    setNavButtonState(0, 0);
                }
            },

            openFromPreview: function (previewEl) {
                var fieldId = getFieldIdFromPreview(previewEl);
                if (!fieldId) return;

                _items = collectAllPreviews();
                _index = -1;

                for (var i = 0; i < _items.length; i++) {
                    if (_items[i].fieldId === fieldId) {
                        _index = i;
                        break;
                    }
                }

                if (_index < 0) {
                    // Not found in list; just show this one.
                    setModalSrc(getSrcFromPreview(previewEl, fieldId));
                    setNavButtonState(0, 1);
                    return;
                }

                openAtIndex(_index);
            },

            prev: function () {
                if (_index <= 0) {
                    setNavButtonState(_index, _items.length);
                    return;
                }
                openAtIndex(_index - 1);
            },

            next: function () {
                if (_index < 0 || _index >= _items.length - 1) {
                    setNavButtonState(_index, _items.length);
                    return;
                }
                openAtIndex(_index + 1);
            },
        };
    })();
</script>
'''


class ImageInputWidget(Input):
    def __call__(self, field, **kwargs):
        widget_html = render_template_string(
            _WIDGET_TEMPLATE,
            field=field,
        )

        include_script = True
        if has_request_context():
            flag_name = '_florist_imageinputwidget_script_included'
            include_script = not getattr(g, flag_name, False)
            setattr(g, flag_name, True)

        if not include_script:
            return widget_html

        script_html = render_template_string(_SCRIPT_TEMPLATE)
        return widget_html + script_html

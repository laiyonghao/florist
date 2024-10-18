import pathlib
from flask import render_template, Blueprint, render_template_string

from wtforms.widgets import Input


# template_folder = pathlib.Path(__file__).parent.parent / 'templates'
# _ff_bp = Blueprint('_florist_form', __name__, template_folder=template_folder)

# print(f'{template_folder=}')


template = '''
<!-- box-->
<div id="{{ field.id }}" >
    <div class="d-flex" >
        <input id="inner_{{ field.id }}" class="form-control mr-2" name="{{ field.id }}" type="text" value="{% if field.data %}{{field.data}}{% endif %}"></input>
        <button class="btn btn-secondary" type="button" onclick="BrowseServer('{{ url_for("flaskfilemanager.index") }}', 'inner_{{ field.id }}');">Browse</button>
    </div>
    
    <div class="d-flex" style="align-items: flex-end;">
        <img id="img_inner_{{ field.id }}" class="mt-1" height="100" {% if field.data %}src="{{field.data}}"{%else%}hidden="true"{%endif%}/>
        <a id="a_inner_{{ field.id }}" class="pl-2 text-primary" style="cursor:pointer" onclick="ClearField('inner_{{ field.id }}')" {% if not field.data %}hidden="true"{%endif%}>Clear</a>
    </div>

</div>
'''


class ImageInputWidget(Input):
    def __call__(self, field, **kwargs):
        return render_template_string(
            template,
            field=field,
        )

import colander
import deform.widget
from wtforms import Form, TextAreaField, validators

from blog_pyramid.models.category import Category


def validate_unique_name(node, appstruct, dbsession):
    if dbsession.query(Category).filter_by(name=appstruct['name']).first():
        raise colander.Invalid(node, "Category already taken")


class CategoryCreateForm(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(), validator=colander.Length(min=3, max=20))
    description = colander.SchemaNode(colander.String(), validator=colander.Length(min=10, max=100), widget=deform.widget.TextAreaWidget())


class CategoryEditForm(Form):
    description = TextAreaField('Description', [validators.Length(min=10, max=100)])

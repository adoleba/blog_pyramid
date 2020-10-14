import colander
import deform.widget

from blog_pyramid.models.category import Category


def validate_unique_name(node, appstruct, dbsession):
    if dbsession.query(Category).filter_by(name=appstruct['name']).first():
        raise colander.Invalid(node, "Category already taken")


class CategoryForm(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    description = colander.SchemaNode(colander.String(), validator=colander.Length(max=100), widget=deform.widget.TextAreaWidget())


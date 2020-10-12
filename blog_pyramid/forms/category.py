import colander
import deform.widget


class CategoryForm(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(), validator=colander.Length(max=20))
    description = colander.SchemaNode(colander.String(), validator=colander.Length(max=100), widget=deform.widget.TextAreaWidget())

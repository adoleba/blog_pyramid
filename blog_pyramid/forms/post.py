import colander
import deform.widget

categories = (('A', 'Kategoria A'), ('B', 'Kategoria B'), ('C', 'Kategoria C'))


class PostForm(colander.MappingSchema):
    title = colander.SchemaNode(colander.String(), title="Tytuł", validator=colander.Length(max=30))
    intro = colander.SchemaNode(colander.String(), title="Intro", validator=colander.Length(max=100))
    body = colander.SchemaNode(colander.String(), title="Treść", widget=deform.widget.RichTextWidget())
    categories = colander.SchemaNode(colander.String(), title="Kategoria", widget=deform.widget.SelectWidget(values=categories))
